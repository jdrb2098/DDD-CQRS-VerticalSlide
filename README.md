# 🧠 Asisya API — FullStack Technical Test

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

---

## 📘 Descripción General

**Asisya API** es una aplicación backend construida con **FastAPI** que implementa una arquitectura limpia basada en principios de:

- 🧱 **Clean Architecture**
- 🧩 **Domain-Driven Design (DDD)**
- ⚙️ **CQRS (Command Query Responsibility Segregation)**
- 🧭 **Vertical Slicing**
- 💬 **Mediator Pattern**

El proyecto está diseñado para ser **modular, escalable y fácilmente extensible**, siguiendo una organización por **features** (módulos verticales).

## 🎯 Objetivos

Exponer una API REST con operaciones CRUD para productos y categorías.

Permitir carga masiva eficiente (100.000+ productos).

Implementar seguridad JWT para endpoints críticos.

Aplicar principios de arquitectura limpia, DDD y CQRS.

Incorporar pruebas unitarias e integración.

Proveer contenedores Docker y un pipeline CI/CD básico.
---

## 🧰 Tecnologías Principales

| Componente | Tecnología |
|-------------|-------------|
| **Framework API** | FastAPI |
| **ORM / DB Layer** | SQLAlchemy + Alembic |
| **Base de datos** | PostgreSQL |
| **Mediator Pattern** | [`mediatr`](https://pypi.org/project/mediatr/) |
| **Validación de datos** | Pydantic v2 |
| **Autenticación** | JWT |
| **Infraestructura local** | Docker + Docker Compose |
| **Seeder / Inicialización** | Script Python (`seed_initial_data.py`) |

---

## 🏗️ Arquitectura

### 🧱 Clean Architecture

El proyecto sigue una separación clara de capas:

| Capa | Descripción |
|------|--------------|
| **Domain** | Entidades del dominio y lógica de negocio pura. |
| **Core** | Configuración global, conexión DB, base repository. |
| **Features** | Casos de uso por módulo, agrupando Commands/Queries/Controllers. |
| **Infrastructure** | Implementaciones técnicas: ORM, migraciones, almacenamiento, seeds. |
| **Crosscutting** | Utilidades transversales: logging, autorización, notificaciones. |

---

### 🧩 Vertical Slicing + CQRS

Cada **feature** contiene sus comandos, queries, modelos y controlador propios.  
Esto permite mantener independencia total entre módulos.

Ejemplo: Módulo de Categorías

```bash
features/
├── categories/
│ ├── commands/
│ │ ├── create_category_command.py
│ │ ├── update_category_command.py
│ │ └── delete_category_command.py
│ ├── queries/
│ │ ├── get_all_categories_query.py
│ │ └── get_category_by_id_query.py
│ ├── repository.py
│ ├── models.py
│ └── controller.py

```

**Beneficios:**
- Modularidad completa  
- Separación de responsabilidades (lectura/escritura)  
- Facilidad para testing e incorporación de nuevas features

---

### ⚙️ Mediator Pattern

El patrón **Mediator** (implementado con [`mediatr`](https://pypi.org/project/mediatr/)) desacopla la capa de presentación de los casos de uso (controladores):

```python
from mediatr import Mediator

query = GetAllCategoriesQuery()
result = await Mediator.send_async(query)
## Cada caso de uso define su Handler con la lógica correspondiente:
@Mediator.handler
class GetAllCategoriesQueryHandler:
    def handle(self, query: GetAllCategoriesQuery):
        return self.category_repository.get_all()
```
🗂️ Estructura del Proyecto
.
```bash
.
├── core/
│   ├── base_repository.py
│   ├── config.py
│   ├── constants.py
│   └── database.py
├── crosscutting/
│   ├── authorization.py
│   ├── logging.py
│   └── notification_service.py
├── domain/
│   ├── category.py
│   ├── product.py
│   ├── role.py
│   └── user.py
├── features/
│   ├── admin/
│   ├── auth/
│   ├── categories/
│   ├── products/
│   └── user/
├── infrastructure/
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── alembic.ini
│   ├── seeds/
│   │   └── seed_initial_data.py
│   ├── storage_service.py
│   └── email_service.py
├── main.py
└── media/
    └── categories/
```
### 🧪 Pruebas
El proyecto incluye:

- Pruebas unitarias: para casos de uso y repositorios.

- Pruebas de integración: verifican endpoints y flujos reales.

- Mocks: para servicios externos (DB, storage, email, etc.).

### 🔐 Seguridad

- JWT Authentication implementada en crosscutting/authorization.py.
- Protección de endpoints mediante dependencias de seguridad en FastAPI.
- Tokens se almacenan en localStorage del frontend.

### 🚀 Escalabilidad y Performance

- Carga masiva con procesamiento asíncrono (/products/bulk).
- Lambdas AWS (LocalStack) para procesar colas de productos.
- Batch inserts para optimizar escritura masiva.

### Despliegue Local con Docker
1️⃣ Configurar variables de entorno
```bash
Crea un archivo .env basado en .env.example.
```
#### Construir y levantar contenedores

```bash
docker-compose up --build
```

### Servicios Disponibles

| Servicio       | Puerto | Descripción                            |
| -------------- | ------ | -------------------------------------- |
| **db**         | `5433` | Base de datos PostgreSQL (`asisya_db`) |
| **localstack** | `4566` | Emulador de AWS (SQS y Lambda)         |
| **asisya_api** | `8000` | Backend FastAPI (API principal)        |
| **frontend**   | `3000` | Aplicación React SPA                   |


## ☁️ Despliegue Cloud con AWS (Infraestructura + API + Frontend)
El proyecto está preparado para desplegarse automáticamente en un entorno AWS completamente gestionado utilizando GitHub Actions, AWS SAM (Serverless Application Model) y CloudFormation.

Este proceso crea todos los recursos necesarios para ejecutar la aplicación de manera segura, escalable y reproducible.

### 🧱 Recursos creados en AWS
Durante la ejecución del pipeline, se despliegan y configuran los siguientes componentes:


| Recurso              | Tipo AWS                    | Descripción                                                         |
| -------------------- | --------------------------- | ------------------------------------------------------------------- |
| **IAM Role**         | `AWS::IAM::Role`            | Rol con permisos para Lambda, EC2, RDS, S3 y SQS.                   |
| **S3 Bucket**        | `AWS::S3::Bucket`           | Almacenamiento de archivos y artefactos de despliegue.              |
| **SQS Queue**        | `AWS::SQS::Queue`           | Cola de mensajes para procesamiento masivo (`bulk-products-queue`). |
| **RDS (PostgreSQL)** | `AWS::RDS::DBInstance`      | Base de datos relacional usada por el backend.                      |
| **Lambda Functions** | `AWS::Serverless::Function` | Procesos asíncronos y tareas automáticas.                           |
| **EC2 Instance**     | `AWS::EC2::Instance`        | Servidor que aloja el backend (FastAPI) y frontend (React).         |
| **ECR Repository**   | `AWS::ECR::Repository`      | Repositorio para almacenar la imagen Docker de la API.              |

Todos estos recursos se gestionan como una pila (stack) de CloudFormation, lo que permite repetir o actualizar el despliegue fácilmente.

### ⚙️ Pipeline de Despliegue (GitHub Actions)

El flujo CI/CD está definido en .github/workflows/deploy.yml y automatiza la creación de la infraestructura y el despliegue de la aplicación.

#### 🔁 Flujo de ejecución

- Push o ejecución manual (workflow_dispatch) activa el pipeline.

- Se configura el entorno AWS usando credenciales seguras (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).

- Se instala y ejecuta AWS SAM para construir y empaquetar el template (template.yaml).

- Se despliega la infraestructura con CloudFormation, incluyendo IAM, S3, SQS, RDS y EC2.

- Se construye la imagen Docker de la API y se sube al repositorio ECR.

- Finalmente, se conecta a la instancia EC2 para ejecutar el contenedor con FastAPI y React.

