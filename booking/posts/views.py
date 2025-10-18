from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import datetime 
from .models import Table, Customer, TableDate

# Update the cistomers data base
def update_customers():
    # Delete all customers without an assigned table
    Customer.objects.filter(table=None).delete()

# Update the dates for each table (reservations)
def update_table_dates():
    # Remove all expired TableDate created
    today = datetime.date.today()

    expired_table_dates = TableDate.objects.filter(date__lt=today)
    for table_date in expired_table_dates:
        table_date.table.status = Table.TableStatus.AVAILABLE
        table_date.table.save()
        table_date.delete()

    table_dates_for_today = TableDate.objects.filter(date=today)
    # Set all table that have a reservation for today as unvailable
    for table_date in table_dates_for_today:
        table_date.table.status = Table.TableStatus.UNAVAILABLE
        table_date.table.save()

# Create your views here.
def index(request):
    update_customers()
    update_table_dates()
    return render(request, 'index.html')

# Customer reservation
def reservation(request):

    if request.method == 'POST':
        # Collect data from customer
        name = request.POST.get('name')
        if not name:
            messages.error(request, "Please write your name.")
            return redirect('reservation')

        phone_number = request.POST.get('phone_number')
        if not name:
            messages.error(request, "Please write your phone number.")
            return redirect('reservation')
        
        number_of_guests = request.POST.get('number_of_guests')
        if not number_of_guests:
            messages.error(request, "Please select the number of guests.")
            return redirect('reservation')
        
        date_str = request.POST.get('date')
        if not date_str:
            messages.error(request, "Please select a date.")
            return redirect('reservation')
        
        time_str = request.POST.get('time')
        if not time_str:
            messages.error(request, "Please select a time.")
            return redirect('reservation')
        
        notes = request.POST.get('notes')
        # Convert strings to python date and time types
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.datetime.strptime(time_str, '%H:%M').time()

        customer = Customer.objects.create(
            name=name,
            phone_number=phone_number,
            number_of_guests=number_of_guests,
            notes=notes,
            date=date,
            time=time,
        )
        customer.save()
        return redirect('checkTables', customer_id=customer.id)
    else:   
        return render(request, 'reservation.html')

# Set the available tables to reserve 
def checkTables(request, customer_id):
    update_table_dates()
    customer = Customer.objects.get(id=customer_id)
    # Collect all available tables for that date
    tables = Table.objects.all()
    available_tables = []
    for table in tables:
        # Select all dates that are already reserved
        dates = []
        for date in table.dates.all():
            dates.append(date.date)
        if customer.date not in dates:
            available_tables.append(table)

    if(len(available_tables) > 0 ):
        return render(request, 'checkTables.html', {'tables': available_tables, 'customer' : customer})
    else:
        messages.info(request, 'No tables available, please choose a different date.')
        return redirect('/')

# Assign a table to customer
def assignTable(request, customer_id, table_id):
    customer = Customer.objects.get(id=customer_id)
    table = Table.objects.get(id=table_id)

    if request.method == 'POST':
        # Assign the table to customer
        customer.table = table
        customer.save()
        #Create a date for the table
        table_date = TableDate.objects.create(name=customer.name, date=customer.date, table=table)
        table_date.save()
        messages.success(request, 'Table assigned successfully!')
        return redirect('/')
    else:
        # Delete customer's data
        customer.delete()
        messages.info(request, 'Table not assigned. Please try again.')
        return redirect('/')

# Staff login
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('staff', username=username)
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
# Staff logout
def logout(request):
    auth.logout(request)
    return redirect('/')

# Staff environment
def staff(resquest, username):
    update_table_dates()
    update_customers()
    today = datetime.date.today()

    total_tables = len(Table.objects.all())
    unav_tables= len(Table.objects.filter(status='unavailable'))
    # Let's do it like this for now
    customers_day = Customer.objects.filter(date=today)
    customers_month = Customer.objects.filter(date__month=today.month)
    customers_year = Customer.objects.filter(date__year=today.year)


    return render(resquest, 'staff.html',
                   {'username' : username,
                    'customers_day' : customers_day,
                    'customers_month' : customers_month,
                    'customers_year' : customers_year,
                    'total' : total_tables,
                    'occupied' : unav_tables,
                    'date' : today
                    })




