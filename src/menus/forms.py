from django import forms

from .models import Item
from restaurants.models import RestaurantLocation


class ItemFrom(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        '''
        handling of additional arguments;
        here we pass a user to our form
        '''
        super(ItemFrom, self).__init__(*args, **kwargs)

        # update the queryset that is coming to the foreign key
        self.fields['restaurant'].queryset = RestaurantLocation.objects.filter(owner=user)

    class Meta:
        model = Item
        fields = [
            'restaurant',
            'name',
            'contents',
            'excludes',
            'public',
        ]