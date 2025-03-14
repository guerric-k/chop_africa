from django.shortcuts import render, redirect, get_object_or_404
from .models import Table, Reservation, User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone

# Create your views here.
# Home view
def home_view(request):
    featured_meals = [
        {'name': 'Ekwang', 'description': 'A delicious mix of crushed Cocoyams, beef, leaves and fish', 'image': 'images/ekwang.jpeg'},
        {'name': 'Ndole', 'description': 'Bitter leaf stew and boiled plantains', 'image': 'images/ndole.jpg'},
        {'name': 'Grilled Mackerel', 'description': 'Grilled fish with boiled fermented cassava', 'image': 'images/grilled_mackerel.jpeg'},
        {'name': 'Puff Puff', 'description': 'Fried dough', 'image': 'images/puff_puff.jpg'},
        {'name': 'suya', 'Grilled Beef': 'Spicy grilled beef', 'image': 'images/suya.jpg'},
    ]
    return render(request, 'bookings/home.html', {'featured_meals': featured_meals})

#Menu view
def menu_view(request):
    meals = [{'name': f'Ekwang {i}', 'description': f'A delicious mix of crushed Cocoyams, beef, leaves {i}', 'price': i * 2500, 'image': f'images/ekwang{i}.jpeg'} for i in range(1, 21)]
    paginator = Paginator(meals, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'menu.html', {'meals': page_obj})
