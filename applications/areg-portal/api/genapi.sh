#!/bin/bash

fastapi-codegen --input openapi.yaml --output app -t templates && mv app/main.py ../backend/ && mv app/models.py ../backend/openapi/
rm -rf app

rm -rf ../frontend/src/rest
java -jar ./openapi-generator-cli-5.4.0.jar generate -i ./openapi.yaml -g typescript-axios -o ../frontend/src/rest --type-mappings Date=string

echo Generated new models and main.py
