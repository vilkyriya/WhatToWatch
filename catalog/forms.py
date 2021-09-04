from crispy_forms.helper import FormHelper
from django import forms

from catalog.models import Composition


class CompositionForm(forms.ModelForm):
    rating_my = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class': 'col-md-4'}))

    class Meta:
        model = Composition
        fields = ['rating_my']

    def __init__(self, *args, **kwargs):
        super(CompositionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
