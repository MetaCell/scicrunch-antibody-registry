# Antibody Registry

An updated version of the Antibody Registry platform

## Prerequisites

### Python

The deployment process is based on Python 3.9+ scripts. It is recommended to setup a virtual
environment first.

With conda:
```bash
conda create --name areg python=3.9
conda activate areg
```

### Setup CloudHarness

The Antibody Registry deployment is built on top of [CloudHarness](https://github.com/MetaCell/cloud-harness).

To setup CloudHarness:

```
git clone https://github.com/MetaCell/cloud-harness.git
sh cloud-harness/install.sh
```

### Install skaffold

skaffold is needed to build the images and run them on minikube.
Get it [here](https://skaffold.dev/docs/install/).

### Install helm

You can install helm from [here](https://helm.sh/docs/intro/install/).

## Development setup

A Kubernetes cluster, like Minikube or Docker Desktop, is required setup locally.
For more information, refer to the [CloudHarness documentation](https://github.com/MetaCell/cloud-harness/tree/develop/docs/build-deploy/local-deploy)

To setup the local deployment, run
```
harness-deployment cloud-harness . -l -d areg.local -dtls -n areg -e local -i areg-portal
``` 

With Visual Studio Code and the Cloud Code plugin installed, can run and the debug
with the auto-generated configuration *CloudHarness: Run/Debug*.

Can also run from the command line:

```
skaffold dev --cleanup=false
```

## Deploy

### Create deployment

CloudHarness scripts script automate the deployment process.

To manually create the helm chart update the ci/cd Codefresh scripts, run:

```
harness-deployment cloud-harness . -n areg -e dev -i areg-portal
harness-deployment cloud-harness . -n areg -e prod -i areg-portal
```
### Cluster setup

Kubernetes 1.22+ is supported (v1 spec)

#### Cert-manager
The cert-manager must be installed in order to use letsencrypt generated certificates

To check if cert-manager is installed, run:
```
kubectl get pods -n cert-manager
```
If cert manager is installed, the command will return 3 lines.

To install the cert manager on a new cluster, run:
```
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.15.1/cert-manager-legacy.yaml
```

See also https://cert-manager.io/docs/installation/kubernetes/.

#### CSI driver

On google cloud, the **Compute Engine persistent disk CSI Driver** must be enabled in order for the volume cloning to work.

### Install and upgrade with Helm

1. Create the namespace `kubectl create ns areg`
1. Run  `helm install areg deployment/helm  --namespace areg` to install.
1. Run `kubectl create rolebinding areg-admin-default --clusterrole=admin --serviceaccount=areg:default -n areg` to allow workflows to run on namespace areg

To upgrade an existing deployment, use:

```
helm upgrade areg deployment/helm --namespace areg --install --reset-values [--force]
```

## CoC

Antibody Registry adheres to the Contributor Covenant: https://www.contributor-covenant.org/

## Citing Antibody Registry in academic work

Please cite as The Antibody Registry (RRID:SCR_006397) https://antibodyregistry.org/