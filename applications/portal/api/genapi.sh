#!/bin/bash

fastapi-codegen --input openapi.yaml --output app -t templates && mv app/main.py ../backend/ && mv app/models.py ../backend/openapi/
rm -rf app

rm -rf ../frontend/src/rest
# npm install -g @openapitools/openapi-generator-cli
openapi-generator-cli generate -i ./openapi.yaml -g typescript-axios -o ../frontend/src/rest --type-mappings Date=string
rm -rf ../frontend/src/rest/.openapi-generator

openapi-generator-cli generate -i ../../accounts-api/api/openapi.yaml -g typescript-axios -o ../frontend/src/rest/accounts-api --type-mappings Date=string
rm -rf ../frontend/src/rest/accounts-api/.openapi-generator

echo Generated new models and main.py
