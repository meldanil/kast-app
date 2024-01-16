import mimetypes
from .forms import TitleSearchForm
from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View

import random
import string

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Title, TitleFile, Category, Level, Order, OrderItem, Address
from .forms import TitleForm, CheckoutForm
import isbnlib


def title_create_view(request):
    context = {}
    form = TitleForm(request.POST or None)
    form1 = TitleSearchForm(request.POST or None)
    if form1.is_valid():
        pass
    context['form1'] = form1
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect('storage/create/')
        form.add_error(None, "You must be logged in to create a titles")
    context['form'] = form
    return render(request, 'storage/create.html', context)

def title_list_view(request):
    object_list = Title.products.all()
    paginate_by = 6
    return render(request, "storage/list.html", {"products": object_list})

def category_list(request, category_handle):
    category = get_object_or_404(Category, handle=category_handle)
    products = Title.objects.filter(category_id=category)
    return render(request, 'storage/list.html', {'category': category, 'products': products})

def level_list(request, level_handle):
    level = get_object_or_404(Level, handle=level_handle)
    products = Title.objects.filter(level_id=level)
    return render(request, 'storage/list.html', {'level': level, 'products': products})

def title_detail_view(request, isbn=None):
    obj = get_object_or_404(Title, isbn=isbn, in_stock=True)
    attachments = ['attachment'] # fix it later!
    is_owner = False
    if request.user.is_authenticated:
        is_owner = True
    is_owner = obj.user == request.user
    context = {"object": obj}
    if is_owner:
        form = TitleForm(request.POST or None, request.FILES or None , instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            #  return redirect('storage/create/')
        context['form'] = form
    return render(request, 'storage/detail.html', context)

def title_manage_detail_view(request, isbn=None):
    obj = get_object_or_404(Title, isbn=isbn)
    is_owner = False
    if request.user.is_authenticated:
        is_owner = True
    is_owner = obj.user == request.user
    context = {"object": obj}
    if is_owner:
        form = TitleForm(request.POST or None, request.FILES or None , instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            #  return redirect('storage/create/')
        context['form'] = form
    return render(request, 'storage/detail.html', context)

def title_attachment_download_view(request, isbn=None, pk=None):
    attachment = get_object_or_404(TitleFile, title__isbn=isbn, pk=pk)
    can_download = attachment.is_free or False
    if request.user.is_authenticated:
        can_download = True # check ownership
    if can_download is False:
        return HttpResponseBadRequest()
    file = attachment.file.open(mode='rb') # cdn - S3 object storage
    filename = attachment.file.name
    content_type, encoding = mimetypes.guess_type(filename)
    response =  FileResponse(file)
    response['Content-Type'] = content_type or 'application/octet-steam'
    response['Content-Disposition'] = f'attachment;filename={filename}'
    return response

def basket_summary(request):
    return render(request, 'storage/summary.html')


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'storage/order-summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

@login_required
def add_to_cart(request, isbn):
    item = get_object_or_404(Title, isbn=isbn)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__isbn=item.isbn).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("storage:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("storage:order-summary")
    else:
        start_date = timezone.now()
        order = Order.objects.create(
            user=request.user, start_date=start_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("storage:order-summary")

@login_required
def remove_from_cart(request, isbn):
    item = get_object_or_404(Title, isbn=isbn)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__isbn=item.isbn).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("storage:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("storage:detail", isbn=isbn)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("storage:detail", isbn=isbn)
    

@login_required
def remove_single_item_from_cart(request, isbn):
    item = get_object_or_404(Title, isbn=isbn)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__isbn=item.isbn).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("storage:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("storage:detail", isbn=isbn)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("storage:detail", isbn=isbn)

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }
            return render(self.request, "storage/checkout.html", context)
            
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("storage:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('storage:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("storage:order-summary")
