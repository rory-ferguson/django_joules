from django.conf.urls import url
from . import views

app_name = 'missing_categories'

urlpatterns = [
    url(r'', views.main, name=app_name),
]