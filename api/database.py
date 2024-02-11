from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uralsteel.settings import DATABASES

DB_DEFAULT = DATABASES['default']

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_DEFAULT['USER']}:{DB_DEFAULT['PASSWORD']}{DB_DEFAULT['HOST']}:{DB_DEFAULT['PORT']}@/{DB_DEFAULT['NAME']}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()