"""Flow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from FlowControling.views import HomePage, CalendarView, AccountView, StartView, DeleteAccount
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    # path('calendar/',  CalendarView.as_view()),
    path('calendar/<int:delta>/', CalendarView.as_view()),
    path('account', AccountView.as_view()),
    path('about', StartView.as_view()),
    path('account/delete', DeleteAccount.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),


]

