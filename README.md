Django URL Mapper
=================

###The problem

You need to provide a link in your template to something specific, such as a
terms and conditions page, but you don't know the primary key of the
page, or there are several versions of the page, all in a different language
with a different slug.

Or maybe there is a degree of variability in the way the URL is generated - a
switchable content app, for example.

Or it could just be that the page may or may not exist, and you need to know
whether to display the URL at all.

###The solution

Django URL mapper allows you to define a set of keys that you can use in your
template. Think of a URL name and keyword arguments rolled into one.

In the backend, these keys can be mapped to a function, view, object or plain old URL.

Using the {% mapped_url %} template tag, you can get the URL, provided it exists,
with no special knowledge of how the URL is obtained.

It is up to either a back-end developer (if using a function lookup) or a content
editor (if using a datbase lookup) to map that key to a URL on the site.

Installation
------------

Download django-url-mapper to your environment, add urlmapper to your
INSTALLED_APPS and run the migrations.

Basic Setup
-----------

The first step is defining the keys that the templates can use with the tag. This
is simply a list of strings defined in settings.

```python

URLMAPPER_KEYS = [
    'homepage',
    'terms-and-conditions'
]

```

At this point, you need do nothing more.

If you log into Django admin, you can map each of these keys to:

- a valid relative URL for the site
- an object
- a Django urlpattern

### Providing functional URL mappings

If you wish to delegate a mapping key to a function, then you can do this by
defining URLMAPPER_FUNCTIONS in settings.

This is a series of key/value pairs, with the value being a Python callable that
returns a string object.

You may optionally take a request object as an argument to your callable.

```python

def get_account_page_for_request(request):
    # Do something with request...
    return url

URLMAPPER_FUNCTIONS = {
    'account': get_account_page_for_request,
    'terms-and-conditions': lambda: '/terms-and-conditions/'
}

```

Any keys that are mapped in this way will not be visible in the Django admin.

See Advanced Settings for further customisation.

Usage
-----

### Template tags

Examples:

```html

{% load urlmapper_tags %}

{% if 'terms_and_conditions'|is_mapped_url %}
    <a href="{% mapped_url 'terms-and-conditions'%}">Terms and conditions</a>
{% endif %}


```

### Helpers

The above logic can also be written as:

```python

from urlmapper.helpers import check_mapped_url, get_mapped_url

if checked_mapped_url('terms-and-conditions'):
    # If you have any mapped functions that rely on the request being present
    # then you will need to pass it to get_mapped_url
    print get_mapped_url('terms-and-conditions', request=None)

```

Note that **check_mapped_url** and **get_mapped_url** only check and return
a valid URL (if any) for that key. Whether or not the user has the ability to
view the content at that URL is another matter, and could only ever be
determined at the point the user submits a request, potentially with additional
form data.


Advanced Settings
-----------------

###URLMAPPER_RAISE_EXCEPTION

Determines whether the template renderer should raise an exception if there is a
problem generating the URL (key does not exist or mapping function raises an
Exception).

Note that an exception is not raised if the key is valid but is not mapped to
anything.

Default is True.

###URLMAPPER_CONTENTTYPES

Restricts the content types that can be used for object mapping.

```python

URLMAPPER_CONTENTTYPES = (
    # (app_label, model)
    ('cms', 'blogpost'),
    ('cms', 'page')
)

```

Note that urlmapper is always an excluded app.

###URLMAPPER_ALLOWED_MAPPINGS

Restricts the type of URL mapping that can be performed using Django admin.

```python

# Default
URLMAPPER_ALLOWED_MAPPINGS = ['url', 'object', 'view_name']

```

Admins will only see fields for the available mapping type(s).

To do
-----

- ~~More test coverage~~ (currently 94%)
- Better widget for selecting a content object
