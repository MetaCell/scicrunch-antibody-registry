#!/bin/bash

fastapi-codegen --input openapi.yaml --output app -t templates && mv app/main.py ../backend/ && mv app/models.py ../backend/openapi/
rm -rf app

rm -rf ../frontend/src/rest
# npm install -g @openapitools/openapi-generator-cli
openapi-generator-cli generate -i ./openapi.yaml -g typescript-axios -o ../frontend/src/rest --type-mappings Date=string

echo Generated new models and main.py
