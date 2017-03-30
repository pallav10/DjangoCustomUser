from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
import views

internal_apis = [
    url(r'^users/$', views.user_registration),
    ]

urlpatterns = []

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
