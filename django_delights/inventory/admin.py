from django.contrib import admin
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase

# Register your models here.
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'price_per_unit', 'quantity')  # Ensure these fields exist in the model
    list_filter = ('name',)  # Use fields suitable for filtering (e.g., 'name' or 'price_per_unit')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')  # Fields displayed in the admin list view

@admin.register(RecipeRequirement)
class RecipeRequirementAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'ingredient', 'quantity')  # Fields displayed in the admin list view

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'timestamp', 'user')  # Fields displayed in the admin list view
