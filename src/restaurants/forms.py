from django import forms

from .models import RestaurantLocation


class RestaurantLocationCreateForm(forms.ModelForm):

    class Meta:
        model = RestaurantLocation
        fields = [
            'name',
            'location',
            'category',
            'slug',
        ]


