from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from django.views.generic import CreateView
from .filters import SalesProductsFilter
from DeliveryManagement.models import DeliveryCost
from CostAnalysisManagement.models import RetailPrice

from .utils import cart_data
from .decorators import unauthenticated_user, sales_manager_only
from .models import *
from .forms import *  # BulkOrderRequestForm, BulkOrderItemsInlineFormset
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import UserCreationForm
import json
import datetime

# PDF gen imports
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

import csv


# ========================================Sales Manager related view functions=========================================
# Product page in the sales dashboard
@sales_manager_only
def sales_dashboard(request):
    total_orders = Order.objects.count()
    total_completed_orders = Order.objects.filter(order_status='Delivered').count()
    items_sold = OrderItem.objects.all().aggregate(Sum('quantity'))['quantity__sum']
    total_products = SalesProduct.objects.count()
    total_sales_tasks = SalesTask.objects.count()
    total_completed_sales_tasks = SalesTask.objects.filter(task_status='Task Completed').count()

    order_item = OrderItem.objects.all()

    orders = Order.objects.all().order_by('date_ordered').aggregate(Sum('net_total'))['net_total__sum']

    total_sales_teams = SalesTeam.objects.count()
    total_customers = Customer.objects.count()
    total_sales = Order.objects.all().aggregate(Sum('net_total'))['net_total__sum']
    products = SalesProduct.objects.all().order_by('category')

    # Sales chart related functions
    today_income = Order.objects.filter(date_ordered__contains=datetime.date.today()).aggregate(Sum('net_total'))[
        'net_total__sum']
    day2_income = \
        Order.objects.filter(date_ordered__contains=datetime.date.today() - datetime.timedelta(days=1)).aggregate(
            Sum('net_total'))['net_total__sum']
    day3_income = \
        Order.objects.filter(date_ordered__contains=datetime.date.today() - datetime.timedelta(days=2)).aggregate(
            Sum('net_total'))['net_total__sum']
    day4_income = \
        Order.objects.filter(date_ordered__contains=datetime.date.today() - datetime.timedelta(days=3)).aggregate(
            Sum('net_total'))['net_total__sum']
    day5_income = \
        Order.objects.filter(date_ordered__contains=datetime.date.today() - datetime.timedelta(days=4)).aggregate(
            Sum('net_total'))['net_total__sum']
    day6_income = \
        Order.objects.filter(date_ordered__contains=datetime.date.today() - datetime.timedelta(days=5)).aggregate(
            Sum('net_total'))['net_total__sum']

    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    day3 = datetime.date.today() - datetime.timedelta(days=2)
    day4 = datetime.date.today() - datetime.timedelta(days=3)
    day5 = datetime.date.today() - datetime.timedelta(days=4)
    day6 = datetime.date.today() - datetime.timedelta(days=5)

    day_list = [day6, day5, day4, day3, yesterday, today]
    income_list = [day6_income, day5_income, day4_income, day3_income, day2_income, today_income]

    # Sales products related chart
    category1_count = SalesProduct.objects.filter(category='s').count()
    category2_count = SalesProduct.objects.filter(category='F').count()
    category3_count = SalesProduct.objects.filter(category='N').count()
    category4_count = SalesProduct.objects.filter(category='H').count()
    category5_count = SalesProduct.objects.filter(category='O').count()

    product_category_count = [category1_count, category2_count, category3_count, category4_count, category5_count]
    product_categories = ['Skin Cosmetics', 'Face Makeup', 'Nail Cosmetic', 'Hair Cosmetic', 'Other categories']

    context = {
        'total_orders': total_orders,
        'total_completed_orders': total_completed_orders,
        'items_sold': items_sold,
        'total_sales_tasks': total_sales_tasks,
        'total_completed_sales_tasks': total_completed_sales_tasks,
        'total_sales_teams': total_sales_teams,
        'total_customers': total_customers,
        'total_products': total_products,
        'total_sales': total_sales,
        'orders': orders,
        'products': products,
        'day_list': day_list,
        'income_list': income_list,
        'product_category_count': product_category_count,
        'product_categories': product_categories,

    }
    return render(request, 'CustomerAndSalesManagement/sales/sales_dashboard.html', context)


def sales_product_page(request):
    products = SalesProduct.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'CustomerAndSalesManagement/sales/sales_products.html', context)


# product update page in the sales dashboard
def update_product_page(request):
    products = SalesProduct.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'CustomerAndSalesManagement/sales/sales_product_update.html', context)


# Adding new products into the selling platform
def create_sales_products(request):
    sales_products = SalesProduct.objects.values('name')

    #Retail_price = RetailPrice.objects.all()

    products = RetailPrice.objects.exclude(product_name__in=sales_products)
    form = ProductForm()
    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/customer_sales/sales_products')

    context = {
        'form': form,
        'products': products,
    }

    return render(request, 'CustomerAndSalesManagement/sales/product_form.html', context)


# Update the product in the selling platform
def update_sales_products(request, pk):
    product = SalesProduct.objects.get(id=pk)
    form = UpdateProductForm(instance=product)
    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = UpdateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/customer_sales/update_products')

    context = {
        'form': form
    }
    return render(request, 'CustomerAndSalesManagement/sales/product_update_form.html', context)


# Delete a product from the selling platform
def delete_sales_products(request, pk):
    product = SalesProduct.objects.get(id=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('/customer_sales/update_products')

    context = {
        'product': product
    }
    return render(request, 'CustomerAndSalesManagement/sales/product_delete_form.html', context)


# Sales team management
def sales_teams_management(request):
    sales_teams = SalesTeam.objects.all()
    sales_teams_count = SalesTeam.objects.all().count()
    available_teams = SalesTeam.objects.filter(available=True)
    available_teams_count = SalesTeam.objects.filter(available=True).count()

    task_teams = SalesTask.objects.values('sales_team')
    teams_with_tasks = SalesTeam.objects.filter(id__in=task_teams).count()
    completed_tasks = SalesTask.objects.filter(task_status='Task Completed').count()

    team_member_count = SalesTeamMembers.objects.all().count()
    available_team_members = SalesTeamMembers.objects.filter(sales_team__in=available_teams).count()

    context = {
        'sales_teams_count': sales_teams_count,
        'available_teams_count': available_teams_count,
        'team_member_count': team_member_count,
        'available_team_members': available_team_members,
        'teams_with_tasks': teams_with_tasks,
        'completed_tasks': completed_tasks,
        'sales_teams': sales_teams,
    }
    return render(request, 'CustomerAndSalesManagement/sales/sales_team_management.html', context)


def team_information_page(request, pk):
    team = SalesTeam.objects.get(id=pk)
    task = SalesTask.objects.filter(sales_team=team)
    employees = SalesTeamMembers.objects.filter(sales_team=team)

    context = {
        'team': team,
        'task': task,
        'employees': employees,
    }
    return render(request, 'CustomerAndSalesManagement/sales/sales_team_information_page.html', context)


# Manage Sales Teams
def update_sales_teams(request):
    sales_teams = SalesTeam.objects.all()
    context = {
        'sales_teams': sales_teams,
    }
    return render(request, 'CustomerAndSalesManagement/sales/update_sales_teams.html', context)


# assign team members
def manage_sales_teams(request):
    sales_team = SalesTeam.objects.last()
    context = {
        'sales_team': sales_team
    }
    return render(request, 'CustomerAndSalesManagement/sales/sales_tasks_teams.html', context)


# Sales team creation page
def create_sales_team(request):
    form = CreateSalesTeamForm()

    if request.method == 'POST':
        form = CreateSalesTeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/customer_sales/manage_sales_teams')

    context = {
        'form': form,
    }
    return render(request, 'CustomerAndSalesManagement/sales/sales_create_team.html', context)


def assign_team_members(request, pk, pk2):
    sales_team = SalesTeam.objects.get(id=pk)

    teams_formset = inlineformset_factory(SalesTeam, SalesTeamMembers, form=AddTeamMembersForm, fields=('team_member',),
                                          extra=pk2)
    formset = teams_formset(instance=sales_team)
    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = AddTeamMembersForm(request.POST)
        formset = teams_formset(request.POST, instance=sales_team)
        if formset.is_valid():
            formset.save()
            return redirect('/customer_sales/sales_teams_management')

    context = {
        'formset': formset,
        'sales_team': sales_team,
    }
    return render(request, 'CustomerAndSalesManagement/sales/sales_assign_teams.html', context)


# Update Sales teams
def update_sales_team_form(request, pk):
    sales_team = SalesTeam.objects.get(id=pk)
    form = UpdateSalesTeamForm(instance=sales_team)

    if request.method == 'POST':
        form = UpdateSalesTeamForm(request.POST, instance=sales_team)
        if form.is_valid():
            form.save()
            return redirect('sales_teams_management')

    context = {
        'form': form,
        'sales_team': sales_team,
    }
    return render(request, 'CustomerAndSalesManagement/sales/update_sales_teams_form.html', context)


# assign team members
def update_sales_team_members(request, pk):
    sales_team = SalesTeam.objects.get(id=pk)
    context = {
        'sales_team': sales_team
    }
    return render(request, 'CustomerAndSalesManagement/sales/update_sales_team_members.html', context)


# Update team members
def update_team_members(request, pk, pk2):
    sales_team = SalesTeam.objects.get(id=pk)

    teams_formset = inlineformset_factory(SalesTeam, SalesTeamMembers, form=UpdateTeamMembersForm,
                                          fields=('team_member',),
                                          extra=0)
    formset = teams_formset(instance=sales_team)
    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = UpdateTeamMembersForm(request.POST)
        formset = teams_formset(request.POST, instance=sales_team)
        if formset.is_valid():
            formset.save()
            return redirect('/customer_sales/sales_teams_management')

    context = {
        'formset': formset,
        'sales_team': sales_team,
    }
    return render(request, 'CustomerAndSalesManagement/sales/update_team_members_form.html', context)


# Delete Sales Team
def delete_sales_team(request, pk):
    sales_team = SalesTeam.objects.get(id=pk)
    if request.method == 'POST':
        sales_team.delete()
        return redirect('/customer_sales/sales_teams_management')
    context = {
        'sales_team': sales_team
    }
    return render(request, 'CustomerAndSalesManagement/sales/delete_sales_team.html', context)


# Sales tasks management page
def sales_tasks_management(request):
    total_tasks = SalesTask.objects.all().count()
    completed_tasks = SalesTask.objects.filter(task_status='Task Completed').count()
    incomplete_tasks = SalesTask.objects.exclude(task_status='Task Completed').count()
    pending_tasks = SalesTask.objects.filter(task_status='Status Pending').count()
    assigned_tasks = SalesTask.objects.filter(task_status='Assigned').count()
    task_teams = SalesTask.objects.values('sales_team')
    teams_with_tasks = SalesTeam.objects.filter(id__in=task_teams).count()
    tasks = SalesTask.objects.all()

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'assigned_tasks': assigned_tasks,
        'incomplete_tasks': incomplete_tasks,
        'teams_with_tasks': teams_with_tasks,
        'tasks': tasks,

    }
    return render(request, 'CustomerAndSalesManagement/sales/sales_tasks_management.html', context)


def create_sales_task(request):
    form = CreateSalesTaskForm()
    if request.method == 'POST':
        form = CreateSalesTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/customer_sales/sales_tasks_management')

    context = {
        'form': form,
    }
    return render(request, 'CustomerAndSalesManagement/sales/sales_create_task.html', context)


def update_sales_tasks(request):
    sales_task = SalesTask.objects.all()
    context = {
        'sales_task': sales_task,
    }
    return render(request, 'CustomerAndSalesManagement/sales/update_sales_tasks.html', context)


def update_sales_tasks_form(request, pk):
    sales_task = SalesTask.objects.get(id=pk)
    form = UpdateSalesTaskForm(instance=sales_task)

    if request.method == 'POST':
        form = UpdateSalesTaskForm(request.POST, instance=sales_task)
        if form.is_valid():
            form.save()
            return redirect('/customer_sales/sales_tasks_management')

    context = {
        'form': form,
    }

    return render(request, 'CustomerAndSalesManagement/sales/update_sales_task_form.html', context)


def delete_sales_task(request, pk):
    sales_task = SalesTask.objects.get(id=pk)

    if request.method == 'POST':
        sales_task.delete()
        return redirect('/customer_sales/sales_tasks_management')

    context = {
        'sales_task': sales_task,
    }
    return render(request, 'CustomerAndSalesManagement/sales/delete_sales_task.html', context)


def customer_management(request):
    total_customers = Customer.objects.all().exclude(username='salesadmin').count()
    customers = Customer.objects.all().exclude(username='salesadmin')

    context = {
        'total_customers': total_customers,
        'customers': customers,
    }
    return render(request, 'CustomerAndSalesManagement/sales/sales_customer_management.html', context)


def view_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    total_orders = Order.objects.filter(customer=customer).count()
    orders = Order.objects.filter(customer=customer)
    total_order_items = OrderItem.objects.filter(order__customer=customer).aggregate(Sum('quantity'))['quantity__sum']
    context = {
        'customer': customer,
        'total_orders': total_orders,
        'total_order_items': total_order_items,
        'orders': orders,
    }
    return render(request, 'CustomerAndSalesManagement/sales/sales_customer_view.html', context)


# ========================================Report Generation======================================

# Generate PDF for Sales Product
def sales_products_pdf(request):
    # Create ByteStream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    text_ob = c.beginText()
    text_ob.setTextOrigin(inch, inch)
    text_ob.setFont("Helvetica", 14)

    # Adding lines to text
    # lines = [
    #     'This is line 1',
    #     'This is line 2',
    #     'This is line 3',
    # ]
    products = SalesProduct.objects.all()

    # Create a list
    lines = []
    for product in products:
        lines.append(product.name)
        lines.append(str(product.selling_price))
        lines.append(str(product.retail_price))
        lines.append(str(product.category))
        lines.append(str(product.description))
        lines.append(str(product.date_created))
        lines.append(str(product.vote_total))
        lines.append(str(product.vote_ratio))
        lines.append(" ")

    # Loop
    for line in lines:
        text_ob.textLine(line)

    # Finishing
    c.drawText(text_ob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='Sales_products.pdf')


# Sales Products CSV
def sales_products_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Sales_products.csv'

    # Create CSV Writer
    writer = csv.writer(response)

    products = SalesProduct.objects.all()

    # Add column headings to the csv file
    writer.writerow([
        'Product Name',
        'Category',
        'Description',
        'Markup Price',
        'Selling Price',
        'Date Created',
        'Total Votes',
        'Votes Ratio',
    ])

    # Loop through and output
    for product in products:
        writer.writerow([product.name,
                         product.category,
                         product.description,
                         product.retail_price,
                         product.selling_price,
                         product.date_created,
                         product.vote_total,
                         product.vote_ratio,
                         ])

    return response


# Sales Team CSV
def sales_teams_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Sales_teams.csv'

    # Create CSV Writer
    writer2 = csv.writer(response)

    teams = SalesTeam.objects.all()

    # Add column headings to the csv file
    writer2.writerow([
        'Team ID',
        'Team Name',
        'Description',
        'Date Created',
        'Availability',
        'No Of Employees',
    ])

    # Loop through and output
    for team in teams:
        writer2.writerow([team.id,
                          team.team_name,
                          team.team_description,
                          team.date_created,
                          team.available,
                          team.no_of_employees,
                          ])

    return response


# Sales Task CSV
def sales_task_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Sales_tasks.csv'

    # Create CSV Writer
    writer3 = csv.writer(response)

    tasks = SalesTask.objects.all()

    # Add column headings to the csv file
    writer3.writerow([
        'Task ID',
        'Task Name',
        'Description',
        'Sales Team',
        'Progress',
        'Status',
    ])

    # Loop through and output
    for task in tasks:
        writer3.writerow([task.id,
                          task.task_name,
                          task.task_description,
                          task.sales_team,
                          task.progress,
                          task.task_status,
                          ])

    return response


# ========================================Customer website related view functions======================================
# Register to the customer website
@unauthenticated_user
def customer_registration(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            return redirect('customer_login')

    context = {
        'form': form,
        'data': data,
        'cart_items': cart_items,
    }
    return render(request, 'CustomerAndSalesManagement/customer_registration.html', context)


# Customer side login function
@unauthenticated_user
def customer_login(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('customer_products')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {
        'data': data,
        'cart_items': cart_items,
    }
    return render(request, 'CustomerAndSalesManagement/customer_login.html', context)


def logout_customer(request):
    logout(request)
    messages.success(request, 'Customer was successfully logged out!')
    return redirect('customer_login')


# product page in the customer website
def sales_product(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        print('SEARCH: ', search_query)

    products = SalesProduct.objects.filter(Q(name__icontains=search_query) | Q(category__icontains=search_query))

    product_filter = SalesProductsFilter(request.GET, queryset=products)
    products = product_filter.qs

    context = {
        'products': products,
        'cart_items': cart_items,
        'search_query': search_query,
        'product_filter': product_filter,
    }

    return render(request, 'CustomerAndSalesManagement/customer_products.html', context)


# Product page
def customer_product_page(request, pk):
    data = cart_data(request)
    cart_items = data['cart_items']

    product = SalesProduct.objects.get(id=pk)
    reviews = ProductReview.objects.filter(product_id=pk)

    context = {
        'product': product,
        'cart_items': cart_items,
        'reviews': reviews,
    }

    return render(request, 'CustomerAndSalesManagement/customer_product_page.html', context)


# cart in the customer website
@login_required(login_url='customer_login')
def cart(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'CustomerAndSalesManagement/cart.html', context)


# checkout page in the customer website
@login_required(login_url='customer_login')
def checkout(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    delivery_cost = DeliveryCost.objects.all()
    fee = 0

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
        'delivery_cost': delivery_cost,
        'fee': fee,
    }
    return render(request, 'CustomerAndSalesManagement/checkout.html', context)


# Updating cart items
def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', product_id)

    customer = request.user.customer
    product = SalesProduct.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],

        )

    return JsonResponse('Payment Complete', safe=False)


def customer_home(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'CustomerAndSalesManagement/customer_home.html', context)


# ========================================Customer Account related functions============================================
# Customer dashboard page
@login_required(login_url='customer_login')
def customer_dashboard(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    user = request.user.customer
    user_id = user.username
    count = Order.objects.filter(customer__username=user_id).count()
    orders = Order.objects.filter(customer__username=user_id)[0:count - 1]
    order_items = OrderItem.objects.all()

    context = {
        'orders': orders,
        'order_items': order_items,
        'cart_items': cart_items,
    }
    return render(request, 'CustomerAndSalesManagement/customer_account/customer_dashboard.html', context)


def customer_orders(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    user = request.user.customer
    user_id = user.username
    count = Order.objects.filter(customer__username=user_id).count()
    orders = Order.objects.filter(customer__username=user_id)[0:count - 1]

    items = OrderItem.objects.all()

    context = {
        'orders': orders,
        'items': items,
        'cart_items': cart_items,
    }
    return render(request, 'CustomerAndSalesManagement/customer_account/customer_orders.html', context)


@login_required(login_url='customer_login')
def customer_order_details_page(request, pk):
    data = cart_data(request)
    cart_items = data['cart_items']

    order = Order.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order=pk)
    shipping_address = ShippingAddress.objects.get(order=pk)

    context = {
        'cart_items': cart_items,
        'order': order,
        'order_items': order_items,
        'shipping_address': shipping_address,
    }
    return render(request, 'CustomerAndSalesManagement/customer_account/customer_order_details.html', context)


@login_required(login_url='customer_login')
def customer_review(request, pk, pk2):
    data = cart_data(request)
    cart_items = data['cart_items']

    product = SalesProduct.objects.get(id=pk)
    order = Order.objects.get(id=pk2)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.product = product
        review.customer = request.user.customer
        review.save()

        product.get_vote_count

        return redirect('customer_order_details', pk2)

    context = {
        'form': form,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'CustomerAndSalesManagement/customer_account/customer_product_review.html', context)


@login_required(login_url='customer_login')
def customer_reviews_page(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    customer = request.user.customer
    reviews = ProductReview.objects.filter(customer=customer.id)

    context = {
        'reviews': reviews,
        'cart_items': cart_items,
    }
    return render(request, 'CustomerAndSalesManagement/customer_account/customer_reviews.html', context)


@login_required(login_url='customer_login')
def customer_edit_review(request, pk):
    data = cart_data(request)
    cart_items = data['cart_items']

    review = ProductReview.objects.get(id=pk)
    form = EditReviewForm(instance=review)

    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = EditReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('/customer_sales/customer_reviews')

    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'CustomerAndSalesManagement/customer_account/customer_review_update.html', context)


@login_required(login_url='customer_login')
def customer_edit_profile(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    customer = request.user.customer
    form = EditProfileForm(instance=customer)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

            return redirect('customer_dashboard')

    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'CustomerAndSalesManagement/customer_account/customer_edit_profile.html', context)


@login_required(login_url='customer_login')
def customer_profile(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    customer = request.user.customer

    context = {
        'cart_items': cart_items,
        'customer': customer,
    }
    return render(request, 'CustomerAndSalesManagement/customer_account/customer_profile.html', context)


@login_required(login_url='customer_login')
def bulk_order_request_page(request):
    customer = request.user.customer

    form = BulkOrderRequestForm()

    if request.method == 'POST':
        form = BulkOrderRequestForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.customer = customer
            order.save()
            return redirect('/customer_sales/bulk_order_request_add_products')

    context = {
        'form': form,
    }
    return render(request, 'CustomerAndSalesManagement/customer_bulk_order_request.html', context)


@login_required(login_url='customer_login')
def bulk_order_request_add_products(request):
    customer = request.user.customer
    product_count = SalesProduct.objects.all().count()
    bulk_order = BulkOrderRequest.objects.last()
    sales_products = SalesProduct.objects.all()

    bulk_products_formset = inlineformset_factory(BulkOrderRequest, BulkOrderItems, form=BulkOrderItemsForm,
                                                  fields=('product', 'quantity',),
                                                  extra=product_count)
    formset = bulk_products_formset(instance=bulk_order)
    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = BulkOrderItemsForm(request.POST)
        formset = bulk_products_formset(request.POST, instance=bulk_order)
        if formset.is_valid():
            formset.save()
            return redirect('/customer_sales/customer_dashboard')

    context = {
        'formset': formset,
        'sales_products': sales_products,
    }
    return render(request, 'CustomerAndSalesManagement/bulk_order_add_items.html', context)
