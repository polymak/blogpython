"""
URL configuration for blogsite project.

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
from django.conf import settings
from django.conf.urls.static import static
from blog import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    
    # Legacy API endpoints (for backward compatibility)
    path('api/blogs/', api_views.BlogListCreateView.as_view(), name='api-blog-list-create'),
    path('api/blogs/<int:pk>/', api_views.BlogDetailView.as_view(), name='api-blog-detail'),
    path('api/users/', api_views.UserListCreateView.as_view(), name='api-user-list-create'),
    path('api/users/<int:pk>/', api_views.UserDetailView.as_view(), name='api-user-detail'),
    path('api/login/', api_views.login_view, name='api-login'),
    path('api/logout/', api_views.logout_view, name='api-logout'),
    path('api/check-auth/', api_views.check_auth, name='api-check-auth'),
    
    # New dedicated API for Flutter app
# path('api/v1/', include('blogsite_python_flutter.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
