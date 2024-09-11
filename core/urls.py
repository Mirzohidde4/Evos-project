from django.contrib import admin
from django.urls import path
from main.views import HomePage

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', HomePage)
]
