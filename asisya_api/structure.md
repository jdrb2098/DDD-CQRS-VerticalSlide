.
├── core
│   ├── base_repository.py
│   ├── config.py
│   ├── constants.py
│   └── database.py
├── crosscutting
│   ├── authorization.py
│   ├── logging.py
│   └── notification_service.py
├── domain
│   ├── category.py
│   ├── __init__.py
│   ├── product.py
│   ├── role.py
│   └── user.py
├── .env
├── .env.example
├── features
│   ├── admin
│   │   ├── commands
│   │   │   ├── delete_user_command.py
│   │   │   └── enable_user_command.py
│   │   ├── controller.py
│   │   ├── __init__.py
│   │   └── queries
│   │       └── get_all_users_query.py
│   ├── auth
│   │   ├── auth_service.py
│   │   ├── controller.py
│   │   ├── __init__.py
│   │   └── models.py
│   ├── categories
│   │   ├── commands
│   │   │   ├── create_category_command.py
│   │   │   ├── delete_category_command.py
│   │   │   └── update_category_command.py
│   │   ├── controller.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── queries
│   │   │   ├── get_all_categories_query.py
│   │   │   └── get_category_by_id_query.py
│   │   └── repository.py
│   ├── products
│   │   ├── commands
│   │   │   ├── create_bulk_products_command.py
│   │   │   └── create_product_command.py
│   │   ├── controller.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── queries
│   │   │   └── get_products_query.py
│   │   └── repository.py
│   └── user
│       ├── commands
│       │   ├── signup_command.py
│       │   ├── update_user_command.py
│       │   └── validate_user_command.py
│       ├── constants.py
│       ├── controller.py
│       ├── __init__.py
│       ├── models.py
│       └── repository.py
├── infrastructure
│   ├── alembic
│   │   ├── env.py
│   │   ├── README
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── 24753577381d_init_schema.py
│   ├── alembic.ini
│   ├── alembic.ini.bak
│   ├── email_service.py
│   ├── external_api_service.py
│   ├── __init__.py
│   ├── lambdas
│   │   └── process_bulk_products
│   │       ├── handler.py
│   │       ├── __init__.py
│   │       └── requirements.txt
│   ├── seeds
│   │   ├── __init__.py
│   │   └── seed_initial_data.py
│   └── storage_service.py
├── __init__.py
├── main.py
├── .pytest_cache
│   ├── CACHEDIR.TAG
│   ├── .gitignore
│   ├── README.md
│   └── v
│       └── cache
│           └── nodeids
├── .structure.md
└── structure.md

25 directories, 70 files
