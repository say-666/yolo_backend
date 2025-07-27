from django.urls import path, include
from . import views
from caqulate import views as caqulate_views
from user import views as user_views
urlpatterns = [
    path('query/pages',views.pages),
    path('query/search',views.search),
    path('query/download',views.download),
    path('query/delete',views.delete_picture),

]