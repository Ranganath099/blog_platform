from post.models import Category

def categories_context(request):
    return {"categories": Category.objects.all()}  # Return all categories
