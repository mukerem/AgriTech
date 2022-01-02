from django.urls import path, include
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('home/', views.homepage, name='homepage'),
    path('crop_prediction/', views.crop_prediction_view, name='crop_prediction'),
    path('data-gazer/', views.data_gazer, name="data_gazer"),
    path('crop-data-gazer/<farmer_id>/', views.crop_production_data_gazer, name="crop_production_data_gazer"),

    path('federal/', views.federalGovtview, name='federal'),
    path('region/', views.region_list, name='region'),
    path('zone/<int:pk>', views.zoneListview, name='zone'),
    path('zone/<int:pk>/woredas/', views.woredaListview, name='woreda'),
    path('zone/woredas/<int:pk>/advisors', views.advisorListview, name='advisor'),
    path('advisors/create', views.AdvisorCreateView.as_view(), name='create-advisor'),
    path('advisors/edit/<int:pk>', views.EditAdvisorCreateView.as_view(), name='edit-advisor'),
    path('zone/create', views.AddZoneView.as_view(), name='create-zone'),
    path('zone/edit/<int:pk>', views.EditZoneView.as_view(), name='edit-zone'),
    path('woreda/create', views.AddWoredaView.as_view(), name='add-woreda'),
    path('woreda/edit/<int:pk>', views.EditWoredaView.as_view(), name='edit-woreda'),
    path('add_region/', views.AddRegionView.as_view(), name='add-region'),
    path('region/edit/<int:pk>', views.EditRegionView.as_view(), name='edit-region'),
    path('farmer/', views.farmer_list, name='farmer_list'),
    path('add-farmer/', views.add_farmer, name='add_farmer'),
    path('edit-farmer/<int:farmer_id>/', views.edit_farmer, name='edit_farmer'),
    path('crop/', views.crop_list_fun, name='crop_list'),
    path('add-crop/', views.add_crop, name='add_crop'),
    path('edit-crop/<int:crop_id>/', views.edit_crop, name='edit_crop'),
    path('crop_production/', views.crop_production_list, name='crop_production_list'),
    path('add-crop_production/', views.add_crop_production, name='add_crop_production'),
    path('edit-crop_production/<int:crop_id>/', views.edit_crop_production, name='edit_crop_production'),
    path('livestock/', views.livestock_list, name='livestock_list'),
    path('add-livestock/', views.add_livestock, name='add_livestock'),
    path('edit-livestock/<int:livestock_id>/', views.edit_livestock, name='edit_livestock'),
    path('livestock_production/', views.livestock_production_list, name='livestock_production_list'),
    path('add-livestock_production/', views.add_livestock_production, name='add_livestock_production'),
    path('edit-livestock_production/<int:livestock_id>/', views.edit_livestock_production, name='edit_livestock_production'),
    path('federal/regions/', views.region, name='federal_region'),
    # path('region/zone/<int:pk>/woreda', views.woreda, name='woreda'),
    # path('woreda/<int:pk>/field-advisors/', views.field_advisor, name='advisor'),
    path('advisor/', views.advisor_index, name="advisor_index"),
    path('statistics/', views.federal_statistics, name="statistics"),
    path('region_stats/<int:pk>/', views.region_stats, name="region_stats"),
    path('advisor/', views.advisor_index, name="advisor_index")
]