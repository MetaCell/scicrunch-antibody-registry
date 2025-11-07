FROM quay.io/keycloak/keycloak:26.4.0

EXPOSE 9000
EXPOSE 8080
USER root
COPY --chmod=0755 scripts/create_api_user.sh /opt/keycloak/startup-scripts/create_api_user.sh
COPY --chmod=0755 scripts/kc-entrypoint.sh /opt/keycloak/bin/kc-entrypoint.sh

USER keycloak

# Customize keycloak look
COPY themes/custom /opt/keycloak/themes/custom
COPY plugins/* /opt/keycloak/standalone/deployments/
ENTRYPOINT [ "/opt/keycloak/bin/kc-entrypoint.sh" ]
CMD [ "start", "--import-realm", "--health-enabled=true", "--http-enabled=true", "--hostname-strict=false", "--metrics-enabled=true" ]
