from django.shortcuts import render, redirect, get_object_or_404
from .models import Table, Reservation, User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .forms import UserRegistrationForm, LoginForm, ReservationForm

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
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    request.session['user_id'] = user.customer_id
                    messages.success(request, 'Login successful!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid password.')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
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

    return render(request, 'modify_reservation.html', {'form': form, 'reservation': reservation})

# Delete reservation view
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id, user__customer_id=request.session.get('user_id'))

    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation deleted successfully.')
        return redirect('view_reservations')

    return render(request, 'delete_reservation_confirm.html', {'reservation': reservation})

