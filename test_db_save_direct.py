#!/usr/bin/env python3
"""
直接测试数据库保存功能
"""
import os
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_direct_db_save():
    """直接测试数据库保存"""
    print("=" * 60)
    print("直接测试数据库保存功能")
    print("=" * 60)
    
    # 加载环境变量
    try:
        from dotenv import load_dotenv
        env_path = project_root / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            print(f"[OK] 已加载 .env 文件")
    except ImportError:
        print("[!] python-dotenv 未安装，使用系统环境变量")
    
    # 检查环境变量
    supabase_url = os.getenv("SUPABASE_DB_URL")
    if not supabase_url:
        print("[X] SUPABASE_DB_URL 未设置")
        print("    请在 Render Dashboard 中设置此环境变量")
        return False
    
    print(f"[OK] SUPABASE_DB_URL 已设置")
    if "@" in supabase_url:
        parts = supabase_url.split("@")
        if len(parts) == 2:
            masked = parts[0].split(":")[0] + ":****@" + parts[1]
            print(f"    值: {masked}")
    
    # 尝试导入数据库模块
    try:
        from jubianai.backend.database import SessionLocal, VideoGeneration, User
        from jubianai.backend.video_history import VideoHistoryService
        from jubianai.backend.auth import AuthService
        print("[OK] 数据库模块导入成功")
    except ImportError as e:
        print(f"[X] 数据库模块导入失败: {e}")
        return False
    
    # 检查 SessionLocal
    if not SessionLocal:
        print("[X] SessionLocal 未初始化（数据库未配置）")
        return False
    
    print("[OK] SessionLocal 已初始化")
    
    # 尝试连接并测试保存
    try:
        db = SessionLocal()
        print("[OK] 数据库连接成功")
        
        # 检查表是否存在
        from sqlalchemy import inspect, text
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()
        
        print(f"\n数据库表列表: {tables}")
        
        if 'users' not in tables:
            print("[X] users 表不存在")
            db.close()
            return False
        print("[OK] users 表存在")
        
        if 'video_generations' not in tables:
            print("[X] video_generations 表不存在")
            print("    请运行 jubianai/supabase_init.sql 创建表")
            db.close()
            return False
        print("[OK] video_generations 表存在")
        
        # 检查默认用户
        default_user = db.query(User).filter(User.username == "default_user").first()
        if not default_user:
            print("[!] 默认用户不存在，尝试创建...")
            default_user = AuthService.get_or_create_default_user(db)
            print(f"[OK] 默认用户已创建: id={default_user.id}")
        else:
            print(f"[OK] 默认用户存在: id={default_user.id}")
        
        # 测试保存一条记录
        print("\n测试保存视频生成记录...")
        test_task_id = f"test_{int(__import__('time').time())}"
        try:
            generation = VideoHistoryService.create_generation_record(
                db=db,
                task_id=test_task_id,
                user_id=default_user.id,
                prompt="测试提示词",
                duration=5,
                fps=24,
                width=1280,
                height=720,
                status="pending"
            )
            print(f"[OK] 测试记录保存成功!")
            print(f"    记录 ID: {generation.id}")
            print(f"    任务 ID: {generation.task_id}")
            
            # 立即查询验证
            saved = db.query(VideoGeneration).filter(
                VideoGeneration.task_id == test_task_id
            ).first()
            
            if saved:
                print(f"[OK] 查询验证成功，记录确实已保存")
                # 删除测试记录
                db.delete(saved)
                db.commit()
                print(f"[OK] 测试记录已清理")
            else:
                print(f"[X] 查询验证失败，记录未找到")
            
            db.close()
            return True
            
        except Exception as save_error:
            print(f"[X] 保存测试记录失败: {save_error}")
            import traceback
            traceback.print_exc()
            db.close()
            return False
        
    except Exception as e:
        print(f"[X] 数据库操作失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_direct_db_save()
    
    print("\n" + "=" * 60)
    if success:
        print("[OK] 数据库保存功能测试通过")
        print("\n如果视频生成时仍然无法保存，可能的原因：")
        print("1. Render 环境变量中的 SUPABASE_DB_URL 与本地不同")
        print("2. 保存时出现异常但被捕获（检查 Render 日志）")
        print("3. 事务提交失败（检查数据库连接）")
    else:
        print("[X] 数据库保存功能测试失败")
        print("\n请检查：")
        print("1. SUPABASE_DB_URL 是否正确")
        print("2. 数据库表是否已创建")
        print("3. 数据库连接是否正常")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


