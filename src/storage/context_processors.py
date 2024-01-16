from .models import Category, Level


def categories(request):
    return {
        'categories': Category.objects.all()
    }

def levels(request):
    return {
        'levels': Level.objects.all()
    }
