"""
资产管理和知识库 API
使用 PostgreSQL 数据库存储元数据
"""
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime
import re
import os

from backend.models import Asset


class AssetMetadata(BaseModel):
    """资产元数据（兼容旧接口）"""
    filename: str
    character_name: str
    view_type: str
    file_path: str
    file_url: Optional[str] = None
    upload_time: str
    file_size: int
    id: Optional[int] = None


def parse_filename(filename: str) -> tuple[str, str]:
    """
    解析文件名，提取人物名称和视图类型
    格式：人物名-视图类型.扩展名
    例如：小明-正视图.jpg -> ("小明", "正视图")
         小美-侧视图.png -> ("小美", "侧视图")
    """
    # 移除扩展名
    name_without_ext = Path(filename).stem
    
    # 使用正则表达式匹配：人物名-视图类型
    match = re.match(r'^(.+?)-(.+)$', name_without_ext)
    
    if match:
        character_name = match.group(1).strip()
        view_type = match.group(2).strip()
        return character_name, view_type
    else:
        # 如果没有匹配到，使用文件名作为人物名，视图类型为"未知"
        return name_without_ext, "未知"


def get_assets_by_character(db: Session) -> Dict[str, List[AssetMetadata]]:
    """按人物分组获取资产（从数据库）"""
    try:
        assets = db.query(Asset).order_by(Asset.upload_time.desc()).all()
        assets_by_character: Dict[str, List[AssetMetadata]] = {}
        
        for asset in assets:
            character = asset.character_name
            if character not in assets_by_character:
                assets_by_character[character] = []
            assets_by_character[character].append(AssetMetadata(**asset.to_dict()))
        
        return assets_by_character
    except Exception as e:
        # 如果数据库连接失败，返回空字典
        print(f"Error getting assets from database: {e}")
        return {}


async def upload_asset(
    file: UploadFile,
    db: Session,
    file_url: Optional[str] = None
) -> AssetMetadata:
    """
    上传资产文件
    
    注意：在 Vercel Serverless 环境中，文件应该先上传到云存储（如 Vercel Blob Storage、S3），
    然后传入 file_url。这里只存储元数据到数据库。
    """
    # 检查文件类型
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型。支持的格式：{', '.join(allowed_extensions)}"
        )
    
    # 解析文件名
    character_name, view_type = parse_filename(file.filename)
    
    # 读取文件内容（用于获取文件大小）
    content = await file.read()
    file_size = len(content)
    
    # 生成文件路径（用于显示，实际文件存储在云存储）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{character_name}-{view_type}_{timestamp}{file_ext}"
    
    # 如果没有提供 file_url，使用临时路径（仅用于元数据）
    if not file_url:
        file_path = f"assets/{safe_filename}"
    else:
        file_path = file_url
    
    # 创建数据库记录
    try:
        db_asset = Asset(
            filename=file.filename,
            character_name=character_name,
            view_type=view_type,
            file_path=file_path,
            file_url=file_url or file_path,
            file_size=file_size,
            file_type="image"
        )
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        
        return AssetMetadata(**db_asset.to_dict())
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"保存资产元数据失败: {str(e)}"
        )


def delete_asset(filename: str, db: Session) -> bool:
    """删除资产（从数据库）"""
    try:
        # 查找资产
        asset = db.query(Asset).filter(
            (Asset.filename == filename) | 
            (Asset.file_path.contains(filename))
        ).first()
        
        if asset:
            db.delete(asset)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"Error deleting asset: {e}")
        return False


def get_asset_path(filename: str, db: Session) -> Optional[str]:
    """
    获取资产文件路径或 URL（从数据库）
    返回字符串路径/URL，而不是 Path 对象
    """
    try:
        asset = db.query(Asset).filter(
            (Asset.filename == filename) |
            (Asset.file_path.contains(filename)) |
            (Asset.file_url.contains(filename) if Asset.file_url else False)
        ).first()
        
        if asset:
            return asset.file_url or asset.file_path
        return None
    except Exception as e:
        print(f"Error getting asset path: {e}")
        return None


def get_asset_by_id(asset_id: int, db: Session) -> Optional[Asset]:
    """根据 ID 获取资产"""
    try:
        return db.query(Asset).filter(Asset.id == asset_id).first()
    except Exception as e:
        print(f"Error getting asset by id: {e}")
        return None
