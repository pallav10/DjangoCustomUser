from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
import views

internal_apis = [
    url(r'^users/$', views.user_registration),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
    ]

urlpatterns = [
    url(r'^users/login$', views.user_login),
    url(r'^users/(?P<pk>[0-9]+)/change_password/$', views.user_change_password),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
