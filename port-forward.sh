killall -9 kubectl
kubectl port-forward --namespace areg $(kubectl get po -n areg --field-selector=status.phase==Running | grep portal-db | \awk '{print $1;}') 5432:5432 &
kubectl port-forward --namespace areg deployment/accounts 8080:8080 &
kubectl port-forward --namespace areg $(kubectl get po -n areg | grep kafka | \awk '{print $1;}') 9092:9092 &
