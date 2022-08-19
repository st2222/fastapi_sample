# from db.models.report import ReportDataModel
# from db.models.user import UserDataModel
# from db.models.report_detail import ReportDetailDataModel
# from db.models.project import ProjectDataModel
from logging.config import fileConfig

# from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from db.setting.setting import Base, ENGINE
from db.models.user import Base as UserBase
from db.models.report import Base as ReportBase
from db.models.report_detail import Base as ReportDetailBase
from db.models.project import Base as ProjectBase


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# ProjectDataModel()
# ReportDetailDataModel()
# UserDataModel()
# ReportDataModel()
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata  # [UserBase.metadata, ReportBase.metadata,
# ProjectBase.metadata, ReportDetailBase.metadata]

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = config.get_main_option("sqlalchemy.url")
    connectable = ENGINE
    with connectable.connect() as connection:
        context.configure(
            url=url, connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
