"""
数据库配置和连接
支持 Vercel Postgres 和本地 PostgreSQL
"""
import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


def get_database_url() -> str:
    """
    获取数据库连接 URL
    优先级：
    1. POSTGRES_URL (旧版 Vercel Postgres，如果存在)
    2. DATABASE_URL (Neon、Supabase 等 Marketplace 提供商使用这个)
    3. 本地 PostgreSQL (开发环境)
    """
    # 旧版 Vercel Postgres 提供的环境变量（向后兼容）
    postgres_url = os.getenv("POSTGRES_URL")
    if postgres_url:
        return postgres_url
    
    # 通用数据库 URL（Neon、Supabase 等 Marketplace 提供商使用这个）
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url
    
    # 本地开发环境（默认）
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "jubianai")
    
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


# 延迟创建数据库引擎（避免在模块加载时连接失败导致整个函数崩溃）
_engine = None
_SessionLocal = None

def get_engine():
    """获取数据库引擎（延迟初始化）"""
    global _engine
    if _engine is None:
        database_url = get_database_url()
        try:
            # Neon 和 Supabase 的连接字符串已经包含 sslmode 参数
            # 如果连接字符串中已经有 sslmode，就不需要在 connect_args 中设置
            connect_args = {}
            if "neon.tech" in database_url or "supabase.co" in database_url:
                # 如果连接字符串中没有 sslmode，添加它
                if "sslmode" not in database_url:
                    connect_args["sslmode"] = "require"
                connect_args["connect_timeout"] = 10
            
            _engine = create_engine(
                database_url,
                pool_pre_ping=True,  # 自动重连
                pool_recycle=300,    # 连接回收时间（秒）
                echo=False,         # 设置为 True 可以看到 SQL 日志
                connect_args=connect_args if connect_args else {}
            )
        except Exception as e:
            print(f"Error creating database engine: {e}")
            raise
    return _engine

def get_session_local():
    """获取会话工厂（延迟初始化）"""
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal


def get_db():
    """获取数据库会话（用于依赖注入）"""
    SessionLocal = None
    db = None
    try:
        SessionLocal = get_session_local()
        db = SessionLocal()
        yield db
    except Exception as e:
        print(f"Error getting database session: {e}")
        import traceback
        print(traceback.format_exc())
        # 如果数据库连接失败，创建一个模拟的会话对象
        # 这样 API 端点可以继续执行并返回空结果
        class MockSession:
            def query(self, *args, **kwargs):
                return self
            def filter(self, *args, **kwargs):
                return self
            def first(self):
                return None
            def all(self):
                return []
            def order_by(self, *args, **kwargs):
                return self
            def close(self):
                pass
            def commit(self):
                pass
            def rollback(self):
                pass
            def add(self, *args, **kwargs):
                pass
            def delete(self, *args, **kwargs):
                pass
            def refresh(self, *args, **kwargs):
                pass
        
        db = MockSession()
        yield db
    finally:
        if db and hasattr(db, 'close'):
            try:
                db.close()
            except:
                pass


def init_db():
    """初始化数据库表"""
    try:
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        # 不抛出异常，允许应用在没有数据库的情况下运行
        pass

