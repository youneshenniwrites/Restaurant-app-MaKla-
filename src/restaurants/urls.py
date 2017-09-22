from django.conf.urls import url


from .views import (RestaurantListView,
                    RestaurantCreateView,
                    RestaurantUpdateView)


urlpatterns = [
    url(r'^$', RestaurantListView.as_view(), name='list'),
    url(r'^create/$', RestaurantCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/edit/$', RestaurantUpdateView.as_view(), name='detail'),

]


