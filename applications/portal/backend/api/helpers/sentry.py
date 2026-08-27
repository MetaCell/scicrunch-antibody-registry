import sentry_sdk
from cloudharness.applications import get_current_configuration

from sentry_sdk.integrations.django import DjangoIntegration
import re
from cloudharness import log


def should_ignore_event(event, hint, ignore_errors, ignore_message_substrings):
    exc_info = hint.get("exc_info")
    exc_type = exc_info[0] if exc_info else None

    # Type-only match - only safe for single-cause exceptions (e.g. kafka.errors.NoBrokersAvailable).
    if exc_type is not None and ignore_errors:
        names = {exc_type.__name__, f"{exc_type.__module__}.{exc_type.__name__}"}
        if names & set(ignore_errors):
            return True

    # Message match - for exception text, or a bare log.error() call with no exception at all.
    if ignore_message_substrings:
        if exc_type is not None:
            message = str(exc_info[1])
        else:
            message = event.get("logentry", {}).get("message") or event.get("message") or ""
        if any(substring in message for substring in ignore_message_substrings):
            return True

    return False


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

        # Left unset in values-prod.yaml/the base config: infra flakiness is
        # low-value noise in dev/stage, but a real signal in prod.
        ignore_errors = sentry_cfg.get("ignore_errors", [])
        ignore_message_substrings = sentry_cfg.get("ignore_log_message_substrings", [])

        def _before_send(event, hint):
            if should_ignore_event(event, hint, ignore_errors, ignore_message_substrings):
                return None
            return event

        sentry_sdk.init(
            dsn=sentry_cfg.get("dsn", None),
            integrations=[DjangoIntegration()],
            send_default_pii=True,
            sample_rate=sentry_cfg.get("sample_rate", 1.0),
            traces_sampler=traces_sampler,
            before_send=_before_send,
            environment=CloudharnessConfig.get_domain()

        )
    except Exception as e:
        log.error("Sentry initialization failed %s", str(e))
