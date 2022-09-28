
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

# BaseUserManager class never contains any field it only contains methods to manage the users
#  With BaseUserManager class we can modify the fields and set them accordingly.
# AbstractBaseUser and BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User must have a email address')
        
        if not username:
            raise ValueError('User must have a username')
# normalize_email is used to make the uppercase to lowercase if any enters any usercase.
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        # set_password is used to store the password in the encrypted form.
        user.set_password(password)
        # using is used to define which database we want to use.
        # at present we have only one database that is  as default.
        # to use the default database we write _db
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name,last_name,username,email,password=None):
        user=self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        
        user.save(using=self._db)
        return user
        
        
class User(AbstractBaseUser):
    RESTAURANT=1
    CUSTOMER=2
    
    ROLE_CHOICES=(
        (RESTAURANT,'Restuarents'),
        (CUSTOMER,'Customer')
    )
    
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=12,blank=True)
    role=models.PositiveSmallIntegerField(choices=ROLE_CHOICES,blank=True, null=True)
    
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)

    USERNAME_FIELD='email'

    REQUIRED_FIELDS=['username','first_name','last_name']
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    
    
    # it will return true if user is active, superuser or a admin
    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role
    
    objects=UserManager()
    
    
    


class UserProfile(models.Model):
    # uses one to one bacause for one user there can be only one profile and one profile can belong to one user only
    # on delete cascade means that on delete User UserProfile belonging to that user must delete automatically
    # blank and null fields are used to avoid errors because we don't know what type of value will it hold
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    # location = gismodels.PointField(blank=True, null=True, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def full_address(self):
    #     return f'{self.address_line_1}, {self.address_line_2}'

    def __str__(self):
        return self.user.email


    # def save(self, *args, **kwargs):
    #     if self.latitude and self.longitude:
    #         self.location = Point(float(self.longitude), float(self.latitude))
    #         return super(UserProfile, self).save(*args, **kwargs)
    #     return super(UserProfile, self).save(*args, **kwargs)

