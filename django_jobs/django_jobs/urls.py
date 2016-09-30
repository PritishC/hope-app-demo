"""django_jobs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token
from users import views as user_views
from job_ready import views as job_views
from higher_edu import views as edu_views


router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet)
router.register(r'videos', job_views.VideoViewSet, base_name='videos')
router.register(r'articles', job_views.ArticleViewSet, base_name='articles')
router.register(r'universities', edu_views.UniversityViewSet)

urlpatterns = [
    url(r'^virmire/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^virmire-api/', include(router.urls)),
    url(r'^virmire-api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^virmire-api-token-auth/', user_views.JSONWebToken.as_view()),
    url(r'^virmire-api-token-refresh/', refresh_jwt_token),
]
