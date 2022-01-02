from django.shortcuts import render, redirect
from django.urls import  reverse_lazy
from django.views.generic.edit import UpdateView
from .prediction import crop_prediction
# Create your views here.
from django.contrib.auth.decorators import login_required
from .decorators import *
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.views.generic import  ListView , CreateView
from django.db import IntegrityError

from .models import  Farmer, Region, User, Zone, Wereda
from .forms import FieldAdvisorForm, RegionForm, WoredaForm, ZoneForm

from .models import *
import seaborn as sns

from .forms import *
from django.contrib.auth.forms import AuthenticationForm

from django.contrib import messages
from django.utils import timezone
# Create your views here.
def index(request):
    form = AuthenticationForm()
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        return render(request, 'registration/login.html', {'form': form})


@login_required
def homepage(request):
    if request.user.role.short_name == 'super':
        return redirect('/admin/')
    elif request.user.role.short_name == 'federal':
        return render(request, 'federal_index.html')
    elif request.user.role.short_name == 'region':
        return render(request, 'region_index.html')
    elif request.user.role.short_name == 'zone':
        return redirect('submit')
    elif request.user.role.short_name == 'wereda':
        return render(request, 'wereda_index.html')
    elif request.user.role.short_name == 'advisor':
        return render(request, 'advisor_index.html')

zone_list = ('Abeshge','Butajira','Cheha','Endegagn','Enemorina Eaner','Ezha','Geta','Gumer',
    'Kebena','Mareko','Meskane','Muhor Na Aklil','Soddo','Welkite (town)','Hadiya Zone',
    'Ana Lemo','Duna','Gibe','Gomibora','Hosaena','Lemo','Mirab Badawacho','Misha',
    'Misraq Badawacho','Shashogo','Soro ','Mirab Sooro','Siraro','Amekka','Dalocha',
    'Lanfro','Sankurra','Silte')

# crop_list = ['Korra', 'Wheat', 'Turnip', 'Pump Kin', 'Plums', 'Drum Stick', 'Barley', 'Potato', 
#     'Apple', 'other misc. pulses', 'Ricebean (nagadal)', 'Arecanut', 'Moong(Green Gram)', 
#     'Other Dry Fruit', 'Cond-spcs other', 'Sunflower', 'Beans & Mutter(Vegetable)', 
#     'Cashewnut Raw', 'Rajmash Kholar', 'Other Fresh Fruits', 'Ginger', 'Citrus Fruit', 
#     'Onion', 'Cucumber', 'Other Kharif pulses', 'Coriander', 'Orange', 'Water Melon', 
#     'Lentil', 'Castor seed', 'Kapas', 'Soyabean', 'Other Cereals & Millets', 'Ash Gourd', 
#     'Dry chillies', 'Rice', 'Tomato', 'Ribed Guard', 'Peach', 'Cashewnut', 'Bean', 'Coconut ', 
#     'Sesamum', 'Atcanut (Raw)', 'Jute & mesta', 'Sugarcane', 'Samai', 'Black pepper', 
#     'Cotton(lint)', 'Urad', 'Colocosia', 'Total foodgrain', 'Lemon', 'Rapeseed &Mustard', 
#     'Litchi', 'Pome Fruit', 'Papaya', 'Yam', 'Carrot', 'Jute', 'Blackgram', 'Coffee', 
#     'Moth', 'Snak Guard', 'Oilseeds total', 'Guar seed', 'Tapioca', 'Cardamom', 
#     'Small millets', 'Other Citrus Fruit', 'Cauliflower', 'Other  Rabi pulses', 'Jowar', 
#     'Lab-Lab', 'Peas  (vegetable)', 'Linseed', 'Brinjal', 'Cabbage', 'Safflower', 'Ragi', 
#     'Bitter Gourd', 'Bhindi', 'other oilseeds', 'Grapes', 'Bajra', 'Ber', 'Other Vegetables', 
#     'Pear', 'Sapota', 'Turmeric', 'other fibres', 'Jobster', 'Bottle Gourd', 'Jack Fruit', 
#     'Mango', 'Mesta', 'Masoor', 'Garlic', 'Arhar/Tur', 'Tea', 'Paddy', 'Dry ginger', 
#     'Gram', 'Pulses total', 'Beet Root', 'Varagu', 'Cowpea(Lobia)', 'Pome Granet', 
#     'Arcanut (Processed)', 'Sweet potato', 'Banana', 'Pineapple', 'Horse-gram', 'Maize', 
#     'Sannhamp', 'Niger seed', 'Tobacco', 'Rubber', 'Cashewnut Processed', 'Peas & beans (Pulses)', 
#     'Redish', 'Perilla', 'Groundnut', 'Khesari']

crop_list = ['Wheat', 'Onion', 'Orange', 'Rice', 'Tomato','Coffee']

def crop_prediction_view(request):
    features = ['Zone_Name', 'Crop', 'Area']
    context = {'prediction': -1, "zone": zone_list, "crop": crop_list}
    if request.method == 'POST':
        sample = []
        for f in features:
            sample.append(request.POST.get(f, False))
        # sa=sample[:2]
        # sb = sample[2]
        # x = []
        # for i in zone:
        #     if i in sa:
        #         x.append(1)
        #     else:
        #         x.append(0)
        # for i in crop:
        #     if i in sa:
        #         x.append(1)
        #     else:
        #         x.append(0)
        # sample = x + [float(sb)]
        sample[-1] = float(sample[-1])
        result = crop_prediction(sample)
        context['prediction'] = round(result, 2)

    return render(request, 'crop_prediction.html', context)


def federalGovtview(request):
        
    return render(request , 'federal_index.html')

def zoneListview(request, pk):
    
    zon = Zone.objects.filter(region__pk=pk)
    
    return render(request , 'zone_list.html', {'zone' : zon})

def woredaListview(request, pk):
    
    wereda = Wereda.objects.filter(zone__pk=pk)
    
    return render(request , 'wereda_list.html', {'wereda' : wereda})

def advisorListview(request, pk):
    
    advisor = User.objects.filter(wereda__pk=pk, role__short_name="advisor")
    
    return render(request , 'advisor_list.html', {'advisor' : advisor})

class AddRegionView(CreateView):
    form_class = RegionForm
    template_name = "add_region.html"
    success_url =  reverse_lazy("region")

class EditRegionView(UpdateView):
    extra_context = {"model" : "Region"}
    model = Region
    fields = "__all__"
    template_name = "edit_page.html"
    success_url = reverse_lazy("region")


class AddZoneView(CreateView):
    form_class = ZoneForm
    template_name = "add_zone.html"
    success_url =  reverse_lazy("region")

class EditZoneView(UpdateView):
    model = Zone 
    extra_context = {"model" : "Zone"}
    template_name = "edit_page.html"
    fields = "__all__"
    success_url =  reverse_lazy("region")
    
class AddWoredaView(CreateView):
    form_class = WoredaForm
    template_name = "add_woreda.html"
    success_url =  reverse_lazy("region")

class EditWoredaView(UpdateView):
    model = Wereda
    extra_context = {"model" : "Woreda"}
    fields = "__all__"
    template_name = "add_woreda.html"
    success_url =  reverse_lazy("region")

class AdvisorCreateView(CreateView):
    form_class = FieldAdvisorForm
    template_name = "add_advisor.html"
    success_url =  reverse_lazy("region")

class EditAdvisorCreateView(UpdateView):
    model = User
    template_name = "edit_page.html"
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
    extra_context = {"model" : "Advisor"}
    success_url =  reverse_lazy("region")


def region(request):
    regions = Region.objects.all()
    return render(request, 'federal_region.html', context={'regions' : regions})

# def zone(request, pk):
    
#     zones = Zone.objects.filter(region__pk=pk)
    
#     return render(request, 'federal_zone.html', context={'zones' : zones})

def woreda(request, pk):
    
    weredas = Wereda.objects.filter(zone__pk=pk)
    
    return render(request, 'federal_woreda.html', context={'weredas' : weredas})

def field_advisor(request, pk):
    field_ads = User.objects.filter(wereda__pk=pk)
    return render(request, 'field_advisor.html', {"advisors": field_ads})

def advisor_index(request):
    return render(request, 'advisor_index.html',)



@login_required
@federal_auth
def region_list(request):
    total_regions = Region.objects.all().order_by('name')
    return render(request, 'all_regions.html', {'region': total_regions})


@login_required
@advisor_auth
def farmer_list(request):
    wereda = request.user.wereda
    total = Farmer.objects.filter(wereda=wereda).order_by('name')
    return render(request, 'farmer_list.html', {'farmer': total})


# class add_farmer(CreateView):
#     model = Farmer
#     template_name = "add_farmer.html"
#     success_url = "farmer"
#     fields = '__all__'

@login_required
@advisor_auth
def add_farmer(request):
    if request.method =="POST":
        form = AddFarmer(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.region = request.user.region
            post.zone = request.user.zone
            post.wereda = request.user.wereda
            post.save()

            messages.success(request, "farmer "+post.name+" was added successfully.")
            return redirect('farmer_list')
    else:
        form = AddFarmer()
    return render(request, 'add_farmer.html', {'form': form})



@login_required
@advisor_auth
def edit_farmer(request, farmer_id):
    farmer = Farmer.objects.get(pk=farmer_id)
    if request.method == "POST":
        form = EditFarmer(request.POST, request.FILES, instance=farmer)
        if form.is_valid():
            post = form.save(commit=False)
            
            post.save()
            
            messages.success(request, "The farmer "+farmer.name+" was update successfully.") 
            return redirect('farmer_list')    
                
    else:
        form = EditFarmer(instance=farmer)
    return render(request, 'edit_farmer.html', 
                 {'form': form})



@login_required
@advisor_auth
def crop_list_fun(request):
    total_crops = Crop.objects.all().order_by('name')
    return render(request, 'crop_list.html', {'crop': total_crops})



@login_required
@advisor_auth
def add_crop(request):
    if request.method =="POST":
        form = AddCrop(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            post.save()

            messages.success(request, "crop "+post.name+" was added successfully.")
            return redirect('crop_list')
    else:
        form = AddCrop()
    return render(request, 'add_crop.html', {'form': form})



@login_required
@advisor_auth
def edit_crop(request, crop_id):
    crop = Crop.objects.get(pk=crop_id)
    if request.method == "POST":
        form = EditCrop(request.POST, request.FILES, instance=crop)
        if form.is_valid():
            post = form.save(commit=False)
            
            post.save()
            
            messages.success(request, "The crop "+crop.name+" was update successfully.") 
            return redirect('crop_list')    
                
    else:
        form = EditCrop(instance=crop)
    return render(request, 'edit_crop.html', 
                 {'form': form})




@login_required
@advisor_auth
def crop_production_list(request):
    total_crops = CropProduction.objects.all()
    return render(request, 'crop_production_list.html', {'crop': total_crops})



@login_required
@advisor_auth
def add_crop_production(request):
    if request.method =="POST":
        form = AddCropProduction(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            post.save()

            messages.success(request, "crop production was added successfully.")
            return redirect('crop_production_list')
    else:
        form = AddCropProduction()
    return render(request, 'add_crop_production.html', {'form': form})



@login_required
@advisor_auth
def edit_crop_production(request, crop_id):
    crop = CropProduction.objects.get(pk=crop_id)
    if request.method == "POST":
        form = EditCropProduction(request.POST, request.FILES, instance=crop)
        if form.is_valid():
            post = form.save(commit=False)
            
            post.save()
            
            messages.success(request, "The crop production was update successfully.") 
            return redirect('crop_production_list')    
                
    else:
        form = EditCropProduction(instance=crop)
    return render(request, 'edit_crop_production.html', 
                 {'form': form})





@login_required
@advisor_auth
def livestock_list(request):
    total_livestock = Livestock.objects.all().order_by('name')
    return render(request, 'livestock_list.html', {'livestock': total_livestock})



@login_required
@advisor_auth
def add_livestock(request):
    if request.method =="POST":
        form = AddLivestock(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            post.save()

            messages.success(request, "livestock "+post.name+" was added successfully.")
            return redirect('livestock_list')
    else:
        form = AddLivestock()
    return render(request, 'add_livestock.html', {'form': form})



@login_required
@advisor_auth
def edit_livestock(request, livestock_id):
    livestock = Livestock.objects.get(pk=livestock_id)
    if request.method == "POST":
        form = EditLivestock(request.POST, request.FILES, instance=livestock)
        if form.is_valid():
            post = form.save(commit=False)
            
            post.save()
            
            messages.success(request, "The livestock "+livestock.name+" was update successfully.") 
            return redirect('livestock_list')    
                
    else:
        form = EditLivestock(instance=livestock)
    return render(request, 'edit_livestock.html', 
                 {'form': form})



@login_required
@advisor_auth
def livestock_production_list(request):
    total_livestock = LivestockProduction.objects.all()
    return render(request, 'livestock_production_list.html', {'livestock': total_livestock})



@login_required
@advisor_auth
def add_livestock_production(request):
    if request.method =="POST":
        form = AddLivestockProduction(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            post.save()

            messages.success(request, "livestock production was added successfully.")
            return redirect('livestock_production_list')
    else:
        form = AddLivestockProduction()
    return render(request, 'add_livestock_production.html', {'form': form})



@login_required
@advisor_auth
def edit_livestock_production(request, livestock_id):
    livestock = LivestockProduction.objects.get(pk=livestock_id)
    if request.method == "POST":
        form = EditLivestockProduction(request.POST, request.FILES, instance=livestock)
        if form.is_valid():
            post = form.save(commit=False)
            
            post.save()
            
            messages.success(request, "The livestock production was update successfully.") 
            return redirect('livestock_production_list')    
                
    else:
        form = EditLivestockProduction(instance=livestock)
    return render(request, 'edit_livestock_production.html', 
                 {'form': form})



@login_required
def federal_statistics(request):
    region = Region.objects.all()

    return render(request, 'view_stats_filter.html', {"region": region})



@login_required
def region_stats(request, pk):
    
    if pk == 0:
        
        data = CropProduction.objects.all()
    else:
        
        region = Region.objects.get(pk=pk)
        data = CropProduction.objects.filter(farmer__region=region)

    crop_lists = set()
    for i in data:
        crop_lists.add(i.crop.name)
    crop_map = {i: 0 for i in crop_lists}
    for i in data:
        crop_map[i.crop.name] += i.quantity
    crop_tuple = [(i, crop_map[i]) for i in crop_map]
    crop_type = [i for i,j in crop_tuple]
    qua  = [j for i,j in crop_tuple]
    orga_data = {'Crop':  crop_type, 'Production': qua,}
    if not crop_type:
        return render(request, "region_stats.html", {'data': None})
    #plt.plot(orga_data)

    # fig = plt.gcf()
    plt.figure(figsize=(13,10))
    sns.barplot("Crop","Production",data=orga_data)
    plt.xticks(rotation=90)
    # plt.show()
    fig = plt.gcf()
    #sns.barplot("Crop","Production",data=orga_data)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request, "region_stats.html", {'data': uri})

@login_required
@advisor_auth
def data_gazer(request):
    if request.method == "POST":
        form = DataGazer(request.POST)
        if form.is_valid():
            # post = form.save(commit=False)
            user_id = request.POST.get("ID_number")
            name = request.POST.get("name")
            area = request.POST.get("area")
            product = request.POST.get("product_type")
            quantity = request.POST.get("quantity")
            try:
                farmer = Farmer(id_number=user_id, name=name, area=area, region=request.user.region, zone=request.user.zone, wereda=request.user.wereda)
                farmer.save()
            except IntegrityError:
                farmer = Farmer.objects.get(id_number=user_id)
                farmer.area = area
                farmer.name = name
                farmer.save()

            item = Item(farmer=farmer, name=product, quantity=quantity)
            item.save()

            messages.success(request, "Successfully registered.") 
            return redirect('crop_production_data_gazer', farmer.id)    
                
    else:
        form = DataGazer()

    return render(request, 'data_gazer.html', {'form': form})

@advisor_auth
def crop_production_data_gazer(request, farmer_id):
    farmer = Farmer.objects.get(pk=farmer_id)
    if request.method =="POST":
        form = DataCropProduction(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.farmer = farmer
            post.save()

            messages.success(request, "crop production " + post.crop.name +  " was added successfully.")
            return redirect('crop_production_data_gazer', farmer_id)
    else:
        form = DataCropProduction()
    return render(request, 'crop_production_data_gazer.html', {'form': form})
