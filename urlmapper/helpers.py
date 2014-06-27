from models import URLMap
import settings


def get_mapped_url(key, request=None):
    """
    Return the URL for a given key, or None if one does not exist.
    """
    if key not in settings.URLMAPPER_KEYS:
        if settings.URLMAPPER_RAISE_EXCEPTION:
            raise KeyError(
                "Key '{key}' does not exist in settings.URLMAPPER_KEYS".format(
                    key=key
                )
            )
        return ''

    if key in settings.URLMAPPER_FUNCTIONS:
        try:
            try:
                return settings.URLMAPPER_FUNCTIONS[key](request)
            except TypeError:
                return settings.URLMAPPER_FUNCTIONS[key]()
        except Exception, e:
            if settings.URLMAPPER_RAISE_EXCEPTION:
                raise e
            return ''

    try:
        return URLMap.objects.get(key=key).get_url()
    except URLMap.DoesNotExist:
        return ''


def check_mapped_url(key):
    """
    Check whether a URL is mapped.
    """
    return bool(
        key in settings.URLMAPPER_KEYS
        and (
            key in settings.URLMAPPER_FUNCTIONS
            or URLMap.objects.filter(key=key).exists()
        )
        and get_mapped_url(key)
    )
