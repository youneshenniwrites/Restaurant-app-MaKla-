from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.db.models import Q

from .utils import unique_slug_generator
from .validators import validate_category


User = settings.AUTH_USER_MODEL  # built-in Django user model


class RestaurantLocationQueryset(models.query.QuerySet):  # RestaurantLocation.objects.all().search(query)
    def search(self, query):
        if query:
            query = query.strip()
            return self.filter(Q(name__icontains=query) |
                               Q(location__icontains=query) |
                               Q(category__icontains=query) |
                               Q(item__name__icontains=query) |
                               Q(item__contents__icontains=query)
                               ).distinct()
        return self


class RestaurantLocationManager(models.Manager):
    def get_queryset(self):
        return RestaurantLocationQueryset(self.model, using=self._db)

    def search(self, query):  # RestaurantLocation.objects.search()
        return self.get_queryset().search(query)


class RestaurantLocation(models.Model):
    owner = models.ForeignKey(User, default=1)  # associates a particular user to the restaurant model
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, null=True, blank=True)
    # validated category field
    category = models.CharField(max_length=120, null=True, blank=True, validators=[validate_category])
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)

    objects = RestaurantLocationManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurants:detail', kwargs={'slug': self.slug})

    @property
    def title(self):
        '''
        property that makes instance.title display instance.name
        '''
        return self.name


# Using Django Signals to customize data before saving to db
def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.category = instance.category.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=RestaurantLocation)



'''
Foreign keys associate a user to a particular model.
Many to one relation. We use here the built-in Django User model
to reverse associate a user with our Restaurant model.

Django Shell:

from django.contrib.auth import get_user_model
User = get_user_model
instance = User.objects.get(id=1)
instance.restaurantlocation_set.all()

'''