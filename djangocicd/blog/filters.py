from django_filters import CharFilter, FilterSet
from django.contrib.postgres.search import SearchVector
from django.utils import timezone
from rest_framework.exceptions import APIException

from djangocicd.blog.models import Post


class PostFilter(FilterSet):
    search = CharFilter(method="filter_search")
    author__in = CharFilter(method="filter_author__in")
    created_at__range = CharFilter(method="filter_created_at__range")
    
    def filter_search(self, qs, name, value):
        return qs.annotate(search=SearchVector("title")).filter(search=value) 

    def filter_author__in(self, qs, name, value):
        limit = 10
        authors = value.split(",")
        if len(authors) > limit:
            raise APIException(f"You can't add more than {len(authors)} usernames")
        return qs.filter(author__username__in=authors)

    def filter_created_at__range(self, qs, name, value):
        limit = 2
        created_at__in = value.split(",")
        if len(created_at__in) > limit:
            raise APIException(f"Only adding two 'created_in' comma-separated in the middle allowed")
        created_at_0, created_at_1 = created_at__in
        
        if not created_at_1:
            created_at_1 = timezone.now()

        if not created_at_0:
            return qs.filter(created_at__date__lt=created_at_1)
        
        return qs.filter(created_at__date__range=(created_at_0, created_at_1))
        
    class Meta:
        model = Post
        fields = ("slug", "title", )
    
