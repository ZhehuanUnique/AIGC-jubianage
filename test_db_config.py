#!/usr/bin/env python3
"""
测试数据库配置脚本
用于检查数据库是否已正确配置
"""
import os
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_database_config():
    """测试数据库配置"""
    print("=" * 60)
    print("数据库配置检查")
    print("=" * 60)
    
    # 1. 检查环境变量
    print("\n1. 检查环境变量:")
    supabase_url = os.getenv("SUPABASE_DB_URL")
    database_url = os.getenv("DATABASE_URL")
    
    if supabase_url:
        print(f"   [OK] SUPABASE_DB_URL: 已设置")
        # 隐藏密码显示
        if "@" in supabase_url:
            parts = supabase_url.split("@")
            if len(parts) == 2:
                masked = parts[0].split(":")[0] + ":****@" + parts[1]
                print(f"      值: {masked}")
            else:
                print(f"      值: {supabase_url[:50]}...")
        else:
            print(f"      值: {supabase_url[:50]}...")
    else:
        print(f"   [X] SUPABASE_DB_URL: 未设置")
    
    if database_url:
        print(f"   [OK] DATABASE_URL: 已设置")
        if "@" in database_url:
            parts = database_url.split("@")
            if len(parts) == 2:
                masked = parts[0].split(":")[0] + ":****@" + parts[1]
                print(f"      值: {masked}")
            else:
                print(f"      值: {database_url[:50]}...")
        else:
            print(f"      值: {database_url[:50]}...")
    else:
        print(f"   [!] DATABASE_URL: 未设置（可选）")
    
    # 2. 尝试导入数据库模块
    print("\n2. 检查数据库模块:")
    try:
        from jubianai.backend.database import SessionLocal, engine, get_db
        print("   [OK] 数据库模块导入成功")
    except ImportError as e:
        print(f"   [X] 数据库模块导入失败: {e}")
        return False
    
    # 3. 检查 SessionLocal
    print("\n3. 检查数据库连接:")
    if SessionLocal:
        print("   [OK] SessionLocal 已初始化")
    else:
        print("   [X] SessionLocal 未初始化（数据库未配置）")
        return False
    
    # 4. 尝试连接数据库
    print("\n4. 测试数据库连接:")
    try:
        from jubianai.backend.database import SessionLocal
        db = SessionLocal()
        print("   [OK] 数据库连接成功")
        
        # 5. 检查表是否存在
        print("\n5. 检查数据库表:")
        try:
            from jubianai.backend.database import VideoGeneration, User
            from sqlalchemy import inspect
            
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            required_tables = ['video_generations', 'users']
            for table in required_tables:
                if table in tables:
                    print(f"   [OK] 表 '{table}' 存在")
                else:
                    print(f"   [X] 表 '{table}' 不存在")
            
            # 6. 检查记录数量
            print("\n6. 检查现有记录:")
            try:
                video_count = db.query(VideoGeneration).count()
                user_count = db.query(User).count()
                print(f"   [OK] 视频生成记录: {video_count} 条")
                print(f"   [OK] 用户记录: {user_count} 条")
            except Exception as e:
                print(f"   [!] 查询记录失败: {e}")
            
            db.close()
            
        except Exception as e:
            print(f"   [X] 检查表失败: {e}")
            db.close()
            return False
        
    except Exception as e:
        print(f"   [X] 数据库连接失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("[OK] 数据库配置检查完成 - 数据库已正确配置")
    print("=" * 60)
    return True

if __name__ == "__main__":
    # 加载 .env 文件（如果存在）
    try:
        from dotenv import load_dotenv
        env_path = project_root / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            print(f"已加载 .env 文件: {env_path}")
        else:
            print("未找到 .env 文件，使用系统环境变量")
    except ImportError:
        print("python-dotenv 未安装，跳过 .env 文件加载")
    
    success = test_database_config()
    sys.exit(0 if success else 1)

