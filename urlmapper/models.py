from django.contrib.contenttypes.generic import GenericForeignKey
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, resolve, NoReverseMatch, Resolver404
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

import settings


def _get_key_choices():
    """
    Return all the keys that are not mapped to functions, as a list of choices.
    """
    keys = list(
        set(settings.URLMAPPER_KEYS) - set(settings.URLMAPPER_FUNCTIONS.keys())
    )
    if not keys:
        return [('', ugettext("There are no defined keys"))]
    return zip(keys, keys)


def _get_content_type_choices():
    """
    Return all the content types that can be mapped.
    """
    filters = models.Q()
    for app_label, model in settings.URLMAPPER_CONTENTTYPES:
        filters |= models.Q(app_label=app_label, model=model)
    # Always exclude this app
    filters &= ~models.Q(app_label='urlmapper')
    return filters


class URLMapVisibleMananger(models.Manager):

    def get_queryset(self):
        queryset = super(URLMapVisibleMananger, self).get_queryset()
        return queryset.exclude(key__in=settings.URLMAPPER_FUNCTIONS.keys())


class URLMap(models.Model):
    """
    Map a key to a URL in the database. This could be a straight-up URL, an
    object that has a get_absolute_url method, or a view name and keyword args.
    """
    key = models.CharField(
        _("Key"),
        max_length=64,
        unique=True,
        choices=_get_key_choices()
    )

    # Map to a URL
    url = models.CharField(
        _("URL"),
        max_length=255,
        help_text=_("Enter a relative URL"),
        blank=True
    )

    # Map to an object
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        verbose_name=_("Content Type"),
        limit_choices_to=_get_content_type_choices(),
        blank=True,
        null=True
    )
    object_id = models.PositiveIntegerField(
        _("Object ID"),
        null=True,
        blank=True
    )
    content_object = GenericForeignKey()

    # Map to a view
    view_name = models.CharField(
        _("View name"),
        max_length=255,
        blank=True
    )
    view_keywords = models.TextField(
        _("View keywords"),
        help_text=_(
            "Use a=b to define keywords and commas to separate e.g "
            "slug=terms-and-conditions, language=en"
        ),
        blank=True
    )

    objects = URLMapVisibleMananger()
    _objects = models.Manager()

    def __unicode__(self):
        return u"{key} --> {url}".format(
            key=self.key,
            url=self.get_url()
        )

    def _get_view_kwargs(self, raise_exception=True):
        if not self.view_keywords:
            return {}
        try:
            return {
                keyword.split('=')[0].strip(): keyword.split('=')[1].strip()
                for keyword in self.view_keywords.split(',')
                if keyword
            }
        except Exception as e:
            if raise_exception:
                raise e
            return {}

    def _get_view_url(self, raise_exception=True):
        try:
            return reverse(
                self.view_name,
                kwargs=self._get_view_kwargs(raise_exception=False)
            )
        except NoReverseMatch as e:
            if raise_exception:
                raise e
            return ''

    def _validate_url(self):
        if self.url:
            try:
                resolve(self.url)
            except Resolver404:
                raise ValidationError(
                    ugettext(
                        "URL {url} does not correspond to a valid application view."
                    ).format(
                        url=self.url
                    )
                )

    def _validate_object(self):
        if self.content_type is not None or self.object_id is not None:
            if self.content_type is None or self.object_id is None:
                raise ValidationError(
                    ugettext(
                        "Please supply both a content type and object ID."
                    )
                )
            if not self.content_object:
                raise ValidationError(
                    ugettext(
                        "Object with type {type} and ID {id} does not exist"
                    ).format(
                        type=self.content_type,
                        id=self.object_id
                    )
                )
            if getattr(self.content_object, 'get_absolute_url', None) is None:
                raise ValidationError(
                    ugettext(
                        "Object with type {type} and ID {id} does not have a "
                        "get_absolute_url method."
                    ).format(
                        type=self.content_type,
                        id=self.object_id
                    )
                )

    def _validate_view(self):
        if self.view_keywords and not self.view_name:
            raise ValidationError(
                ugettext(
                    "View keywords supplied but no view name provided"
                )
            )
        try:
            kwargs = self._get_view_kwargs()
        except:
            raise ValidationError(
                ugettext(
                    "Keywords are not in the format a=b, c=d"
                )
            )
        if self.view_name:
            try:
                self._get_view_url()
            except NoReverseMatch:
                raise ValidationError(
                    ugettext(
                        "No match for view {view} and keyword arguments {kwargs}."
                    ).format(
                        view=self.view_name,
                        kwargs=kwargs
                    )
                )

    def _validate_single_mapping(self):
        num_supplied_values = sum(
            (
                bool(self.url),
                self.content_type is not None or self.object_id is not None,
                bool(self.view_name or self.view_keywords)
            )
        )
        if num_supplied_values != 1:
            raise ValidationError(
                ugettext(
                    "Please supply exactly one form of URL mapping ({n} supplied).".format(
                        n=num_supplied_values
                    )
                )
            )

    def clean_fields(self, exclude=None):
        super(URLMap, self).clean_fields(exclude=exclude)
        self._validate_single_mapping()
        self._validate_url()
        self._validate_object()
        self._validate_view()

    def get_url(self):
        if self.url:
            return self.url
        if self.content_object:
            return self.content_object.get_absolute_url()
        if self.view_name:
            return self._get_view_url(raise_exception=False)
        return ''
    get_url.short_description = _('URL')

    def mapping_type(self):
        if self.url:
            return _("Direct")
        if self.object_id:
            return _("Object")
        if self.view_name:
            return _("View")
    mapping_type.short_description = _("Mapping type")

    class Meta:
        verbose_name = _("URL map")
        verbose_name_plural = _("URL maps")
