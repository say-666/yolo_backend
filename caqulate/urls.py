from django.urls import path, include
from . import views
urlpatterns = [
    path('restart/channel', views.restart_channel),
    path('setting',views.caqulate_data),
    path('restart/setting',views.restart_setting),
    path('detail',views.caqulate_detail),
    path('simulate',views.simulate_caqulate),

]