from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
#from Shared.utils import unique_slug_generator




class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email,username, password):

        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,username, password):

        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
        )
    username = models.CharField(max_length=255,)
    selling_point = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):

        return self.username

    def get_short_name(self):

        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):

        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):

        return self.staff

    @property
    def is_admin(self):

        return self.admin

    @property
    def is_active(self):

        return self.active


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='defaultProfile.png')
    slug = models.SlugField(blank=True,null=True)
    summary = models.TextField(blank=True,null=True)

    @property
    def owner(self):
        return self.user

class ParaProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=25,blank=True)
    channel_name = models.CharField(max_length=1000,blank=True,null=True)
    def __str__(self):
        return self.user.username

class CustomerProfile(models.Model):
    user     = models.OneToOneField(User,on_delete=models.CASCADE)
    image    = models.ImageField()
    address  = models.CharField(max_length=255)
    phone    = models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):
        return self.user.username








# @receiver(pre_save, sender=Profile)
# def set_profile_slug(sender, instance, **kwargs):
#     if not instance.slug :
#         instance.slug = unique_slug_generator(instance)
