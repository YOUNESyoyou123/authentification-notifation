from django.contrib import admin
from django.urls import path
from auth_app import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inscription_view, name='inscription'),
    path('connexion/', views.connexion_view, name='connexion'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
]
urlpatterns += staticfiles_urlpatterns()