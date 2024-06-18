rm /opt/cloudharness/resources/auth/api_user_password
rm /opt/cloudharness/resources/secrets/scicrunch-api-key

kubectl -n areg get secrets accounts -o yaml|grep api_user_password|cut -d " " -f 4|base64 -d > /opt/cloudharness/resources/auth/api_user_password
kubectl -n areg get secrets scicrunch-api-key -o yaml|grep scicrunch-api-key|cut -d " " -f 4|base64 -d > /opt/cloudharness/resources/secrets/scicrunch-api-key

cp deployment/helm/values.yaml /opt/cloudharness/resources/allvalues.yaml

