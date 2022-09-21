killall -9 kubectl
kubectl port-forward --namespace areg $(kubectl get po -n areg | grep portal-db | \awk '{print $1;}') 5432:5432 &
kubectl port-forward --namespace areg $(kubectl get po -n areg | grep accounts | \awk '{print $1;}') 8080:8080 &
kubectl port-forward --namespace areg $(kubectl get po -n areg | grep kafka | \awk '{print $1;}') 9092:9092 &
