from videos.models import Category

def categories_context_processor(request):
    return {
        'categories': Category.objects.all(),
    }