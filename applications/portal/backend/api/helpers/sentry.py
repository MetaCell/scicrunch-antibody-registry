import sentry_sdk
from cloudharness.applications import get_current_configuration

from sentry_sdk.integrations.django import DjangoIntegration
import re
from cloudharness import log


def init_sentry():
    try:
        from cloudharness.utils.config import CloudharnessConfig
        app_cfg = get_current_configuration()
        sentry_cfg = app_cfg.get("sentry", {})
        if not sentry_cfg:
            log.info("Sentry is not configured, skipping initialization.")
            return
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

        sentry_sdk.init(
            dsn=sentry_cfg.get("dsn", None),
            integrations=[DjangoIntegration()],
            send_default_pii=True,
            sample_rate=sentry_cfg.get("sample_rate", 1.0),
            traces_sampler=traces_sampler,
            environment=CloudharnessConfig.get_domain()

        )
    except Exception as e:
        log.error("Sentry initialization failed %s", str(e))
