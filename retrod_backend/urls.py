"""
URL configuration for retrod_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.http import JsonResponse

def root_health_check(request):
    return JsonResponse({
        "status": "online",
        "service": "Retrod PMS AI Chatbot Server",
        "webhook_url": "/api/v1/integrations/whatsapp/webhook/",
        "version": "1.0.0"
    })

urlpatterns = [
    path("", root_health_check, name="root_health_check"),
    path("admin/", admin.site.urls),
    path("api/v1/integrations/", include("apps.integrations.urls")),
    path("api/v1/core/", include("apps.core.urls")),
]


