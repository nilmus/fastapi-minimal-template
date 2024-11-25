from typing import Annotated

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from fastapi import Depends

from . import env

database_url = env.DATABASE_SETTINGS.DB_URL

engine = sa.create_engine(database_url)


class Base(sa_orm.DeclarativeBase):
    pass


def create_db_and_tables():
    Base.metadata.create_all(engine)


def delete_db_and_tables():
    Base.metadata.drop_all(engine)


def get_session():
    Session = sa_orm.sessionmaker(engine)
    with Session() as session:
        try:
            yield session
        finally:
            session.close()


SessionDep = Annotated[sa_orm.Session, Depends(get_session)]
