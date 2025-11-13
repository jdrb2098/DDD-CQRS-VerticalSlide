#!/bin/bash
set -e

echo "🔧 Creando cola SQS..."
awslocal sqs create-queue --queue-name bulk-products-queue

echo "✅ Recursos creados correctamente"
