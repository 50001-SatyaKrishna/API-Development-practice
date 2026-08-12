from sqlalchemy import create_engine, text
from app.config import settings

url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(url)
with engine.connect() as conn:
    print(conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")).fetchall())
    print(conn.execute(text("SELECT * FROM alembic_version")).fetchall())
