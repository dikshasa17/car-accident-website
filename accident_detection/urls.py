"""accident_detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from accident import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),

    #Auth
    path('signup/',views.signupuser, name='signupuser'),
    path('login/',views.loginuser, name='loginuser'),
    path('logout/',views.logoutuser, name='logoutuser'),

    #Driver's Detail
    path('details/',views.userdetail, name='userdetail'),
    path('',views.home, name='home'),
    path('view/',views.viewdetails, name='viewdetails'),
    path('delete/', views.deletedetails, name='deletedetails'),
    path('edit/', views.editdetails, name='editdetails'),
    path('search_users/', views.search_users, name='search_users'),
    path('search_emergency/', views.search_emergency, name='search_emergency'),

    #Emergency
    path('emergency/',views.emergencydetail, name='emergencydetail'),
    path('viewemergency/',views.viewemergency, name='viewemergency'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

