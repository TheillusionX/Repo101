"""
URL configuration for appinstance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main_page'),
    path('request/', requests_page, name='requests_page'),
    path('inventory/', inventory_page, name="inventory_page"),
    path('sign_up/', sign_up_page, name = "sign_up_page"),
    path('log_in', log_in_page, name = "log_in_page"),
    path('performance/', performance_page, name = "performance_page")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)