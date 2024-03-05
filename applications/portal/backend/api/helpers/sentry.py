import cloudharness.sentry as sentry
from cloudharness.applications import get_current_configuration
from sentry_sdk.integrations.django import DjangoIntegration
import re

def init_sentry():
    try:
        
        app_cfg = get_current_configuration()
        sentry_cfg = app_cfg.get("sentry", {})
        resources_extensions = set(["css", "js", "png", "jpg", "jpeg", "gif", "svg", "ico", "xml"])

        def traces_sampler(sampling_context):
            url = sampling_context['transaction_context'].get("name", "")

            if "/ready" in url or "/live" in url:
                return 0.0

            for pattern in sentry_cfg.get("traces_sample_rate_patterns", {}):
                if pattern in url or re.match(pattern, url):
                    return sentry_cfg.traces_sample_rate_patterns[pattern]

            extension = "." in url and url.split(".")[-1]
            if extension in resources_extensions:
                return sentry_cfg.get("traces_sample_rate_resources", 0.0)
            
            return sentry_cfg.get("traces_sample_rate", 1.0)

        sentry.init(
            integrations=[DjangoIntegration()],
            sample_rate=sentry_cfg.get("sample_rate", 1.0),
            traces_sampler=traces_sampler,
        )
    except Exception as e:
        log.exception("Sentry initialization failed")