from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.roll_view, name='card'),
    path('update-rolik/<int:roll_id>', views.update_roll, name='update-roll'),
    path('logout/', LogoutView.as_view(template_name="registration/logout.html"), name='logout'),

]