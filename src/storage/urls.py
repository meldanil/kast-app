from django.urls import path

from . import views

app_name = 'storage'
urlpatterns = [
    path('', views.title_list_view, name='list'),
    path('create/', views.title_create_view, name='create'),
    path('<str:isbn>/', views.title_detail_view, name='detail'),
    path('<str:isbn>/download/<int:pk>/', views.title_attachment_download_view, name='download'),
    path('category/<slug:category_handle>/', views.category_list, name='category_list'),
    path('level/<slug:level_handle>/', views.level_list, name='level_list'),
    path('basket', views.basket_summary, name='basket_summary'),
    path('add_to_cart/<isbn>', views.add_to_cart, name='add-to-cart'),
    path('order-summary', views.OrderSummaryView.as_view(), name='order-summary'),
    path('remove-from-cart/<isbn>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<isbn>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('thankyou', views.finalise, name='thank'),
    path('main_table', views.main_table_view, name='main_table'),
    path('check', views.check_amount, name='check')
]