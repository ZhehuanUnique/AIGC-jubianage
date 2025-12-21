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
    1. POSTGRES_URL (Vercel Postgres)
    2. DATABASE_URL (通用环境变量)
    3. 本地 PostgreSQL (开发环境)
    """
    # Vercel Postgres 提供的环境变量
    postgres_url = os.getenv("POSTGRES_URL")
    if postgres_url:
        return postgres_url
    
    # 通用数据库 URL
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


# 创建数据库引擎
database_url = get_database_url()
engine = create_engine(
    database_url,
    pool_pre_ping=True,  # 自动重连
    pool_recycle=300,    # 连接回收时间（秒）
    echo=False           # 设置为 True 可以看到 SQL 日志
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """获取数据库会话（用于依赖注入）"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)

