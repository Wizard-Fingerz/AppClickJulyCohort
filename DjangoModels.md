
---

# 🧩 **Django Models and Relationships**  

---

## 🔹 1. What is a Django Model?

A **Model** in Django is a **Python class** that defines the structure of your database tables.
Each attribute in the class represents a **field** in the database.

In essence, Models are the **blueprints** for your database.

---

### ✅ Example:

```python
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=200, unique = True)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

Each time you run migrations, Django creates a table like this in the database:

| id | name | age | email                                       | date_registered |
| -- | ---- | --- | ------------------------------------------- | --------------- |
| 1  | John | 22  | [john@example.com](mailto:john@example.com) | 2025-10-21      |

---

## 🔹 2. Fields in Django Models

Common field types:

| Field Type                | Description               | Example                                       |
| ------------------------- | ------------------------- | --------------------------------------------- |
| `CharField(max_length=n)` | Short text                | Name, title                                   |
| `TextField()`             | Long text                 | Description, content                          |
| `IntegerField()`          | Whole numbers             | Age, quantity                                 |
| `FloatField()`            | Decimal numbers           | Price, score                                  |
| `BooleanField()`          | True/False                | Active status                                 |
| `DateField()`             | Stores date               | Birthday                                      |
| `DateTimeField()`         | Stores date and time      | Created date                                  |
| `EmailField()`            | Email validation          | [email@example.com](mailto:email@example.com) |
| `FileField()`             | File uploads              | Profile photo                                 |
| `ImageField()`            | Image uploads             | Avatar                                        |
| `ForeignKey()`            | One-to-Many relationship  | Author of a post                              |
| `ManyToManyField()`       | Many-to-Many relationship | Students and Courses                          |
| `OneToOneField()`         | One-to-One relationship   | User ↔ Profile                                |

---

## 🔹 3. Creating and Applying Migrations

After creating a model:

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates and applies database tables.

---

## 🔹 4. Django ORM (Object Relational Mapper)

Django ORM lets you interact with the database using **Python code** — no need for raw SQL.

### Example:

```python
# Create
student = Student.objects.create(name="John", age=22, email="john@gmail.com")

# Read
students = Student.objects.all()

# Filter
young_students = Student.objects.filter(age__lt=25)

# Update
student.name = "John Doe"
student.save()

# Delete
student.delete()
```

---

## 🔹 5. Relationships Between Models

### There are three main types of relationships:

| Relationship                 | Description                                                              | Example            |
| ---------------------------- | ------------------------------------------------------------------------ | ------------------ |
| **One-to-One**               | A single record in one model is linked to one record in another model.   | User ↔ Profile     |
| **One-to-Many (ForeignKey)** | A single record in one model is linked to multiple records in another.   | Teacher → Students |
| **Many-to-Many**             | Multiple records in one model are linked to multiple records in another. | Students ↔ Courses |

---

## 🔸 A. One-to-One Relationship

Used when **each record in Model A** relates to **exactly one record in Model B**.

### Example:

User ↔ Profile

```python
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username
```

**Explanation:**

* `on_delete=models.CASCADE`: if the user is deleted, the profile is also deleted.
* Each user has exactly one profile.

---

## 🔸 B. One-to-Many Relationship (ForeignKey)

Used when **one record** in a model relates to **many** in another model.

### Example:

Teacher → Students

```python
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name
```

**Usage:**

```python
# Fetch teacher's students
teacher = Teacher.objects.get(id=1)
students = teacher.students.all()
```

---

## 🔸 C. Many-to-Many Relationship

Used when multiple records in one model relate to multiple records in another.

### Example:

Students ↔ Courses

```python
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, related_name='students')

    def __str__(self):
        return self.name
```

**Usage:**

```python
# Add course to student
course = Course.objects.get(id=1)
student = Student.objects.get(id=2)
student.courses.add(course)

# View student's courses
student.courses.all()

# View all students in a course
course.students.all()
```

---

## 🔹 6. Model Meta Options

You can customize model behavior using the `Meta` class inside your model.

```python
class Student(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Students"
```

---

## 🔹 7. Model Methods

You can define custom methods inside models for extra logic.

```python
class Student(models.Model):
    name = models.CharField(max_length=100)
    marks = models.IntegerField()

    def is_passed(self):
        return self.marks >= 40
```

Usage:

```python
student = Student.objects.get(id=1)
student.is_passed()   # True or False
```

---

## 🔹 8. Choices Field Example

When a field should only accept certain options:

```python
class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
```

---

## 🔹 9. Working with File and Image Fields

```python
class Document(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

Make sure you set in **settings.py**:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

And in **urls.py**:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 🔹 10. Related Names and QuerySets

The `related_name` attribute allows reverse access to relationships.

Example:

```python
teacher.students.all()
```

comes from `related_name='students'`.

Without it, Django defaults to `student_set`.

---

## 🔹 11. Model Inheritance

Django allows **model inheritance** for shared fields.

### Example:

```python
class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    class Meta:
        abstract = True  # No table for Person

class Teacher(Person):
    subject = models.CharField(max_length=50)

class Student(Person):
    grade = models.CharField(max_length=10)
```

---

## 🔹 12. Using Django Admin for Models

Register models in `admin.py`:

```python
from django.contrib import admin
from .models import Student, Teacher, Course

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
```

Now you can manage them visually at:

```
http://127.0.0.1:8000/admin/
```

---

## 🔹 13. Real-World Example (School Management System)

### Models

* **Teacher** → teaches many **Students** (ForeignKey)
* **Student** → takes many **Courses** (ManyToMany)
* **Profile** → belongs to one **User** (OneToOne)

This combination is exactly how you structure complex systems like hospital management, e-commerce, or edutech platforms.

---

## 🎯 **Learning Outcomes**

After this module, students should be able to:
✅ Define and migrate Django models.
✅ Use Django ORM for CRUD operations.
✅ Establish and manage all three relationship types.
✅ Customize models with Meta and methods.
✅ Handle files, images, and choices.
✅ Navigate relationships in both directions.

---

