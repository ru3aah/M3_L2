from django.urls import path
from .views import show_all_models, index, home, show_one_model, delete_model

app_name = 'my_app'

urlpatterns = [
    path('', index, name='index'),
    path('index/', home),
    path('models/', show_all_models, name='models'),
    path('models/<int:id>/', show_one_model, name='one_model'),
    path('models/<int:id>/delete/', delete_model, name='delete_model'),
]