rm /opt/cloudharness/resources/auth/api_user_password
rm /opt/cloudharness/resources/secrets/SCICRUNCH_API_KEY

kubectl -n areg get secrets accounts -o yaml|grep api_user_password|cut -d " " -f 4|base64 -d > /opt/cloudharness/resources/auth/api_user_password
kubectl -n areg get secrets scicrunch-api-key -o yaml|grep SCICRUNCH_API_KEY|cut -d " " -f 4|base64 -d > /opt/cloudharness/resources/secrets/SCICRUNCH_API_KEY

cp deployment/helm/values.yaml /opt/cloudharness/resources/allvalues.yaml

