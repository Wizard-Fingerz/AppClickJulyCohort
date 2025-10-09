# 📘 Django Course Teaching Notes

---

## 1. Creation of Virtual Environment and Installation of Django

**Objective:** Understand the need for virtual environments and install Django.

* **What is a Virtual Environment?**

  * An isolated environment for Python projects.
  * Prevents dependency conflicts between projects.

* **Steps:**

  ```bash
  # Create a virtual environment with the default Python version
  python -m venv env

  VirtualEnv venv

  # OR, to create a virtual environment with a specific Python version (e.g., Python 3.10)
  python3.10 -m venv env

  # Activate the environment
  # Windows
  env\Scripts\activate
  # Mac/Linux
  source env/bin/activate

  Incas ths oes not work immediately... Try to install Virtual env
  pip install virtualenv

Perfect 👍 — let’s focus on the **bypass method** since you’re hitting authorization issues. This way you don’t need admin rights, and it only affects your current PowerShell session.

---

# 🔹 How to Bypass PowerShell Execution Policy

### 1. Open PowerShell

* Press **Win + R**
* Type `powershell` and hit **Enter**

---

### 2. Start PowerShell with Bypass Policy

Instead of changing execution policy permanently, run:

```powershell
powershell -ExecutionPolicy Bypass
```

This opens a new PowerShell session where script restrictions are ignored.

---

### 3. Navigate to Your Project Folder

```powershell
cd C:\Users\YourName\Desktop\myproject
```

---

### 4. Activate Your Virtual Environment

```powershell
.\env\Scripts\activate
```

Now you should see:

```
(env) PS C:\Users\YourName\Desktop\myproject>
```

✅ Your virtual environment is active.

---

### 5. Deactivate When Done

```powershell
deactivate
```

---

⚡ **Tip for Students:**
If bypassing feels confusing, just use **Command Prompt**:

```cmd
env\Scripts\activate.bat
```

No execution policy errors will show there.



  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process



  # Install Django
  pip install django

  # (Recommended) Use a requirements.txt file to manage dependencies

  # Create a requirements.txt file with Django listed
  echo django > requirements.txt

  # OR, if you've already installed Django and want to generate requirements.txt with all installed packages
  pip freeze > requirements.txt

  # Install all dependencies from requirements.txt
  pip install -r requirements.txt
  ```

* **Check Installation:**

  ```bash
  django-admin --version
  ```

✅ **Exercise:** Students create their own environment and install Django.

---

## 2. Create Project & App using Django

**Objective:** Learn to set up Django projects and apps.

* **Create a Project:**

  ```bash
  django-admin startproject myproject
  cd myproject
  ```

* **Run the Server:**

  ```bash
  # Run the server on the default port (8000)
  python manage.py runserver

  # OR, to specify a custom port (e.g., 8080)
  python manage.py runserver 8080

  # You can also specify the IP address and port (e.g., accessible on all network interfaces)
  python manage.py runserver 0.0.0.0:8000
  ```

* **Create an App:**

  ```bash
  python manage.py startapp blog
  ```

* **Register App:** Add `'blog'` to `INSTALLED_APPS` in `settings.py`.

✅ **Exercise:** Create a project called `school` and an app called `students`.

---

## 3. Introduction to Django MVT (Model-View-Template)

**Objective:** Understand Django’s architecture.

* **Model:** Handles database structure.
* **View:** Handles business logic.
* **Template:** Handles presentation (HTML).

📌 **Diagram:**

```
User → URL → View → Model → Template → Response
```

✅ **Example:** Create a `Student` model, write a view to display student data, and connect it to a template.

---

## 4. Django Views

* **Function-Based Views:**

  ```python
  from django.http import HttpResponse

  def home(request):
      return HttpResponse("Welcome to Django!")
  ```

* **Class-Based Views:**

  ```python
  from django.views import View
  from django.http import HttpResponse

  class HomeView(View):
      def get(self, request):
          return HttpResponse("Hello from Class-Based View")
  ```

✅ **Exercise:** Write a view that displays your name.

---

## 5. Django URLs

* **Basic URL Mapping:**

  ```python
  from django.urls import path
  from . import views

  urlpatterns = [
      path('', views.home, name='home'),
      path('about/', views.about, name='about'),
  ]
  ```

* **Include in Project URLs:**

  ```python
  from django.urls import include, path

  urlpatterns = [
      path('', include('blog.urls')),
  ]
  ```

✅ **Exercise:** Create URLs for `home`, `about`, and `contact`.

---

## 6. Django Templates

* **Template Example:**
  `templates/home.html`

  ```html
  <h1>Welcome, {{ name }}</h1>
  ```

* **Add Template Directory to Settings:**

  In your Django project's `settings.py`, add the path to your templates folder in the `TEMPLATES` setting:

  ```python
  import os

  TEMPLATES = [
      {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'DIRS': [os.path.join(BASE_DIR, 'templates')],
          'APP_DIRS': True,
          'OPTIONS': {
              'context_processors': [
                  # ... default context processors ...
              ],
          },
      },
  ]
  ```

  This tells Django to look for templates in the `templates` directory at the root of your project.

* **Render Template in View:**

  ```python
  from django.shortcuts import render

  def home(request):
      return render(request, 'home.html', {'name': 'John'})
  ```

✅ **Exercise:** Create a template that displays your favorite subject.

---

## 7. Django Models

* **Example Model:**

  ```python
  from django.db import models

  class Student(models.Model):
      name = models.CharField(max_length=100)
      age = models.IntegerField()
      email = models.EmailField()
  ```

* **Apply Migrations:**

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

✅ **Exercise:** Create a `Teacher` model with `name`, `subject`, and `email`.

---

## 8. Conditions in Django

* **Template Condition Example:**

  ```html
  {% if student.age >= 18 %}
      <p>Adult</p>
  {% else %}
      <p>Minor</p>
  {% endif %}
  ```

✅ **Exercise:** Show if a student passed (score ≥ 50) or failed.

---

## 9. Loops & Include in Django

* **Loop Example:**

  ```html
  {% for student in students %}
      <li>{{ student.name }}</li>
  {% endfor %}
  ```

* **Include Example:**

  ```html
  {% include 'navbar.html' %}
  ```

✅ **Exercise:** Loop through a list of 5 subjects and display them.

---

## 10. Django QuerySets

* **Examples:**

  ```python
  students = Student.objects.all()
  student = Student.objects.get(id=1)
  filtered = Student.objects.filter(age__gte=18)
  ```

✅ **Exercise:** Fetch all students above age 20.

---

## 11. CRUD Operations

* **Create:**

  ```python
  Student.objects.create(name="John", age=20, email="john@example.com")
  ```
* **Read:** `Student.objects.all()`
* **Update:**

  ```python
  student = Student.objects.get(id=1)
  student.name = "Jane"
  student.save()
  ```
* **Delete:**

  ```python
  student.delete()
  ```

✅ **Exercise:** Perform CRUD operations on the `Teacher` model.

---

## 12. Static File Management

* **Setup:**
  In `settings.py`

  ```python
  STATIC_URL = '/static/'
  STATICFILES_DIRS = [BASE_DIR / "static"]
  ```

* **Use in Template:**

  ```html
  {% load static %}
  <img src="{% static 'images/logo.png' %}" alt="Logo">
  ```

✅ **Exercise:** Add a CSS file to style your home page.

---

## 13. Error Handling

* **Custom 404 & 500 Pages:**

  * Create `404.html` and `500.html` in `templates/`.
  * Enable `DEBUG = False` in `settings.py`.

* **Try/Except in Views:**

  ```python
  try:
      student = Student.objects.get(id=1)
  except Student.DoesNotExist:
      student = None
  ```

✅ **Exercise:** Create a custom error page for “Student Not Found.”

---

## 14. Django REST Framework (DRF)

* **Install:**

  ```bash
  pip install djangorestframework
  ```

* **Add to `INSTALLED_APPS`:**

  ```python
  'rest_framework',
  ```

* **Simple API View:**

  ```python
  from rest_framework.response import Response
  from rest_framework.decorators import api_view

  @api_view(['GET'])
  def api_home(request):
      return Response({"message": "Hello API"})
  ```

✅ **Exercise:** Build an API that returns all students in JSON format.

---

# ✅ Teaching Flow Suggestion

* Week 1: Virtual Env, Installation, Project/App
* Week 2: MVT, Views, URLs
* Week 3: Templates, Models
* Week 4: Conditions, Loops, QuerySets
* Week 5: CRUD, Static Files
* Week 6: Error Handling, DRF
---

