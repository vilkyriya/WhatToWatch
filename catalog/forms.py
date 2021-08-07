from catalog.models import Composition
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib import admin


class CompositionForm(forms.ModelForm):
    rating_my = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class': 'col-md-4'}))

    class Meta:
        model = Composition
        fields = ['rating_my']

    def __init__(self, *args, **kwargs):
        super(CompositionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


# class CompositionAdminCreationForm(forms.ModelForm):
#     class Meta:
#         model = Composition
#         exclude = ['slug', 'rating_my']
#
#
# class CompositionAdminChangeForm(forms.ModelForm):
#     class Meta:
#         model = Composition
#         fields = "__all__"

