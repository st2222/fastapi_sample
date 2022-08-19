import sys
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DateTime, Boolean
from typing import Final
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DIALECT: Final[str] = "mysql"
DRIVER: Final[str] = "pymysql"
USERNAME: Final[str] = "root"
PASSWORD: Final[str] = "root"
HOST: Final[str] = "127.0.0.1"
PORT: Final[str] = "3306"
DATABASE: Final[str] = "nippo"
CHARSET_TYPE: Final[str] = "utf8"
DB_URL: Final[str] = f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset={CHARSET_TYPE}"


# DB接続するためのEngineインスタンス
ENGINE = create_engine(DB_URL, echo=True)


# DBに対してORM操作するときに利用
# Sessionを通じて操作を行う
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=True, bind=ENGINE)
)

Base = declarative_base()


session.configure(bind=ENGINE)


Base.metadata.bind = ENGINE
