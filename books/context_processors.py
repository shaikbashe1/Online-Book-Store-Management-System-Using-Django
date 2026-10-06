from .models import Category

def categories_processor(request):
    return {'global_categories': Category.objects.all()}
