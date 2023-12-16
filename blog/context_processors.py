from .models import Category

def menu(request):
    # Define your menu items here
    categories = Category.objects.all()

    # You can add more logic to dynamically generate menu items based on your requirements

    # Return a dictionary with the menu data
    return {'categories': categories}