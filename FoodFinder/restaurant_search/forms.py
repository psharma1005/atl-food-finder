from django import forms

class RestaurantSearchForm(forms.Form):
    cuisine = forms.CharField(label='Restaurant Name', max_length=100)
    min_rating = forms.FloatField(label='Minimum Rating (1-5)', min_value=1.0, max_value=5.0)
    max_distance = forms.FloatField(label='Maximum Distance (in km)', min_value=0.1)