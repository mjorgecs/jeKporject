from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reservation', views.reservation, name='reservation'),
    path('checkTables/<int:customer_id>', views.checkTables, name='checkTables'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('staff/<str:username>', views.staff, name='staff'),
    path('assignTable/<str:customer_id>/<int:table_id>', views.assignTable, name='assignTable'),
]