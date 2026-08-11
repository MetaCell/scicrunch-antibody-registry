load('/home/user/ucsd-antibody-registry/cloud-harness/deployment-configuration/tilt-deploy.ext', 'deploy')
load('ext://uibutton', 'cmd_button')

config.define_bool('setup-infrastructure')
config.define_bool('watch')
cfg = config.parse()
setup_infrastructure = cfg.get('setup-infrastructure', False)
watch = cfg.get('watch', False)
if setup_infrastructure:
    # setup ingress
    print("Installing ingress controller")
    # local("cd infrastructure/cluster-configuration && source cluster-init.sh")
    local("kubectl get namespace ingress-nginx 2>/dev/null 1>/dev/null || bash -c 'helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace --version v4.2.5 --wait --wait-for-jobs'")
    # print("Let's wait a few seconds...")
    # local("sleep 30")
else:
    print("To setup the infrastructure (f.e. ingress controller)")
    print("run: tilt up -- --setup-infrastructure")

if not watch:
    print("To watch file changes, run: tilt up -- --watch")


# build images
docker_build(ref='areg/cloudharness-base', context='/home/user/ucsd-antibody-registry/cloud-harness', dockerfile='cloud-harness/infrastructure/base-images/cloudharness-base/Dockerfile', build_args={'DEBUG': 'true'})
docker_build(ref='areg/cloudharness-flask', context='/home/user/ucsd-antibody-registry/cloud-harness/infrastructure/common-images/cloudharness-flask', dockerfile='cloud-harness/infrastructure/common-images/cloudharness-flask/Dockerfile', build_args={'DEBUG': 'true', 'CLOUDHARNESS_BASE': 'areg/cloudharness-base'})
docker_build(ref='areg/cloudharness-django', context='/home/user/ucsd-antibody-registry/cloud-harness/infrastructure/common-images/cloudharness-django', dockerfile='cloud-harness/infrastructure/common-images/cloudharness-django/Dockerfile', build_args={'DEBUG': 'true', 'CLOUDHARNESS_BASE': 'areg/cloudharness-base'})
docker_build(ref='areg/accounts', context='/home/user/ucsd-antibody-registry/.overrides/applications/accounts', dockerfile='.overrides/applications/accounts/Dockerfile', build_args={'DEBUG': 'true'})
docker_build(ref='areg/accounts-api', context='/home/user/ucsd-antibody-registry/./applications/accounts-api', dockerfile='applications/accounts-api/Dockerfile', build_args={'DEBUG': 'true', 'CLOUDHARNESS_FLASK': 'areg/cloudharness-flask'})
docker_build(ref='areg/portal', context='/home/user/ucsd-antibody-registry/./applications/portal', dockerfile='applications/portal/Dockerfile', build_args={'DEBUG': 'true', 'CLOUDHARNESS_DJANGO': 'areg/cloudharness-django'})


extra_env = {}
extra_env.setdefault("accounts", [])
extra_env.setdefault("api.accounts", [])
extra_env.setdefault("www", [])


# deploy
deploy(name='areg', namespace='areg', extra_env=extra_env, watch=watch)

# Add Tilt ui elements for: accounts
k8s_resource(
    'accounts',
    links=[link('http://accounts.areg.dev.metacell.us', 'Open accounts page')]
)
cmd_button('accounts:set debug mode',
    argv=["sh", "-c", "kubectl -n areg patch deployment accounts --patch '{\"spec\": {\"template\": {\"spec\": {\"containers\": [{\"name\": \"accounts\", \"command\": [\"/bin/bash\"], \"args\": [\"-c\", \"sleep infinity\"], \"livenessProbe\": null, \"readinessProbe\": null}]}}}}'"],
    resource='accounts',
    icon_name='bug_report',
    text='set debug mode',
)
# Add Tilt ui elements for: api.accounts
k8s_resource(
    'accounts-api',
    links=[link('http://api.accounts.areg.dev.metacell.us', 'Open api.accounts page')]
)
cmd_button('accounts-api:set debug mode',
    argv=["sh", "-c", "kubectl -n areg patch deployment accounts-api --patch '{\"spec\": {\"template\": {\"spec\": {\"containers\": [{\"name\": \"accounts-api\", \"command\": [\"/bin/bash\"], \"args\": [\"-c\", \"sleep infinity\"], \"livenessProbe\": null, \"readinessProbe\": null}]}}}}'"],
    resource='accounts-api',
    icon_name='bug_report',
    text='set debug mode',
)
# Add Tilt ui elements for: www
k8s_resource(
    'portal',
    links=[link('http://www.areg.dev.metacell.us', 'Open www page')]
)
cmd_button('portal:set debug mode',
    argv=["sh", "-c", "kubectl -n areg patch deployment portal --patch '{\"spec\": {\"template\": {\"spec\": {\"containers\": [{\"name\": \"portal\", \"command\": [\"/bin/bash\"], \"args\": [\"-c\", \"sleep infinity\"], \"livenessProbe\": null, \"readinessProbe\": null}]}}}}'"],
    resource='portal',
    icon_name='bug_report',
    text='set debug mode',
)
