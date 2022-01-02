from django import forms
from .models import AdvisorWereda, Crop, CropProduction, Farmer, Livestock, LivestockProduction, Role, Training, User, Region, Wereda, Zone


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = "__all__"


class WoredaForm(forms.ModelForm):
    class Meta:
        model = Wereda
        fields = "__all__"

from .models import *
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import check_password
from django.contrib.admin.widgets import FilteredSelectMultiple


class AddFarmer(forms.ModelForm):

    class Meta:
        model = Farmer
        fields = ['id_number', 'name', 'phone', 'area']


class EditFarmer(forms.ModelForm):

    class Meta:
        model = Farmer
        fields = ['id_number', 'name', 'phone', 'area']


class AddCrop(forms.ModelForm):

    class Meta:
        model = Crop
        fields = '__all__'

class EditCrop(forms.ModelForm):
    model = Crop
    fields = "__all__"

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = "__all__"


class FieldAdvisorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "name",
            "phone",
            "region",
            "zone",
            "wereda",
            "date_of_birth",
            'gender', 
            'education_level'
        ]

    def clean(self):
        self.role = Role.objects.filter(short_name='advisor')
        return super().clean()
    def save(self, commit=True):
        user = super().save(commit=False)
        rr = Role.objects.get(short_name='advisor')
        user.role = rr
        return super().save(commit=commit)
        model = Crop
        fields = '__all__'



class AddCropProduction(forms.ModelForm):

    class Meta:
        model = CropProduction
        fields = '__all__'

class DataCropProduction(forms.ModelForm):

    class Meta:
        model = CropProduction
        fields = ['crop', 'quantity']


class EditCropProduction(forms.ModelForm):
    class Meta:
        model = LivestockProduction
        fields = '__all__'
class AdvisorWoredaForm(forms.ModelForm):
    class Meta:
        model = AdvisorWereda
        fields = "__all__"
    
class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = "__all__"

class CropForm(forms.ModelForm):
    class Meta:
        
        model = CropProduction
        fields = '__all__'



class AddLivestock(forms.ModelForm):

    class Meta:
        model = Livestock
        fields = '__all__'

class EditLivestock(forms.ModelForm):

    class Meta:
        model = Livestock
        fields = '__all__'


class AddLivestockProduction(forms.ModelForm):

    class Meta:
        model = LivestockProduction
        fields = '__all__'

class EditLivestockProduction(forms.ModelForm):
    class Meta:
        model = LivestockProduction
        fields = '__all__'

class DataGazer(forms.Form):

    crop_lists = [i.name for i in Crop.objects.all()]
    ID_number = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
    )
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
    )
    area = forms.IntegerField(
        widget=forms.NumberInput,
        min_value=0,
    )
    product_type = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput,
        min_value=0,
    )
 
 

    def clean(self):
        cleaned_data = super().clean()
        ID_number = cleaned_data.get('ID_number')
        name = cleaned_data.get('name')
        area = cleaned_data.get('area')
        product_type = cleaned_data.get('product_type')
        quantity = cleaned_data.get('quantity')
       
        if (not name) or (not area) or (not ID_number) or(not product_type) or (not quantity):
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data

