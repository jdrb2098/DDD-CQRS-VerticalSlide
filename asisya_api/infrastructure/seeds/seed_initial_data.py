# scripts/seed_initial_data.py
"""
Script idempotente para insertar datos iniciales:
 - usuario admin (usando UserRepository)
 - categorías iniciales
 - productos de ejemplo asociados al admin

Ejecución: PYTHONPATH=. python scripts/seed_initial_data.py
(asegúrate de haber corrido 'alembic upgrade head' antes)
"""

from decimal import Decimal

from asisya_api.core.config import settings
from asisya_api.core.database import SessionLocal, pwd_context
from asisya_api.domain.category import CategoryEntity
from asisya_api.domain.product import ProductEntity
from asisya_api.domain.role import Role
from asisya_api.domain.user import UserEntity
from asisya_api.features.user.repository import UserRepository


def run():
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)

        # --- admin ---
        admin = user_repo.get_by_username(settings.initial_admin_username)
        if not admin:
            print(f"[seed] creando usuario admin '{settings.initial_admin_username}'")
            admin_user = UserEntity(
                username=settings.initial_admin_username,
                email=settings.initial_admin_email,
                full_name="API Admin",
                hashed_password=pwd_context.hash(settings.initial_admin_password),
                disabled=False,
            )

            # Intenta usar el método set_roles tal como lo tienes implementado.
            try:
                admin_user.set_roles([Role.ADMIN, Role.USER])
            except Exception:
                # Si tu repo maneja RoleEntity relacional, UserRepository.create
                # debería encargarse de asociar roles. Dejamos pasar.
                pass

            user_repo.create(admin_user)
            admin = user_repo.get_by_username(settings.initial_admin_username)
            print("[seed] admin creado.")
        else:
            print("[seed] admin ya existe, omitiendo creación.")

        # --- categorías ---
        default_categories = [
            {"name": "SERVIDORES", "slug": "servidores", "description": "Categoría de servidores"},
            {"name": "CLOUD", "slug": "cloud", "description": "Servicios cloud"},
        ]

        created_categories = {}
        for cat in default_categories:
            exists = db.query(CategoryEntity).filter(CategoryEntity.slug == cat["slug"]).first()
            if not exists:
                new_cat = CategoryEntity(
                    name=cat["name"],
                    slug=cat["slug"],
                    description=cat["description"],
                    picture_path=None,
                )
                db.add(new_cat)
                db.commit()
                db.refresh(new_cat)
                created_categories[cat["slug"]] = new_cat
                print(f"[seed] categoría '{cat['slug']}' creada.")
            else:
                created_categories[cat["slug"]] = exists
                print(f"[seed] categoría '{cat['slug']}' ya existe.")

        # --- productos de ejemplo ---
        # Solo crear si no hay productos (evita duplicar)
        has_products = db.query(ProductEntity).first()
        if not has_products:
            print("[seed] creando productos de ejemplo...")
            cat_servidores = created_categories.get("servidores")
            cat_cloud = created_categories.get("cloud")
            sample_products = [
                {
                    "name": "Servidor X100",
                    "sku": "SRV-X100",
                    "description": "Servidor de ejemplo X100",
                    "price": Decimal("1999.90"),
                    "quantity_per_unit": "1 unidad",
                    "units_in_stock": 10,
                    "units_on_order": 0,
                    "discontinued": False,
                    "available": True,
                    "category_id": cat_servidores.id if cat_servidores else None,
                },
                {
                    "name": "Plan Cloud Básico",
                    "sku": "CLOUD-BASIC",
                    "description": "Plan cloud básico",
                    "price": Decimal("29.99"),
                    "quantity_per_unit": "1 mes",
                    "units_in_stock": 9999,
                    "units_on_order": 0,
                    "discontinued": False,
                    "available": True,
                    "category_id": cat_cloud.id if cat_cloud else None,
                },
            ]
            for sp in sample_products:
                p = ProductEntity(
                    name=sp["name"],
                    sku=sp["sku"],
                    description=sp["description"],
                    price=sp["price"],
                    quantity_per_unit=sp["quantity_per_unit"],
                    units_in_stock=sp["units_in_stock"],
                    units_on_order=sp["units_on_order"],
                    discontinued=sp["discontinued"],
                    available=sp["available"],
                    category_id=sp["category_id"],
                    created_by_user_id=admin.id if admin else None,
                )
                db.add(p)
            db.commit()
            print("[seed] productos creados.")
        else:
            print("[seed] ya existen productos, omitiendo creación.")

    except Exception as e:
        print("[seed] error durante seed:", e)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()
