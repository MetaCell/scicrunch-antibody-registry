# portal

FastAPI/Django/React-based web application.
This application is constructed to be deployed inside a cloud-harness Kubernetes.
It can be also run locally for development and test purpose.

The code is generated with the script `harness-application` and is in part automatically generated 
from [openapi definition](./api/openapi.yaml).

## Configuration

### Accounts

The CloudHarness Django application template comes with a configuration that can retrieve user account updates from Keycloak (accounts)
To enable this feature:
* log in into the accounts admin interface
* select in the left sidebar Events
* select the `Config` tab
* enable "metacell-admin-event-listener" under the `Events Config` - `Event Listeners`

An other option is to enable the "metacell-admin-event-listener" through customizing the Keycloak realm.json from the CloudHarness repository.

## Develop

This application is composed of a FastAPI Django backend and a React frontend.

### Backend

Backend code is inside the *backend* directory.
See [here](backend/README.md#Develop)

### Frontend

Frontend code is inside the *frontend* directory.

Frontend is by default generated as a React web application, but no constraint about this specific technology.

#### Call the backend apis
All the api stubs are automatically generated in the [frontend/rest](frontend/rest) directory by `harness-application`
and `harness-generate`.

#### Update the backend apis from openapi.yaml
THe backend openapi models and main.py can be updated using the `genapi.sh` from the api folder.

## Local build & run
Create a Django local superuser account, this you only need to do on initial setup
```bash
cd backend
python3 manage.py migrate # to sync the database with the Django models
python3 manage.py collectstatic --noinput # to copy all assets to the static folder
python3 manage.py createsuperuser
# link the frontend dist to the django static folder, this is only needed once, frontend updates will automatically be applied
cd static/www
ln -s ../../../frontend/dist dist
```


Compile the frontend
```bash
cd frontend
npm install
npm run build
```


sync the Django models with the database and collect all other assets
```bash
cd ../backend
python3 manage.py migrate # to sync the database with the Django models
python3 manage.py collectstatic --noinput # to copy all assets to the static folder
```

start the FastAPI server
```bash
uvicorn --workers 2 --host 0.0.0.0 --port 8000 main:app
```

On Visual Studio Code, can use the following run configuration:

```json
{
      "args": [
        "--host",
        "0.0.0.0",
        "--port", "8000",
        "main:app"
      ],
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/applications/portal/backend",
      "justMyCode": false,
      "name": "Backend",
      "module": "uvicorn",
      "request": "launch",
      "type": "python",
      "env": {
        "CH_CURRENT_APP_NAME": "portal",
        "CH_VALUES_PATH": "${workspaceFolder}/deployment/helm/values.yaml",
        "KUBERNETES_SERVICE_HOST": "localhost"
      }
    },
```


### Running local with port forwardings to a kubernetes cluster
When you create port forwards to microservices in your k8s cluster you want to forced your local backend server to initialize
the AuthService and EventService services.
This can be done by setting the `KUBERNETES_SERVICE_HOST` environment variable to a dummy or correct k8s service host.
The `KUBERNETES_SERVICE_HOST` switch will activate the creation of the keycloak client and client roles of this microservice.

## Integration tests

The base command to run tests is `python manage.py test`.

To run tests locally you need to add configure environmental variables to get the 
correct configuration and a working configure instance of the postgres database running.

If you already have a deployment with the database, first forward it:

```
kubectl port-forward --namespace areg $(kubectl get po -n areg --field-selector=status.phase==Running | grep portal-db | \awk '{print $1;}') 5432:5432
```
And then add the following entry to your hosts file

```
127.0.0.1     portal-db.areg  portal-db
```


Visual Studio code configuration to run tests:
```json
 {
      "args": [
        "test"
      ],
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/applications/portal/backend",
      "justMyCode": false,
      "name": "Test",
      "program": "manage.py",
      "request": "launch",
      "type": "python",
      "env": {
        "CH_CURRENT_APP_NAME": "portal",
        "CH_VALUES_PATH": "${workspaceFolder}/deployment/helm/values.yaml",

      },
      
}

```