# OpenAPI generated server

## Overview
This server was generated by the [OpenAPI Generator](https://openapi-generator.tech) project. By using the
[OpenAPI-Spec](https://openapis.org) from a remote server, you can easily generate a server stub.  This
is an example of building a OpenAPI-enabled Django FastAPI server.

This example uses the [Django](https://www.djangoproject.com/) library on top of [FastAPI](https://fastapi.tiangolo.com/).

## Requirements
Python >= 3

Cloudharness libraries (check also dockerfile chain)

```
pip install -e cloud-harness/libraries/models
pip install -e cloud-harness/libraries/cloudharness-common
pip install -r cloud-harness/infrastructure/common-images/cloudharness-fastapi/libraries/fastapi/requirements.txt 
pip install -e cloud-harness/infrastructure/common-images/cloudharness-django/libraries/cloudharness-django
pip install -r applications/portal/backend/requirements.txt
pip install -e applications/portal/backend
```

## Local backend development
```
# store the accounts api admin password on the local disk

mkdir -p /opt/cloudharness/resources/auth/
kubectl -n areg get secrets accounts -o yaml|grep api_user_password|cut -d " " -f 4|base64 -d > /opt/cloudharness/resources/auth/api_user_password

# store the Scicrunch API_KEY on the local disk
mkdir -p /opt/cloudharness/resources/secrets/
kubectl -n areg get secrets scicrunch-api-key -o yaml|grep scicrunch-api-key|cut -d " " -f 4|base64 -d > /opt/cloudharness/resources/secrets/scicrunch-api-key


# Make the cloudharness application configuration available on your local machine
cp deployment/helm/values.yaml /opt/cloudharness/resources/allvalues.yaml
```

One typical development strategy is to run the server application locally connected to the services running in the 
cluster. To do so you would need to:
```
# Run setup.sh to deploy your applications to the (minikube) cluster
1. ./setup.sh
# Add the appropriate domains to your hosts file. It should include the domais outputted by the harness-deployment commands
and domains of the services you want to use (portal-db, BOOTSTRAP.areg.svc.cluster.local, kafka-0.broker.areg.svc.cluster.local f.e.).
With that out of the way you can simply run the 
port-forward.sh script
2. ./port-forward.sh
# The last crucial step is to properly set up the CH_CURRENT_APP_NAME to the ch application name (portal). This will
make the server know if it should connect to the remote database or to a local one.
With that you will be able to run any manage.py command locally (from runserver, to makemigrations, migrate or even ingest)
3. CH_CURRENT_APP_NAME=portal python manage.py <command>
```

### Update migrations

After changes to the model are made, migrations need to be updated

To do so, run:
```
python manage.py makemigrations
```

### Ingest
To run the ingestion:
```
python manage.py ingest <file-id>
```
Where the file-id is the Google Drive reference to the file (that you can retrieve from the shareable link)
If you already have the antibody_data folder (under portal/backend) the ingestion script won't download the data
again.