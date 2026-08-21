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

### Backend dependencies

`REQUIRES` in [backend/setup.py](backend/setup.py) is the **single source of truth**.
[backend/requirements.txt](backend/requirements.txt) is compiled from it and must never be
edited by hand: it is a lockfile pinning the whole resolved tree (direct *and* transitive)
with SHA256 hashes, so an image built today installs exactly what was tested.

To add, remove or bump a dependency:

1. Edit `REQUIRES` in `backend/setup.py`.
2. Regenerate the lockfile from the `backend` directory:
   ```bash
   uv pip compile setup.py -o requirements.txt \
       --generate-hashes --universal --python-version 3.12
   ```
   `pip-compile` from [pip-tools](https://pip-tools.readthedocs.io/) accepts the same
   arguments apart from `--universal`.
3. Reinstall (`pip install -r requirements.txt && pip install -e .`) and run the tests.
4. Commit `setup.py` and `requirements.txt` together.

Notes:

* Direct dependencies are pinned exactly (`==`). The portal is a deployed application, not
  a redistributable library, so there is no reason to run against anything other than the
  versions it was tested with.
* `REQUIRES` also carries `>=` floors for a handful of packages the portal never imports
  itself, only to keep the resolver away from releases with known advisories. They are
  grouped and commented in `setup.py`; drop one once its parent requires a patched release
  on its own.
* Recompiling reuses the versions already pinned in `requirements.txt` wherever they still
  satisfy the constraints, so a bump stays a small diff instead of dragging every
  transitive forward. To deliberately move one, add
  `--upgrade-package <name>` (or `--upgrade` for all of them).
* Because the lockfile carries hashes, pip switches to `--require-hashes` automatically —
  no extra flags in the [Dockerfile](Dockerfile) or [dev-setup.sh](dev-setup.sh).
* To check the result for known vulnerabilities:
  ```bash
  pip-audit -r requirements.txt --no-deps
  ```
  Auditing the *environment* instead (plain `pip-audit`) also reports packages that come
  from the cloudharness base images — connexion/flask, fastapi, python-keycloak and their
  dependencies. Those are not portal's to fix; they belong to the
  [cloud-harness](../../cloud-harness) requirements files.

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