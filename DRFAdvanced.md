
---

# 🧩 **Advanced Django REST Framework Topics**

---

## 🔹 1. Token Authentication with `rest_framework.authtoken`

### What is Token Authentication?

Instead of using sessions, APIs often use **tokens** to identify users.
Each user gets a **unique token** upon login, and this token must be sent with every API request.

---

### Step 1: Install and Add to Settings

```bash
pip install djangorestframework
pip install djangorestframework-authtoken
```

Then add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
]
```

---

### Step 2: Run Migrations

```bash
python manage.py migrate
```

This creates a `Token` table in the database.

---

### Step 3: Create a Token Automatically for New Users

You can use Django’s signals:

```python
# students/signals.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

Register in `apps.py` or `__init__.py`:

```python
default_app_config = 'students.apps.StudentsConfig'
```

---

### Step 4: Use TokenAuthentication in Views

In `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

---

### Step 5: Obtain a Token via API

Add to your `urls.py`:

```python
from rest_framework.authtoken import views

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token),
]
```

Now, POST to `/api-token-auth/` with:

```json
{
  "username": "john",
  "password": "mypassword"
}
```

You’ll get:

```json
{"token": "9f1d43c20e9e29a9c0fa4a17a2d52b7e9f7f3e20"}
```

Then include this token in future requests:

```
Authorization: Token 9f1d43c20e9e29a9c0fa4a17a2d52b7e9f7f3e20
```

---

## 🔹 2. Pagination, Filtering & Search

### Pagination

In `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

Result:

```json
{
  "count": 45,
  "next": "http://127.0.0.1:8000/api/students/?page=2",
  "previous": null,
  "results": [...]
}
```

---

### Filtering & Searching

Install:

```bash
pip install django-filter
```

Add to settings:

```python
INSTALLED_APPS = [
    ...
    'django_filters',
]
```

Use in `views.py`:

```python
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'age']
    search_fields = ['name', 'email']
    ordering_fields = ['age', 'date_enrolled']
```

Now you can query like:

```
/api/students/?course=Computer Science
/api/students/?search=john
/api/students/?ordering=-age
```

---

## 🔹 3. Custom API Endpoints with `@action` Decorator

You can define **custom routes** beyond standard CRUD operations.

Example:

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        student = self.get_object()
        return Response({'name': student.name, 'course': student.course})

    @action(detail=False, methods=['get'])
    def top_students(self, request):
        top_students = Student.objects.filter(age__gt=20)
        serializer = self.get_serializer(top_students, many=True)
        return Response(serializer.data)
```

Endpoints:

```
/api/students/1/profile/
/api/students/top_students/
```

---

## 🔹 4. Permissions & Role-Based Access

### Basic Permissions

```python
from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_staff
```

Then in views:

```python
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
```

### Built-in Permission Classes

* `AllowAny`
* `IsAuthenticated`
* `IsAdminUser`
* `IsAuthenticatedOrReadOnly`

---

## 🔹 5. Serializing Nested Relationships

### Example: A `Course` model related to `Student`

```python
class Course(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

class Student(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, related_name='students', on_delete=models.CASCADE)
```

Serializer:

```python
class CourseSerializer(serializers.ModelSerializer):
    students = serializers.StringRelatedField(many=True)
    class Meta:
        model = Course
        fields = ['id', 'title', 'code', 'students']
```

Now GET `/api/courses/` returns nested data:

```json
{
  "id": 1,
  "title": "Computer Science",
  "students": ["John", "Mary"]
}
```

---

## 🔹 6. Versioning Your APIs

In `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
```

In `urls.py`:

```python
urlpatterns = [
    path('api/<str:version>/students/', include('students.urls')),
]
```

Now you can have:

```
/api/v1/students/
/api/v2/students/
```

---

## 🔹 7. Deploying Django REST API with Swagger on Render or Vercel

### Render (Recommended for Backend)

1. Push your code to GitHub.
2. Go to [https://render.com](https://render.com)
3. Create a **New Web Service** → select your repository.
4. Set:

   * **Build Command:**

     ```
     pip install -r requirements.txt
     python manage.py migrate
     ```
   * **Start Command:**

     ```
     gunicorn school_api.wsgi
     ```
5. Add your environment variables (e.g., `DEBUG=False`, `SECRET_KEY`).
6. Click **Deploy**.
7. Visit your Render URL:

   ```
   https://school-api.onrender.com/swagger/
   ```

### Vercel (Not Ideal for Django)

Vercel is for frontends (Next.js, React). For Django APIs, you can use:

* **Render**
* **Railway.app**
* **PythonAnywhere**
* **Heroku (via Docker)**

---

# ✅ Summary Table

| Topic                  | Description                             | Example                   |
| ---------------------- | --------------------------------------- | ------------------------- |
| **Token Auth**         | Secure endpoints with token-based login | `/api-token-auth/`        |
| **Pagination**         | Break long lists into pages             | `?page=2`                 |
| **Filtering/Search**   | Query by fields                         | `?search=john`            |
| **Custom Endpoints**   | Add special actions                     | `/students/top_students/` |
| **Permissions**        | Control access by role                  | Admin-only POST           |
| **Nested Serializers** | Handle related data                     | Course → Students         |
| **Versioning**         | Maintain multiple API versions          | `/api/v1/` vs `/api/v2/`  |
| **Deployment**         | Host APIs online                        | Render                    |

---

## 🎯 Learning Outcome

By the end of this module, your students should be able to:

* Secure APIs using token authentication.
* Implement pagination, search, and filtering.
* Create custom endpoints for specific logic.
* Build role-based permissions.
* Handle nested data with serializers.
* Maintain multiple versions of the same API.
* Deploy their RESTful API and document it with Swagger.

---
