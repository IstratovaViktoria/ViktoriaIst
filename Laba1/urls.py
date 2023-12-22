"""
URL configuration for Laba1 project.

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
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from my_project import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/', views.show_info, name='info'),
    path('showbook/<int:id_user>/', views.show_book),
    path('showbook/<str:name_literature>/<int:id_publishing>/<int:id_user>/addstore/', views.add_store, name='add_store'),
    path('showbook/<str:name_literature>/<int:id_publishing>/<int:id_user>/<int:number_store>/deletestore/', views.delete_store, name='delete_store'),
    path('', views.show_index, name="home"),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('user_logout', views.logout_user, name='logout_user'),
    path('buyerView/<str:name_literature>/', views.show_publishing_ofLiterature, name='book_ofLiterature'),
    path('buyerView/<str:name_literature>/<int:id_publishing>/', views.show_bookFromPublishing, name='book_fromPublishing'),
    path('buyerView/<str:name_literature>/<int:id_publishing>/<int:id_user>/', views.show_book, name='show_book'),
    #ajax url
    path('ajax/validate_username', views.validate_username, name='validate_username'),
    path('ajax/check_store_number/<str:name_literature>/', views.check_numberStore, name='check_store_number'),
]
