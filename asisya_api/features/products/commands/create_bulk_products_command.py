from mediatr import Mediator
from typing import List, Dict
import json
import boto3
import os
from asisya_api.crosscutting.logging import get_logger

logger = get_logger(__name__)


class CreateBulkProductsCommand:
    def __init__(self, products: List[Dict], user):
        """
        products: lista de diccionarios con los datos de cada producto
        user: usuario que hace la carga masiva
        """
        self.products = products
        self.user = user


@Mediator.handler
class CreateBulkProductsCommandHandler:
    def __init__(self):
        # Configurar cliente SQS apuntando a LocalStack o AWS real
        self.sqs_client = boto3.client(
            "sqs",
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION"),
        )
        self.queue_url = os.getenv("BULK_PRODUCTS_QUEUE_URL")

    def handle(self, request: CreateBulkProductsCommand):
        logger.info(f"User {request.user.id} encolando {len(request.products)} productos")

        batch_size = 100  # Cantidad de productos por mensaje
        total_messages = 0

        for i in range(0, len(request.products), batch_size):
            batch = request.products[i:i + batch_size]
            message_body = json.dumps({
                "user_id": request.user.id,
                "products": batch
            })

            self.sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body
            )

            total_messages += 1
            logger.debug(f"Lote de {len(batch)} productos encolado (mensaje {total_messages})")

        logger.info(f"{total_messages} mensajes enviados a SQS para {len(request.products)} productos")

        return {"message": f"{len(request.products)} productos encolados en {total_messages} mensajes"}
