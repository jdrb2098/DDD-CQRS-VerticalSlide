import os
import json
import time
import boto3
import logging
from decimal import Decimal
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from asisya_api.core.database import SessionLocal
# Importa desde tu proyecto
from asisya_api.domain.product import ProductEntity
from asisya_api.features.products.repository import ProductRepository
 # ✅ usa tu configuración centralizada

# -------------------------------
# Configuración de logging simple
# -------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# Configuración de SQS
# -------------------------------
sqs_client = boto3.client(
    "sqs",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
)

QUEUE_URL = os.getenv(
    "BULK_PRODUCTS_QUEUE_URL",
    "http://sqs.us-west-2.localhost.localstack.cloud:4566/000000000000/bulk-products-queue"
)

# -------------------------------
# Alias de campos
# -------------------------------
FIELD_ALIASES = {
    "stock": "units_in_stock",
    "qty": "units_in_stock",
    "quantity": "units_in_stock",
    "price_value": "price",
}

# Campos válidos según la tabla
ALLOWED_FIELDS = {
    "name", "sku", "description", "price", "units_in_stock",
    "discontinued", "available", "quantity_per_unit", "units_on_order", "category_id"
}


# -------------------------------
# Lambda handler
# -------------------------------
def lambda_handler(event, context):
    repo = ProductRepository.instance()  # ✅ instancia singleton con sesión interna

    try:
        records = event.get("Records", [])
        for record in records:
            message = json.loads(record["Body"])
            user_id = message.get("user_id")
            products = message.get("products", [])

            logger.info(f"Procesando {len(products)} productos del usuario {user_id}")

            product_entities = []
            for p in products:
                try:
                    normalized = {FIELD_ALIASES.get(k, k): v for k, v in p.items()}
                    sku = normalized.get("sku") or f"{normalized['name'].lower().replace(' ', '-')}-{user_id}"
                    normalized["sku"] = sku

                    if "price" in normalized:
                        normalized["price"] = Decimal(str(normalized["price"]))
                    if "units_in_stock" in normalized:
                        normalized["units_in_stock"] = int(normalized["units_in_stock"])

                    product_data = {k: v for k, v in normalized.items() if k in ALLOWED_FIELDS}
                    product_data.setdefault("discontinued", False)
                    product_data.setdefault("available", True)
                    product_data.setdefault("quantity_per_unit", None)
                    product_data.setdefault("units_on_order", 0)
                    product_data.setdefault("units_in_stock", 0)
                    product_data.setdefault("category_id", normalized.get("category_id"))
                    product_data["created_by_user_id"] = user_id
                    product_data["created_at"] = datetime.utcnow()
                    product_data["updated_at"] = datetime.utcnow()

                    product_entities.append(ProductEntity(**product_data))

                except Exception as ex:
                    logger.error(f"❌ Error normalizando producto {p.get('name')}: {str(ex)}", exc_info=True)
                    continue

            if product_entities:
                try:
                    repo.bulk_create(product_entities)
                    logger.info(f"✅ Batch insertado: {len(product_entities)} productos")
                except ValueError as e:
                    logger.warning(f"⚠️ Error en bulk_create: {str(e)}")
                    continue

    except Exception as e:
        logger.exception(f"❌ Error procesando batch: {str(e)}")



# -------------------------------
# Poller local (para probar con LocalStack)
# -------------------------------
if __name__ == "__main__":
    logger.info("🚀 Iniciando poller local de SQS...")
    while True:
        resp = sqs_client.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5
        )
        messages = resp.get("Messages", [])
        for msg in messages:
            lambda_handler({"Records": [msg]}, None)
            sqs_client.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"]
            )
        time.sleep(1)
