#!/usr/bin/env bash

OPENAPI_JSON="openapi.json"
OPENAPI_YAML="openapi.yaml"
OPENAPI_JSON_PATH="api/${OPENAPI_JSON}"

# Trick to have folder relative to the script, not CWD
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "${PARENT_PATH}"

ls api

function json2yaml {
  python -c 'import sys, yaml, json; print(yaml.dump(json.loads(sys.stdin.read())))'
}

# Generates the openAPI specification
(cd backend && DJANGO_EXTRA_APPS="ninja" python manage.py export_openapi_schema --api neuroglass_research.api.api --output $PARENT_PATH/$OPENAPI_JSON_PATH --indent 2)

cd "${PARENT_PATH}"

cat $PARENT_PATH/$OPENAPI_JSON_PATH | json2yaml > ${PARENT_PATH}/api/"${OPENAPI_YAML}"

# Generates the typescript API binding
(cd frontend && yarn generate-client)
