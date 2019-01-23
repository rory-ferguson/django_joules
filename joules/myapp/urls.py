from django.conf.urls import url
from . import views

app_name = 'myapp'

urlpatterns = [
    url(r'', views.get_name, name='get_name'),
]