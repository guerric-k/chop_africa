from django.shortcuts import render, redirect, get_object_or_404
from .models import Table, Reservation, User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .forms import UserRegistrationForm, LoginForm, ReservationForm
from django.contrib.auth import authenticate, login

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'bookings/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'invalid form data.')
    else:
        form = LoginForm()
    return render(request, 'bookings/login.html', {'form': form})


# Logout view
def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, 'Logged out successfully.')
    return redirect('home')

#Menu view
def menu_view(request):
    meals = []

    # Ekwang
    meals.append(
        {'name': 'Ekwang', 'description': 'A delicious mix of crushed Cocoyams, beef, leaves', 'price': 10, 'image': 'images/ekwang.jpeg'}
    )

    # Ndole
    meals.append(
        {'name': 'Ndole', 'description': 'Bitter leaf stew and boiled plantains with beef and Shrimps', 'price': 12, 'image': 'images/ndole.jpg'}
    )

    # Grilled Mackerel
    meals.append(
        {'name': 'Grilled Mackerel', 'description': 'Grilled fish with boiled fermented cassava', 'price': 1500, 'image': 'images/grilled_mackerel.jpeg'}
    )

    # Puff Puff
    meals.append(
        {'name': 'Puff Puff', 'description': 'Fried dough', 'price': 5000, 'image': 'images/puff_puff.jpg'}
    )

    # Suya
    meals.append(
        {'name': 'Suya', 'description': 'Spicy grilled beef', 'price': 800, 'image': 'images/suya.jpg'}
    )

    # Akara
    meals.append(
        {'name': 'Akara', 'description': 'Spicy crushed fried beans', 'price': 800, 'image': 'images/akara.jpg'}
    )

    # Jollof Rice
    meals.append(
        {'name': 'Jollof Rice', 'description': 'Spicy rice with Chicken', 'price': 3000, 'image': 'images/jollof.jpg'}
    )

    # Fulere
    meals.append(
        {'name': 'Fulere', 'description': 'Home made drink', 'price': 850, 'image': 'images/fulere.jpg'}
    )

    # Peanut Soup
    meals.append(
        {'name': 'Groundnut Soup', 'description': 'Peanut stew with beef chops', 'price': 800, 'image': 'images/groundnut_stew.jpg'}
    )

    #Moin Moin
    meals.append(
        {'name': 'Moin Moin', 'description': 'Steamed beans pudding', 'price': 1000, 'image': 'images/moin_moi.jpg'}
    )

    #Tiga nut drink
    meals.append(
        {'name': 'Tiga Nut Drink', 'description': 'Juiced Tiga nuts with ice blocks and Dates', 'price': 900, 'image': 'images/tiger_nut.jpg'}
    )

    #Chapman Drink
    meals.append(
        {'name': 'Chapman Drink', 'description': 'Home made drinks', 'price': 800, 'image': 'images/chapman_drink.jpg'}
    )

    paginator = Paginator(meals, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bookings/menu.html', {'meals': page_obj})

# Contact view
def contact_view(request):
    return render(request, 'bookings/contact.html')

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

# Reservation view
def make_reservation(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to make a reservation.')
        return redirect('login')

    user = User.objects.get(customer_id=request.session['user_id'])
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = user
            try:
                reservation.clean()
                reservation.save()
                messages.success(request, 'Reservation successful!')
                return redirect('view_reservations')
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = ReservationForm()
    return render(request, 'bookings/make_reservation.html', {'form': form})

# View reservations view
def view_reservations(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to view reservations.')
        return redirect('login')

    user = User.objects.get(customer_id=request.session['user_id'])
    reservations = Reservation.objects.filter(user=user)
    return render(request, 'view_reservations.html', {'reservations': reservations})

# Modify reservation view
def modify_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id, user__customer_id=request.session.get('user_id'))

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reservation updated successfully.')
            return redirect('view_reservations')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'bookings/modify_reservation.html', {'form': form, 'reservation': reservation})

# Delete reservation view
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id, user__customer_id=request.session.get('user_id'))

    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation deleted successfully.')
        return redirect('view_reservations')

    return render(request, 'bookings/delete_reservation_confirm.html', {'reservation': reservation})

