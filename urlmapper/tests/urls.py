from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'test/$', TemplateView.as_view(), name='test'),
    url(r'test/(?P<slug>[-\w]+)/$', TemplateView.as_view(), name='test'),
    url(r'test/(?P<pk>\d+)/$', TemplateView.as_view(), name='test'),
]
