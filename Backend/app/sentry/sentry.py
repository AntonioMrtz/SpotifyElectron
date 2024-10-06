"""Sentry monitoring service"""

import sentry_sdk

from app.common.app_schema import AppEnvironmentMode


def init_sentry(environment: AppEnvironmentMode, sentry_dns: str | None) -> None:
    """Init Sentry monitoring service if PROD environment and dns provided

    Args:
        environment (AppEnvironmentMode): app environment
        sentry_dns (str): sentry dns connection
    """
    if environment == AppEnvironmentMode.PROD and sentry_dns:
        sentry_sdk.init(
            dsn=sentry_dns,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
