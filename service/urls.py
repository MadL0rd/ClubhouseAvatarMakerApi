from rest_framework import routers
from django.urls import path
from . import views

app_name = 'cl'
router = routers.DefaultRouter()

router.register('borders', views.BorderViewSet, basename='borders')
router.register('borders_new', views.BrandViewSet, basename='borders_new')
router.register('codes', views.CodesViewSet, basename='codes')
router.register('setting_json', views.SettingJsonViewSet, basename='setting_json')

urlpatterns = router.urls
urlpatterns += [
    path('get_token/', views.GetToken.as_view(), name='get_token'),
]
