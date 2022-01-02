
from django.utils.safestring import mark_safe
from django.core.exceptions  import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.timezone import now
# Create your models here.
from datetime import datetime

class Role(models.Model):
    role = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20)
    def __str__(self):
        return self.short_name


class Region(models.Model):
    name = models.CharField(max_length=200)
    flag = models.ImageField(upload_to='', null=True, blank=True)
    area = models.PositiveIntegerField(null=True, blank=True)
    population = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return self.name
        

class Zone(models.Model):
    name = models.CharField(max_length=200)
    region =  models.ForeignKey(Region, on_delete=models.CASCADE)
    area = models.PositiveIntegerField(null=True, blank=True)
    population = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return self.name



class Wereda(models.Model):
    name = models.CharField(max_length=200)
    zone =  models.ForeignKey(Zone, on_delete=models.CASCADE)
    area = models.PositiveIntegerField(null=True, blank=True)
    population = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, username, password, name=' ', role=None):
     
        if not username:
            raise ValueError('Users must have an user name')
        
        if not name:
            raise ValueError('Users must have an name')

        if not role:
            raise ValueError('Users must have a role')

        user = self.model(
            username=username,
            name=name,
            role=role,
            register_date=timezone.now().date(),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, password):
        """
        Creates and saves a superuser with the given username and password
        """
        role = Role.objects.get(short_name='super')
        
        user = self.create_user(
            username=username,
            name=' ',
            password=password,
            role=role,
        )
        
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(verbose_name='username', max_length=255,unique=True)
    name = models.CharField(max_length=200)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,15}$',
        message='Phone number must be entered in the format : 09******** or +2519******** up to 15 digits allowed',
        )
        
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, blank=True, null=True)
    wereda = models.ForeignKey(Wereda, on_delete=models.CASCADE, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender =  models.CharField(max_length=200, choices=(("male", "male"), ("female", "female")))
    register_date = models.DateField(default = now)
    education_level = models.CharField(max_length=200, blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        # return self.username
        return self.name
        
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        role = Role.objects.get(short_name='super')
        return self.role == role


class AdvisorWereda(models.Model):
    advisor = models.ForeignKey(User, on_delete=models.CASCADE)
    wereda = models.ForeignKey(Wereda, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s at wereda %s" % (self.advisor.name, self.wereda.name)

class Farmer(models.Model):
    id_number = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,15}$',
        message='Phone number must be entered in the format : 09******** or +2519******** up to 15 digits allowed',
        )
        
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    wereda = models.ForeignKey(Wereda, on_delete=models.CASCADE)
    # date_of_birth = models.DateField(blank=True, null=True)
    # gender =  models.CharField(max_length=200, choices=(("male", "male"), ("female", "female")))
    # education_level = models.CharField(max_length=200, blank=True, null=True)
    # income = models.PositiveIntegerField()
    area = models.PositiveIntegerField()
    # family_size = models.PositiveIntegerField()
    # register_date = models.DateField(default = now)

    def __str__(self):
        # return self.username
        return self.name

class Crop(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Livestock(models.Model):
    name = models.CharField(max_length=200,  unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class CropProduction(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.PositiveIntegerField(default=datetime.now().year)

    class Meta:
        unique_together = ('crop', 'farmer', 'date')

    def __str__(self):
        return "%s on %s" % (self.farmer, self.crop)

class LivestockProduction(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    livestock = models.ForeignKey(Livestock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField(default=now)

    def __str__(self):
        return "%s on %s" % (self.farmer, self.livestock)


class Training(models.Model):
    title = models.CharField(max_length=200)
    farmer = models.ManyToManyField(Farmer)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    video = models.FileField(upload_to='', null=True, blank=True)
    place = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Item(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    date = models.DateField(default=now)
    
    def __str__(self):
        return self.name
