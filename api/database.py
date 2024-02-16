from datetime import datetime
from typing import Annotated

import pytz
from sqlalchemy import create_engine, TIMESTAMP, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column

from config import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={}
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

idpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[TIMESTAMP, mapped_column(
    TIMESTAMP,
    server_default=text('TIMEZONE("utc+5", now()'),
    default=datetime.now(pytz.timezone(settings.TIME_ZONE)))
]


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relations не будут выводиться на печать"""
        cols = []
        for index, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or index < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')

        return f'<{self.__class__.__name__} {", ".join(cols)}>'
