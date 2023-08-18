from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('create', views.create, name="create"),
    path('search/', views.search, name='search'),
    path('random/', views.random_page, name="random"),
    path('<str:name>/edit',views.edit, name="edit"),
    path("<str:name>",views.entry,name="entry")
    
]
