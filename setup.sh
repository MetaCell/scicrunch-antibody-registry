#!/bin/bash

# Setup script for creating a minikube instance and build the needed applications

minikube start --profile areg --memory 12000 --cpus 4 --disk-size 60g --driver=docker

minikube --profile areg addons enable ingress
minikube --profile areg addons enable metrics-server


kubectl config use-context areg
kubectl create ns areg

kubectl config use-context areg
kubectl create rolebinding areg-admin-default --clusterrole=admin --serviceaccount=areg:default -n areg

eval $(minikube --profile areg docker-env)
kubectl config use-context areg
harness-deployment cloud-harness . -l -d areg.local -dtls -n areg -e dev -i portal -u

kubectl config use-context areg
# skaffold dev --cleanup=false
skaffold run

echo To activate the minikube cluster please execute: eval \$\(minikube docker-env\)
