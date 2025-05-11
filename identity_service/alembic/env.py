from logging.config import fileConfig
import sys
from pathlib import Path


from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
# Add the project root to Python path
project_root = Path(__file__).resolve().parents[2]  # Goes up 3 levels to identity_service's parent
sys.path.append(str(project_root))

# Now import your modules
from identity_service.DB.database import SQLALCHEMY_DATABASE_URL, Base, TEST_SQLALCHEMY_DATABASE_URL
from identity_service.DB.models import users #--------------------> all tables




# this is the Alembic Config object, which providesZ
# access to the values within the .ini file in use.
config = context.config

database_urls = {
    "production": SQLALCHEMY_DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://"),
    "test": TEST_SQLALCHEMY_DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
}

def run_migrations_on_db(database_url, db_name):  #-------------------> add function to run the script for more times
    """Run migrations on a specific database."""
    print(f"Running migrations for {db_name} using the URL: {database_url}")
    
        # Set the URL for Alembic configuration
    config.set_main_option('sqlalchemy.url', database_url)


    # Interpret the config file for Python logging.
    # This line sets up loggers basically.
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    # add your model's MetaData object here
    # for 'autogenerate' support
    # from myapp import mymodel
    # target_metadata = mymodel.Base.metadata
    target_metadata = Base.metadata

    # other values from the config, defined by the needs of env.py,
    # can be acquired:
    # my_important_option = config.get_main_option("my_important_option")
    # ... etc.


    def run_migrations_offline() -> None:
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


    def run_migrations_online() -> None:
        """Run migrations in 'online' mode.

        In this scenario we need to create an Engine
        and associate a connection with the context.

        """
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:

            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                include_schemas=True  #----------------> add this
            )

            with context.begin_transaction():
                context.run_migrations()


    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()


def run_migrations(): #---------------------- Run migration in each DB alone!
    try:
        run_migrations_on_db(database_urls["production"], "production")
    except Exception as e:
        print(f"Migration for production failed: {e}")
    
    try:
        run_migrations_on_db(database_urls["test"], "test")
    except Exception as e:
        print(f"Migration for test failed: {e}")


run_migrations()
