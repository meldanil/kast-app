from django.contrib import admin

from .models import Title, Category, Level, Place, Placebook, TitleFile, Order, OrderItem

# Register your models here.
admin.site.register(Title)
# admin.site.register(Category)
# admin.site.register(Level)
admin.site.register(Place)
admin.site.register(TitleFile)
admin.site.register(Placebook)
# admin.site.register(Placebook)
admin.site.register(Order)
admin.site.register(OrderItem)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'handle']
    prepopulated_fields = {'handle': ('category',)}

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['level', 'handle']
    prepopulated_fields = {'handle': ('level',)}
    list_editable = ['handle']
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'contact_person',
                    'phone'
                    'being_delivered',
                    'received',
                    'start_date',
                    'delivered',
                    'shipping_address',
                    'created',
                    ]
    list_display_links = [
        'user'
        
    ]
    list_filter = ['ordered',
                   'delivered',
                   'received'
                   ]
    search_fields = [
        'user__username'
    ]
    # actions = [make_refund_accepted]

