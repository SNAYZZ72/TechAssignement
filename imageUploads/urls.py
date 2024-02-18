from django.urls import path
from .views import index, edit_caption

urlpatterns = [
    path('', index, name='index'),
    path('edit/<int:image_id>/', edit_caption, name='edit_caption'),

]
