from django.conf.urls import url


from .views import (ItemListView,
                    ItemCreateView,
                    ItemUpdateView)


urlpatterns = [
    url(r'^$', ItemListView.as_view(), name='list'),
    url(r'^create/$', ItemCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='detail'),
]





