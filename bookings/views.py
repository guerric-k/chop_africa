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
    meals = []

    # Ekwang
    meals.extend([
        {'name': f'Ekwang {i}', 'description': f'A delicious mix of crushed Cocoyams, beef, leaves {i}', 'price': i * 10, 'image': f'images/ekwang{i}.jpeg'}
        for i in range(1, 21)
    ])

    # Ndole
    meals.extend([
        {'name': f'Ndole {i}', 'description': f'Bitter leaf stew and boiled plantains with beef and Shrimps {i}', 'price': i * 12, 'image': f'images/ndole{i}.jpg'}
        for i in range(1, 21)
    ])

    # Grilled Mackerel
    meals.extend([
        {'name': f'Grilled Mackerel {i}', 'description': f'Grilled fish with boiled fermented cassava {i}', 'price': i * 15, 'image': f'images/grilled_mackerel{i}.jpeg'}
        for i in range(1, 21)
    ])

    # Puff Puff
    meals.extend([
        {'name': f'Puff Puff {i}', 'description': f'Fried dough {i}', 'price': i * 5, 'image': f'images/puff_puff{i}.jpg'}
        for i in range(1, 21)
    ])

    # Suya
    meals.extend([
        {'name': f'Suya {i}', 'description': f'Spicy grilled beef {i}', 'price': i * 8, 'image': f'images/suya{i}.jpg'}
        for i in range(1, 21)
    ])

    # Akara
    meals.extend([
        {'name': f'Akara {i}', 'description': f'Spicy crushed fried beans {i}', 'price': i * 8, 'image': f'images/akara{i}.jpg'}
        for i in range(1, 21)
    ])

    # Jollof Rice
    meals.extend([
        {'name': f'Jollof Rice {i}', 'description': f'Spicy rice with Chicken {i}', 'price': i * 30, 'image': f'images/jollof{i}.jpg'}
        for i in range(1, 21)
    ])

    # Fulere
    meals.extend([
        {'name': f'Fulere {i}', 'description': f'Home made drink {i}', 'price': i * 8, 'image': f'images/fulere{i}.jpg'}
        for i in range(1, 21)
    ])

    # Peanut Soup
    meals.extend([
        {'name': f'Groundnut Soup {i}', 'description': f'Peanut stew with beef chops {i}', 'price': i * 8, 'image': f'images/groundnut_stew{i}.jpg'}
        for i in range(1, 21)
    ])

    #Moin Moin
    meals.extend([
        {'name': f'Moin Moin {i}', 'description': f'Steamed beans pudding {i}', 'price': i * 8, 'image': f'images/moin_moin{i}.jpg'}
        for i in range(1, 21)
    ])

    #Tiga nut drink
    meals.extend([
        {'name': f'Tiga Nut Drink {i}', 'description': f'Juiced Tiga nuts with ice blocks and Dates {i}', 'price': i * 8, 'image': f'images/tiger_nut{i}.jpg'}
        for i in range(1, 21)
    ])
    
    #Chapman Drink
    meals.extend([
        {'name': f'Chapman Drink {i}', 'description': f'Home made drinks {i}',
         'price': i * 8, 'image': f'images/chapman{i}.jpg'} for i in range(1, 21)
    ])

    paginator = Paginator(meals, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bookings/menu.html', {'meals': page_obj})


