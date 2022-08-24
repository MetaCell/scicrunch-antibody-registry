killall -9 kubectl
kubectl port-forward --namespace areg $(kubectl get po -n areg | grep areg-portal-db | \awk '{print $1;}') 5432:5432 &