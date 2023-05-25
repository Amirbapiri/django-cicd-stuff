from django.db.models import QuerySet

from djangocicd.blog.models import Product


def get_products() -> QuerySet[Product]:
    return Product.objects.all()

