
---

# 🧩 **Django REST Framework (DRF) and API Documentation with Swagger**

---

## 🔹 1. Introduction to REST and APIs

### What is an API?

**API (Application Programming Interface)** allows two applications to communicate and exchange data.

### What is a REST API?

**REST (Representational State Transfer)** is an architectural style for designing networked applications.

REST APIs use:

* **HTTP Methods** — `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
* **Endpoints** — e.g., `/api/users/`, `/api/posts/1/`
* **JSON** as data format (usually)

### Why Use Django REST Framework (DRF)?

Django REST Framework is a powerful toolkit built on Django that simplifies:

* Creating RESTful APIs
* Serialization of models
* Authentication & permissions
* Pagination
* API documentation & testing

---

## 🔹 2. Installing Django REST Framework

Make sure your virtual environment is active, then install:

```bash
pip install djangorestframework
```

Add it to your **settings.py**:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

---

## 🔹 3. Setting Up a Django REST API Project

### Example: Building a Student Management API

#### Step 1: Create a Project

```bash
django-admin startproject school_api
cd school_api
```

#### Step 2: Create an App

```bash
python manage.py startapp students
```

#### Step 3: Add App to Settings

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'students',
]
```

---

## 🔹 4. Models (students/models.py)

Define your model just like in a normal Django app:

```python
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=100)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

---

## 🔹 5. Serializer (students/serializers.py)

Serializers convert Django models ↔ JSON data.

```python
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
```

---

## 🔹 6. Views (students/views.py)

Use DRF’s `APIView` or `ViewSets`.

### Example using `ModelViewSet`

```python
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

---

## 🔹 7. URLs (students/urls.py)

Use DRF’s router to automatically generate routes.

```python
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = router.urls
```

Then include in **project urls.py**:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('students.urls')),
]
```

---

## 🔹 8. Run the Server and Test API

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/api/students/
```

You can test GET, POST, PUT, DELETE using:

* **Browser interface (DRF built-in UI)**
* **Postman**
* **Curl**
* **Swagger UI (we’ll set up next)**

---

## 🔹 9. Adding Authentication (Optional but Important)

Add in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

---

## 🔹 10. API Documentation with Swagger

API documentation helps others understand and test your endpoints visually.

### Option 1: Install **drf-yasg**

```bash
pip install drf-yasg
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'drf_yasg',
]
```

In your **project urls.py**:

```python
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="School API",
      default_version='v1',
      description="API documentation for the School Management System",
      terms_of_service="https://www.yoursite.com/policies/terms/",
      contact=openapi.Contact(email="info@yoursite.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('students.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
```

Now visit:

* Swagger UI → [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
* Redoc UI → [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

✅ You’ll see a **beautiful interactive API documentation** where you can test all endpoints directly.

---

## 🔹 11. Option 2: drf-spectacular (modern alternative)

```bash
pip install drf-spectacular
```

Add in settings:

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

In urls.py:

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

---

## 🔹 12. Advanced Topics (for Extended Lessons)

* Token Authentication with `rest_framework.authtoken`
* Pagination, Filtering & Search
* Custom API endpoints using `@action` decorator
* Permissions & Role-based access
* Serializing nested relationships (ForeignKey, ManyToMany)
* Versioning your APIs
* Deploying Django REST API with Swagger on Render or Vercel backend

---

## 🔹 13. Summary Table

| Feature               | Description                     |
| --------------------- | ------------------------------- |
| **Serializer**        | Converts Models ↔ JSON          |
| **ViewSet**           | Handles CRUD automatically      |
| **Router**            | Maps endpoints                  |
| **Swagger/Redoc**     | Auto API Documentation          |
| **Authentication**    | Secures endpoints               |
| **DRF Browsable API** | Test APIs directly from browser |

---

## ✅ **Example Folder Structure**

```
school_api/
│
├── school_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── students/
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
├── db.sqlite3
├── manage.py
```

---

## 🎯 **Outcome for Students**

After this topic, students should be able to:

* Build REST APIs using Django REST Framework
* Serialize and deserialize data
* Perform CRUD operations through API endpoints
* Secure APIs using authentication and permissions
* Document APIs using Swagger and Redoc

---

