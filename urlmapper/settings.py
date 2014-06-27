from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


_DEFAULT_URLMAPPER_ALLOWED_MAPPINGS = ['url', 'object', 'view_name']

URLMAPPER_RAISE_EXCEPTION = getattr(settings, 'URLMAPPER_RAISE_EXCEPTION', True)

URLMAPPER_KEYS = getattr(settings, 'URLMAPPER_KEYS', [])

URLMAPPER_FUNCTIONS = getattr(settings, 'URLMAPPER_FUNCTIONS', {})

URLMAPPER_CONTENTTYPES = getattr(settings, 'URLMAPPER_CONTENTTYPES', [])

URLMAPPER_ALLOWED_MAPPINGS = getattr(
    settings,
    'URLMAPPER_ALLOWED_MAPPINGS',
    _DEFAULT_URLMAPPER_ALLOWED_MAPPINGS
)


# Sanity check the settings

try:
    assert set(URLMAPPER_FUNCTIONS.keys()) <= set(URLMAPPER_KEYS)
except AssertionError:
    raise ImproperlyConfigured(
        "The following mapped functions have no valid corresponding key: {mismatches}".format(
            mismatches=list(set(URLMAPPER_FUNCTIONS.keys()) - set(URLMAPPER_KEYS))
        )
    )

try:
    assert URLMAPPER_ALLOWED_MAPPINGS
    assert set(URLMAPPER_ALLOWED_MAPPINGS) <= set(_DEFAULT_URLMAPPER_ALLOWED_MAPPINGS)
except AssertionError:
    raise ImproperlyConfigured(
        "Allowed mappings must be a non-empty subset of {mappings}".format(
            mappings=_DEFAULT_URLMAPPER_ALLOWED_MAPPINGS
        )
    )
