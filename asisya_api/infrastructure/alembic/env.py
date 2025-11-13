# asisya_api/infrastructure/alembic/env.py
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ---------------------------------------------------------------------
# AGREGAR PROJECT ROOT al sys.path para poder importar `asisya_api`
# ---------------------------------------------------------------------
# env.py está en: <project_root>/asisya_api/infrastructure/alembic/env.py
# Subimos tres niveles para llegar a <project_root>
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Ahora podemos importar nuestro settings y Base
from asisya_api.core.config import settings
from asisya_api.core.database import Base

# IMPORTS DE MODELOS (side-effect: registran tablas en Base.metadata)
# Ajusta si alguno de estos módulos cambia de ruta
import asisya_api.domain.role  # noqa: F401
import asisya_api.domain.user  # noqa: F401
import asisya_api.domain.category  # noqa: F401
import asisya_api.domain.product  # noqa: F401

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# Sobrescribimos sqlalchemy.url con el que arma Settings (DB_* o DATABASE_URL)
config.set_main_option("sqlalchemy.url", settings.database_url)

# metadata target
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
