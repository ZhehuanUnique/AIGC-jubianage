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
            _engine = create_engine(
                database_url,
                pool_pre_ping=True,  # 自动重连
                pool_recycle=300,    # 连接回收时间（秒）
                echo=False,         # 设置为 True 可以看到 SQL 日志
                connect_args={
                    "connect_timeout": 10,  # 连接超时 10 秒
                    "sslmode": "require" if "neon.tech" in database_url or "supabase.co" in database_url else "prefer"
                }
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
    try:
        SessionLocal = get_session_local()
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    except Exception as e:
        print(f"Error getting database session: {e}")
        # 返回一个空会话，避免整个请求失败
        # 在实际使用中，API 端点会处理这个错误
        raise


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

