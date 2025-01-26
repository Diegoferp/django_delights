from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils.timezone import now
from .models import MenuItem, RecipeRequirement, Ingredient, Purchase
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, F, Count
from django.db import models



class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if 'next' in request.GET:
            messages.info(request, "You need to log in to access this page.")
        return super().get(request, *args, **kwargs)



@login_required
def create_ingredient(request):
    if request.method == "POST":
        name = request.POST.get("name")
        unit = request.POST.get("unit")
        price_per_unit = request.POST.get("price_per_unit")
        quantity = request.POST.get("quantity")

        # Check if the ingredient already exists
        if Ingredient.objects.filter(name=name).exists():
            return render(request, "create_ingredient.html", {
                "error_message": f"Ingredient '{name}' already exists. Please choose a different name or update the existing ingredient."
            })

        try:
            # Create the ingredient if it doesn't exist
            Ingredient.objects.create(
                name=name,
                unit=unit,
                price_per_unit=price_per_unit,
                quantity=quantity
            )
            return redirect("inventory")  # Redirect to the ingredient list page
        except IntegrityError:
            # Catch unexpected integrity errors
            return render(request, "create_ingredient.html", {
                "error_message": "An error occurred while creating the ingredient. Please try again."
            })

    return render(request, "create_ingredient.html")

    


@login_required
def update_ingredient(request, pk):
    ingredient = Ingredient.objects.get(id=pk)

    if request.method == "POST":
        ingredient.name = request.POST.get("name")
        ingredient.unit = request.POST.get("unit")
        ingredient.price_per_unit = request.POST.get("price_per_unit")
        ingredient.quantity = request.POST.get("quantity")
        ingredient.save()
        return redirect("inventory")

    return render(request, "update_ingredient.html", {"ingredient": ingredient})



@login_required
def delete_ingredient(request, pk):
    ingredient = Ingredient.objects.get(id=pk)

    if request.method == "POST":
        ingredient.delete()
        return redirect("inventory")

    return render(request, "delete_ingredient.html", {"ingredient": ingredient})




@login_required
def inventory_view(request):
    ingredients = Ingredient.objects.all()  # Fetch all ingredients
    return render(request, 'inventory.html', {'ingredients': ingredients})



@login_required
def create_menu_item(request):
    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        MenuItem.objects.create(title=title, price=price)
        return redirect("create_recipe")  # Redirect back to the create recipe page

    return render(request, "create_menu_item.html")


@login_required
def create_recipe_requirement(request, menu_item_id=None):
    menu_items = MenuItem.objects.all()
    ingredients = Ingredient.objects.all()

    if request.method == "POST":
        menu_item_id = menu_item_id or request.POST.get("menu_item")
        ingredient_id = request.POST.get("ingredient")
        quantity = request.POST.get("quantity")

        RecipeRequirement.objects.create(
            menu_item=MenuItem.objects.get(id=menu_item_id),
            ingredient=Ingredient.objects.get(id=ingredient_id),
            quantity=quantity
        )
        return redirect("recipe_list")  # Redirect to the recipe list page

    return render(request, "create_recipe.html", {"menu_items": menu_items, "ingredients": ingredients})




@login_required
def recipe_list(request):
    menu_items = MenuItem.objects.all()
    recipes = RecipeRequirement.objects.select_related('ingredient', 'menu_item')

    # Group recipes by menu item
    recipes_by_menu_item = {}
    for item in menu_items:
        recipes_for_item = []
        total_cost = 0  # Initialize total cost for the menu item
        for recipe in recipes.filter(menu_item=item):
            ingredient_cost = recipe.quantity * recipe.ingredient.price_per_unit
            total_cost += ingredient_cost
            recipes_for_item.append({
                'recipe': recipe,
                'ingredient_cost': ingredient_cost,
            })
        recipes_by_menu_item[item] = {
            'recipes': recipes_for_item,
            'total_cost': total_cost,
        }

    return render(request, "recipe_list.html", {
        "recipes_by_menu_item": recipes_by_menu_item,
    })




@login_required
def update_recipe_requirement(request, pk):
    recipe = RecipeRequirement.objects.get(id=pk)
    menu_items = MenuItem.objects.all()
    ingredients = Ingredient.objects.all()

    if request.method == "POST":
        recipe.menu_item = MenuItem.objects.get(id=request.POST.get("menu_item"))
        recipe.ingredient = Ingredient.objects.get(id=request.POST.get("ingredient"))
        recipe.quantity = request.POST.get("quantity")
        recipe.save()
        return redirect("recipe_list")

    return render(request, "update_recipe.html", {
        "recipe": recipe,
        "menu_items": menu_items,
        "ingredients": ingredients
    })



@login_required
def delete_recipe_requirement(request, pk):
    recipe = RecipeRequirement.objects.get(id=pk)

    if request.method == "POST":
        recipe.delete()
        return redirect("recipe_list")

    return render(request, "delete_recipe.html", {"recipe": recipe})





@login_required
def menu_view(request):
    menu = MenuItem.objects.all()
    menu_with_availability = []

    for item in menu:
        recipe_requirements = RecipeRequirement.objects.filter(menu_item=item)
        max_dishes = float('inf')  # Start with a large number to calculate the minimum possible
        missing_ingredients = []  # Track missing or insufficient ingredients

        for recipe in recipe_requirements:
            required_quantity = recipe.quantity
            available_quantity = recipe.ingredient.quantity

            # Check for missing or insufficient ingredients
            if available_quantity < required_quantity:
                missing_ingredients.append(f"{recipe.ingredient.name} ({required_quantity - available_quantity} {recipe.ingredient.unit} needed)")
                max_dishes = 0  # If any ingredient is missing, we can't make the dish
            elif required_quantity > 0:
                # Calculate potential dishes and update the minimum
                possible_dishes = available_quantity // required_quantity
                max_dishes = min(max_dishes, possible_dishes)

        menu_with_availability.append({
            'item': item,
            'max_dishes': int(max_dishes) if max_dishes != float('inf') else 0,
            'missing_ingredients': missing_ingredients,
        })

    return render(request, 'menu.html', {'menu_with_availability': menu_with_availability})






def home(request):
    menu_items = MenuItem.objects.all()  # Get all menu items

    if request.method == "POST":
        menu_item_id = request.POST.get("menu_item_id")
        customer_name = request.POST.get("customer_name")
        quantity = int(request.POST.get("quantity", 1))  # Default to 1 if not provided

        if not customer_name:
            return render(request, 'home.html', {
                'menu_items': menu_items,
                'error_message': "Customer name is required.",
            })

        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        recipe_requirements = RecipeRequirement.objects.filter(menu_item=menu_item)

        # Check if there are enough ingredients for the specified quantity
        for req in recipe_requirements:
            if req.quantity * quantity > req.ingredient.quantity:
                return render(request, 'home.html', {
                    'menu_items': menu_items,
                    'error_message': f"We apologize, not enough {req.ingredient.name} to make {quantity} {menu_item.title}(s)."
                })

        # Deduct quantities from ingredients
        for req in recipe_requirements:
            req.ingredient.quantity -= req.quantity * quantity
            req.ingredient.save()

        # Record the purchase multiple times for the quantity purchased
        purchases = [
            Purchase(menu_item=menu_item, user=customer_name, timestamp=now())
            for _ in range(quantity)
        ]
        Purchase.objects.bulk_create(purchases)

        return render(request, 'home.html', {
            'menu_items': menu_items,
            'success_message': f"Successfully purchased {quantity} {menu_item.title}(s)!"
        })

    return render(request, 'home.html', {'menu_items': menu_items})








@login_required
def purchases_view(request):
    purchases_list = Purchase.objects.select_related('menu_item').all().order_by('-timestamp')
    total_sales = sum(purchase.menu_item.price for purchase in purchases_list)
    
    # Pagination setup
    paginator = Paginator(purchases_list, 25)  # Show 25 purchases per page
    page_number = request.GET.get('page')
    purchases = paginator.get_page(page_number)

    return render(request, 'purchases.html', {
        'purchases': purchases,
        'total_sales': total_sales,
    })




@login_required
def add_recipe_ingredient(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    ingredients = Ingredient.objects.all()

    if request.method == "POST":
        ingredient_id = request.POST.get("ingredient")
        quantity = request.POST.get("quantity")

        RecipeRequirement.objects.create(
            menu_item=menu_item,
            ingredient=Ingredient.objects.get(id=ingredient_id),
            quantity=quantity
        )
        return redirect("recipe_list")  # Redirect back to the recipe list page

    return render(request, "add_recipe_ingredient.html", {
        "menu_item": menu_item,
        "ingredients": ingredients,
    })



@login_required
def dashboard_view(request):
    # Calculate revenue, cost, and profit
    purchases = Purchase.objects.select_related('menu_item').all()
    revenue = sum(purchase.menu_item.price for purchase in purchases)

    # Calculate total cost of ingredients used for the purchases
    ingredients_costs = RecipeRequirement.objects.select_related('ingredient', 'menu_item').all()
    cost = sum(
        req.quantity * req.ingredient.price_per_unit
        for req in ingredients_costs
        for _ in range(Purchase.objects.filter(menu_item=req.menu_item).count())
    )
    profit = revenue - cost

    # Get top-selling menu items with total sales and revenue
    top_selling_items = (
        Purchase.objects.values('menu_item__title')
        .annotate(
            total_sold=Count('menu_item'),
            total_revenue=Sum('menu_item__price')
        )
        .order_by('-total_sold')[:5]
    )

    return render(request, 'dashboard.html', {
        'revenue': revenue,
        'cost': cost,
        'profit': profit,
        'top_selling_items': top_selling_items,
    })