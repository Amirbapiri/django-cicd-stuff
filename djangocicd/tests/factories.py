import factory
from django.utils import timezone
from django.contrib.auth import get_user_model

from djangocicd.tests.utils import faker
from djangocicd.users.models import Profile
from djangocicd.blog.models import Subscription, Post


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Iterator(["toltz@gmail.com", "dostoevsky@gmail.com", "camus@gmail.com"])
    password = factory.PostGenerationMethodCall("set_password", "testpasswor$")


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription
    
    subscriber = factory.SubFactory(UserFactory)
    target = factory.SubFactory(UserFactory)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(lambda _: f"{faker.unique.company()}")
    content = factory.LazyAttribute(lambda _: f"{faker.unique.company()}")
    slug = factory.LazyAttribute(lambda _: f"{faker.unique.company()}")
    created_at = factory.LazyAttribute(lambda _: f"{timezone.now()}")
    slug = factory.LazyAttribute(lambda _: f"{timezone.now()}")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
    
    user = factory.SubFactory(User)
    posts_number = factory.LazyAttribute(lambda _: 0) 
    subscriber_number = factory.LazyAttribute(lambda _: 0) 
    subscription_number  = factory.LazyAttribute(lambda _: 0) 
    bio = factory.LazyAttribute(lambda _: f"{faker.unique.company()}") 

