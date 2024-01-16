from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from django_countries.fields import CountryField

PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=100)
    handle = models.SlugField(unique=True)
    comment = models.CharField(max_length=250, null=True, blank=True)
    handle = models.SlugField(unique=True, max_length=250) #slug


    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('storage:category_list', args=[self.handle])
    
    def __str__(self):
        return self.category
    
    


class Level(models.Model):
    level = models.CharField(max_length=100)
    handle = models.SlugField(unique=True)
    comment = models.CharField(max_length=250, null=True, blank=True)
    

    class Meta:
        verbose_name_plural = 'Levels'

    def __str__(self):
        return self.level
    
    def get_absolute_url(self):
        return reverse('storage:level_list', args=[self.handle])

class Title(models.Model):
    isbn = models.CharField(max_length=16, unique=True)
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    publisher = models.CharField(max_length=250, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    origin = models.CharField(max_length=250, blank=True, null=True)
    language = models.CharField(max_length=250, blank=True, null=True)
    cover = models.ImageField(upload_to='storage/', blank=True, null=True, default='storage/book_default.jpg')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.DO_NOTHING)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    category_id = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    level_id = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    products = ProductManager()
    objects = models.Manager()
    # handle = models.SlugField(unique=True) #slug

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/storage/{self.isbn}/"
    

    class Meta:
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.title
    
    def handle_book_attachment_upload(instance, filename):
        return f"storage/{instance.title.isbn}/attachments/{filename}"
    
    def get_copy(self):
        copy_dict = Placebook.objects.filter(title=self.id).values('copy')
        amount = 0
        for item in copy_dict:
            amount += item['copy']
        return amount
    
    def get_add_to_cart_url(self):
        return reverse("storage:add-to-cart", kwargs={
            'isbn': self.isbn
        })

    def get_remove_from_cart_url(self):
        return reverse("storage:remove-from-cart", kwargs={
            'isbn': self.isbn
        })
    

class TitleFile(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/', storage=protected_storage)
    is_free = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Place(models.Model):
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=250, null=True)
    handle = models.SlugField(unique=True) #slug

    class Meta:
        verbose_name_plural = 'Places'

    def __str__(self):
        return self.name


class Placebook(models.Model):
    title = models.ForeignKey('Title', on_delete=models.CASCADE)
    place = models.ForeignKey("Place", on_delete=models.CASCADE)
    copies_num = models.IntegerField()
    handle = models.SlugField(unique=True) #slug

    class Meta:
        verbose_name_plural = 'Placebooks'

    def __str__(self):
        return str(self.id)

    # def __str__(self):
    #     return self.name

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Title, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    

    
    


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=250)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_adres = models.CharField(max_length=250)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length = 15)

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        amount = 0
        for item in self.items.all():
            amount += item.quantity
        return amount
    



class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'