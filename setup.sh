#!/bin/bash

# Setup script for creating a minikube instance and build the needed applications

minikube start --memory 6000 --cpus 4 --disk-size 60g --kubernetes-version=v1.21.2 --driver=docker

minikube addons enable ingress
minikube addons enable metrics-server


kubectl config use-context minikube
kubectl create ns areg
kubectl create rolebinding areg-admin-default --clusterrole=admin --serviceaccount=areg:default -n areg

eval $(minikube docker-env)
kubectl config use-context minikube

harness-deployment cloud-harness . -l -d areg.local -dtls -n areg -e dev -i areg-portal

kubectl config use-context minikube

skaffold dev --cleanup=false
#skaffold build

echo To activate the minikube cluster please execute: eval \$\(minikube docker-env\)
