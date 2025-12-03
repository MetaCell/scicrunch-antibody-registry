BACKUP_FILE=full_backup_postgres.psql
NAMESPACE="${1:-areg}"
echo "🔎 Using namespace: $NAMESPACE"
gcloud config set project metacell-stg
gcloud container clusters get-credentials  metacell-dmo  --zone=us-central1-c

kubectl exec -n $NAMESPACE deployment/keycloak-postgres -- pg_dump -d auth_db -U postgres -F c > kc-$BACKUP_FILE
kubectl exec -n $NAMESPACE deployment/portal-db -- pg_dump -d cloudharness -U mnp -F c > ar-$BACKUP_FILE
NG_POD=areg-85d4c689bf-m25td
kubectl -n $NAMESPACE cp $NAMESPACE/$NG_POD:persistent ./files-backup/persistent 
gcloud config set project metacellllc
gcloud container clusters get-credentials  mnp-cluster-production --zone=us-central1-a


kubectl scale deployment accounts --replicas=0 -n $NAMESPACE
bash clear_keycloak_pvc.sh keycloak-postgres $NAMESPACE


## Drop and recreate the public schema
kubectl exec -i -n $NAMESPACE deployment/keycloak-postgres -- psql -U user -d auth_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
kubectl exec -i -n $NAMESPACE deployment/portal-db -- pg_restore --if-exists --no-owner --clean   -d cloudharness -U mnp < ar-$BACKUP_FILE
kubectl exec -i -n $NAMESPACE deployment/keycloak-postgres -- pg_restore --if-exists --no-owner --clean -d auth_db -U user < kc-$BACKUP_FILE
kubectl -n $NAMESPACE cp ./files-backup/persistent $NAMESPACE/$NG_POD:.  
kubectl scale deployment accounts --replicas=1 -n $NAMESPACE