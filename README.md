# Blogs

### Create Environment
Create a virtual environment to isolate our package dependencies locally.


    python3 -m venv virtualenv


Activate virtual environment


    ./virtualenv/Scripts/activate  

OR

    source env/bin/activate
 

### phpmyadmin


    sudo service apache2 stop
    sudo /opt/lampp/lampp start


Other way phpmyadmin


      # stop mysql
      sudo /etc/init.d/mysql stop
      
      # stop apache2 
      sudo /etc/init.d/apache2 stop
      sudo service apache2 stop
      
      sudo /opt/lampp/lampp start


### requirements file

Link: \
https://intellipaat.com/community/31672/how-to-use-requirements-txt-to-install-all-dependencies-in-a-python-project


To check how many packages install in virtual

    pip freeze


create requirements.txt


    pip freeze > requirements.txt


For install requirements.txt Packages


    pip install -r requirements.txt


##### Install Django and Django REST framework into the virtual environment


    pip install django==4.2
    pip install djangorestframework


Check django version

    python -m django --version


------------------------------------------------------------------------------
## Set up a new project
project_name ==> always config


    django-admin startproject config .


---
### configure settings.py for production and development
- Create settings python package(always name is settings).
- Move settings.py file in settings packages and name this file is base.py.
- Also, create .env, development.py, production.py, s3utils.py


#### Project Structure
    
    BlogsProjectsTasks ==> Project Name
        - blogs ==> App Packages
            - accounts
                - auth_backends
                __init__
                admin.py
                apps.py
                ...
            - templates
                - accounts
                    - forgot-password.html
                    - forgot-password-success.html
            - utils
        - config ==> Project Directory
            __init__.py
            asgi.py
            settings.py
            urls.py
            wsgi.py
        - media
        - virtualenv      
        - db.sqlite3
        .gitignore
        manage.py
        README.md
        requirements.txt

---
#### Now set up the apps
- INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS\

- DJANGO_APPS => is default app\

- THIRD_PARTY_APPS => is module/packages for developer created\

- LOCAL_APPS => is created by developer\


#### Database Setup
Link:- https://docs.djangoproject.com/en/4.2/ref/settings/#databases


    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tasks_blogs_projects',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }



#### drf_secure_token Setup
Link:- https://pypi.org/project/drf-secure-token/


    THIRD_PARTY_APPS = [
        "rest_framework",  # pip install djangorestframework
        "drf_secure_token",  # pip install drf-secure-token
    ]


--

    MIDDLEWARE = [
         ...
        'drf_secure_token.middleware.UpdateTokenMiddleware',
    ]


--


    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.BasicAuthentication',
            'drf_secure_token.authentication.SecureTokenAuthentication',
         ]
    }


## Create User Models
Link:- https://testdriven.io/blog/django-custom-user-model/


    from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
    from django.utils.translation import gettext_lazy as _
    from phonenumber_field.modelfields import PhoneNumberField
    
    class User(AbstractBaseUser, PermissionsMixin):
        ...
        
        USERNAME_FIELD = "username"
        REQUIRED_FIELDS = ["email",]
    
        objects = UserManager()


- Phone Number Field In User models


    pip install django-phonenumber-field
    pip install phonenumbers


- Image In User Models


    # pip install Pillow
    photo = models.ImageField(
        upload_to='accounts/',
        null=True,
        blank=True,
        default="accounts/profile_default.png"
    )


- Create media/accounts/ directory
Link:- https://codinggear.org/how-to-upload-images-in-django/


    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL = '/media/'


- config/urls.py


    from django.conf import settings
    from django.conf.urls.static import static
    from django.contrib import admin
    from django.urls import path, include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        # path("", include("accounts.urls")),
    ]
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


- settings.py


    AUTH_USER_MODEL = "accounts.User"


- Now Migrations for user models


    python manage.py makemigrations
    python manage.py migrate


- Create Superuser


    python manage.py createsuperuser


- Resister User models
accounts/admin.py



#### Filter and Search APIs
Link:- https://django-filter.readthedocs.io/en/latest/guide/install.html


    pip install django-filter

--

    INSTALLED_APPS = [
        ...
        'django_filters',
    ]


--

    from django_filters import rest_framework as filters
    
    class ProductList(generics.ListAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        filter_backends = (filters.DjangoFilterBackend,)
        filterset_fields = ('category', 'in_stock')


#### Create Apis for Users and Auth

- Registrations APIs




