from django.urls import include, path
from rest_framework import routers

from api.authenticate import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

apps = [
    ('auth/', 'api.authenticate.urls', 'auth'),
]

urlpatterns_apps = [path(url, include(urlconf, namespace=namespace)) for url, urlconf, namespace in apps]

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + urlpatterns_apps