from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('ingredients/create/', views.create_ingredient, name='create_ingredient'),
    path('ingredients/update/<int:pk>/', views.update_ingredient, name='update_ingredient'),
    path('ingredients/delete/<int:pk>/', views.delete_ingredient, name='delete_ingredient'),
    path('purchases/', views.purchases_view, name='purchase_list'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/create/', views.create_recipe_requirement, name='create_recipe'),  # Create Recipe
    path('recipes/update/<int:pk>/', views.update_recipe_requirement, name='update_recipe'),
    path('recipes/delete/<int:pk>/', views.delete_recipe_requirement, name='delete_recipe'),
    path('menu/', views.menu_view, name='menu'),
    path('menu/create/', views.create_menu_item, name='create_menu_item'),  # Create Menu Item
    path('recipes/add_ingredient/<int:menu_item_id>/', views.add_recipe_ingredient, name='add_recipe_ingredient'),  # Add Recipe Ingredient
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
