from django.shortcuts import render, get_object_or_404, redirect
from bookings.models import Reservation, User
from bookings.forms import ReservationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from .forms import ReservationFilterForm
# Dashboard views
def dashboard_view(request):
    # Basic dashboard overview
    total_reservations = Reservation.objects.count()
    total_users = User.objects.count()
   
   
    return render(request, 'dashboard/dashboard.html', {
        'total_reservations': total_reservations,
        'total_users': total_users,
    })

def dashboard_reservations(request):
    reservations = Reservation.objects.all()
    filter_form = ReservationFilterForm(request.GET)  # Instantiate the form with GET data

    if filter_form.is_valid():
        date = filter_form.cleaned_data.get('date')
        username = filter_form.cleaned_data.get('username')
        table_number = filter_form.cleaned_data.get('table_number')

        if date:
            reservations = reservations.filter(date=date)
        if username:
            reservations = reservations.filter(user__username__icontains=username)
        if table_number:
            reservations = reservations.filter(table__table_number=table_number)

    return render(request, 'dashboard/reservations.html', {'reservations': reservations, 'filter_form': filter_form})

def dashboard_meals(request):
    # View all meals
    # If you have a meal model
    # meals = Meal.objects.all()
    # return render(request, 'dashboard/meals.html', {'meals': meals})
    # If meals are still being created in the views.py:
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
    return render(request, 'dashboard/meals.html', {'meals': meals})

def dashboard_users(request):
    # View all users
    users = User.objects.all()
    return render(request, 'dashboard/users.html', {'users': users})

def modify_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reservation updated successfully.')
            return redirect('dashboard_reservations')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'dashboard/modify_reservation.html', {'form': form, 'reservation': reservation})

def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation deleted successfully.')
        return redirect('dashboard_reservations')

    return render(request, 'dashboard/delete_reservation_confirm.html', {'reservation': reservation})


# delete_reservation view
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation deleted successfully.')
        return redirect('dashboard_reservations')

    return render(request, 'dashboard/delete_reservation_confirm.html', {'reservation': reservation})