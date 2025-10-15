# Django Templates — Comprehensive Teaching Note

---

## 1. Overview: What are Django Templates?

* Django templates are the presentation layer in the MVT pattern.
* Purpose: separate presentation (HTML) from view logic. Templates are HTML with template language constructs (`{{ }}`, `{% %}`).
* Templates are intentionally not full programming languages — they let you render variables, control flow, include other templates, and use filters/tags.

---

## 2. Basic Concepts & Syntax

### Variables

```html
<p>Hello, {{ user.first_name }}!</p>
```

### Filters (transform data)

```html
{{ post.title|lower }}
{{ value|default:"N/A" }}
{{ price|floatformat:2 }}
```

### Tags (logic & flow)

* Control flow:

**View Example:**

```python
from django.shortcuts import render

def welcome_view(request):
    # The user object is included in the template context by Django's authentication system
    # so we typically don't need to pass it explicitly
    return render(request, 'welcome.html')
```

**Template (welcome.html):**

```django
{% if user.is_authenticated %}
  <p>Welcome back, {{ user.username }}</p>
{% else %}
  <a href="{% url 'login' %}">Login</a>
{% endif %}
```


* For loops:

**View Example:**

```python
from django.shortcuts import render

def product_list(request):
    products = [
        {"name": "Laptop", "price": 1200},
        {"name": "Smartphone", "price": 700},
        {"name": "Headphones", "price": 150},
    ]
    return render(request, "product_list.html", {"products": products})
```

**Template (`product_list.html`):**

```django
<ul>
{% for product in products %}
  <li>{{ product.name }} — {{ product.price }}</li>
{% empty %}
  <li>No products available</li>
{% endfor %}
</ul>
```


* Include:

```django
{% include "partials/navbar.html" %}
```

* Template inheritance:

```django
{% extends "base.html" %}
{% block content %}
  <h1>Home</h1>
{% endblock %}
```

---

## 3. Template Directory Setup

* Default: `TEMPLATES` setting in `settings.py` controls loaders and dirs.

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        ...
    },
]
```

* Typical structure:

```
project/
├─ app1/
│  └─ templates/app1/...
├─ templates/
│  ├─ base.html
│  ├─ partials/
│  │  ├─ navbar.html
│  │  └─ footer.html
│  └─ pages/
│     └─ home.html
```

---

## 4. Template Inheritance — The Foundation of Reuse

`base.html` (global layout):

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{% block title %}MySite{% endblock %}</title>
  {% load static %}
  <link rel="stylesheet" href="{% static 'css/site.css' %}">
  {% block head %}{% endblock %}
</head>
<body>
  {% include 'partials/navbar.html' %}
  <main>{% block content %}{% endblock %}</main>
  {% include 'partials/footer.html' %}
  {% block scripts %}{% endblock %}
</body>
</html>
```

Child template:

```python
# views.py
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/detail.html', {'product': product})
```

```django
{# templates/product/detail.html #}
{% extends "base.html" %}
{% block title %}Product — {{ product.name }}{% endblock %}
{% block content %}
  <h1>{{ product.name }}</h1>
  <p>{{ product.description }}</p>
{% endblock %}
 

---

## 5. Passing Data: Views → Templates

* Function-based view:

```python
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    return render(request, 'product/detail.html', {'product': product, 'related': related})
```

* Class-based view:

```python
# Import the generic DetailView for class-based generic view
from django.views.generic import DetailView

# ProductDetail provides detail page for a Product instance.
# It uses the model Product, the template at product/detail.html,
# and in the template, the object will be available as "product".
class ProductDetail(DetailView):
    model = Product  # The model this view will retrieve
    template_name = 'product/detail.html'  # Which template to render
    context_object_name = 'product'  # Name to use for the object in the template context
```

---

## 6. Template Tags & Filters (Built-in)

* URL reversing: `{% url 'product_detail' product.pk %}`
* Static files: `{% load static %} <img src="{% static 'img/logo.png' %}">`
* i18n: `{% trans "Hello" %}`

---

## 7. Custom Template Tags & Filters

**When to use**: complex presentation logic that’s reused across templates.

Example filter (slugify):
`myapp/templatetags/mytags.py`

```python
from django import template
from django.utils.text import slugify

register = template.Library()

@register.filter
def make_slug(value):
    return slugify(value)
```

In template:

```django
{% load mytags %}
{{ "Hello World" | make_slug }}  {# outputs: hello-world #}
```

Example simple inclusion tag:

```python
@register.inclusion_tag('partials/recent_posts.html')
def show_recent_posts(count=5):
    from blog.models import Post
    posts = Post.objects.published()[:count]
    return {'posts': posts}
```

Use: `{% show_recent_posts 3 %}`

**Teaching tip:** demonstrate creating tags/filters, test them, and stress keeping logic in Python (not templates).

---

## 8. Context Processors

* Purpose: inject data into context for all templates (e.g., site name, cart count).
* Example: `myapp/context_processors.py`

```python
def site_info(request):
    return {'SITE_NAME': 'MyShop'}
```

In `settings.py`, add your context processor to the `TEMPLATES` `OPTIONS["context_processors"]` list:

```python
TEMPLATES = [
    {
        # ...
        'OPTIONS': {
            'context_processors': [
                # ... existing context processors ...
                'myapp.context_processors.site_info',  # add this line
            ],
        },
    },
]
```


**In your template, use the injected variable as follows:**

```django
{{ SITE_NAME }}
```


**Caution:** Avoid running heavy database queries inside context processors because context processors are executed on every template-rendered request—this can significantly slow down your site and increase database load.


---

## 9. Forms in Templates

### Using `forms` from `django.forms`

**In `forms.py`:**

```python
from django import forms
from .models import Contact  # assuming you have a Contact model

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']  # use your actual model fields
```

*If you just want a plain form, not linked to a model:*

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
```


* In view:

```python
from .forms import ContactForm

def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('contact_thanks')
    return render(request, 'contact.html', {'form': form})
```

* In template:

```django
<form method="post" novalidate>
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Send</button>
</form>
```

### Rendering field by field:

```django
<div>
  <label for="{{ form.name.id_for_label }}">Name</label>
  {{ form.name }}
  {% if form.name.errors %}
    <div class="errors">{{ form.name.errors }}</div>
  {% endif %}
</div>
```

**Tip:** Use `crispy-forms` or similar for better HTML without mixing presentation logic into forms.
### Using `crispy-forms` for Better Form Rendering

`django-crispy-forms` is a powerful, flexible way to render beautiful, customizable forms in Django **without having to hand-code much HTML in your templates**. It adds layout objects, helpers, and template packs (especially Bootstrap) to make forms more attractive and DRY.

#### 1. Install and Set Up

```bash
pip install django-crispy-forms
pip install crispy-bootstrap5   # Or crispy-bootstrap4, crispy-tailwind, etc.
```

*In `settings.py`:*

```python
INSTALLED_APPS = [
    # ...
    "crispy_forms",
    "crispy_bootstrap5",  # Or the pack you want
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

#### 2. Use in a Form

Let's rework our earlier `ContactForm`:

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    # Optionally: Add crispy helper for layout
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Submit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = self.FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Send"))
```

Or, for finer control:

```python
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit

class ContactForm(forms.Form):
    # ...fields as above...
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="col-md-6"),
                Column("email", css_class="col-md-6"),
            ),
            "message",
            Submit("submit", "Send")
        )
```

#### 3. In the Template

At the top of your template, **load the crispy_forms tags:**

```django
{% load crispy_forms_tags %}
```

Then, to render the form using all crispy magic & Bootstrap styles:

```django
<form method="post">
  {% csrf_token %}
  {{ form|crispy }}
</form>
```

#### 4. Customizing Button Placement, etc.

Crispy provides helper/layout classes to customize the form:

```python
from crispy_forms.layout import Layout, Field, Row, Column, ButtonHolder, Submit

self.helper.layout = Layout(
    Row(
        Column('name'),
        Column('email'),
    ),
    Field('message'),
    ButtonHolder(
        Submit('submit', 'Send')
    )
)
```

#### 5. Full Example

**views.py:**

```python
from .forms import ContactForm

def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # process data...
        return redirect("contact_thanks")
    return render(request, "contact.html", {"form": form})
```

**contact.html:**

```django
{% extends "base.html" %}
{% load crispy_forms_tags %}

{% block content %}
  <h2>Contact Us</h2>
  <form method="post" novalidate>
    {% csrf_token %}
    {{ form|crispy }}
  </form>
{% endblock %}
```

#### 6. ModelForms + Crispy

For model forms, everything works the same way:

```python
from .models import Product
from crispy_forms.helper import FormHelper

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
```

#### 7. Template Packs

Crispy supports several packs: `bootstrap4`, `bootstrap5`, `uni_form`, `tailwind`, etc.
Choose the pack in settings, and make sure your project includes that CSS so classes map correctly.

#### 8. Extra Tips

- You can still access fields individually (`form.name`), but `|crispy` is usually much better.
- Form errors are automatically shown/handled.
- Customize field attributes per-field (`self.fields["name"].widget.attrs["placeholder"] = ...`).

**Reference:** [https://django-crispy-forms.readthedocs.io](https://django-crispy-forms.readthedocs.io)

---

## 10. Static Files & Media in Templates

* `settings.py`:

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'     # for collectstatic in production

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

* Template usage:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/main.css' %}">
<img src="{{ product.image.url }}" alt="{{ product.name }}">
```

* For serving media in development:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 11. Pagination in Templates

* View:

```python
from django.core.paginator import Paginator

def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    return render(request, 'product/list.html', {'products': products_page})
```

* Template:

```django
{% for p in products %}
  {{ p.name }}
{% endfor %}

<div class="pagination">
  {% if products.has_previous %}
    <a href="?page={{ products.previous_page_number }}">Prev</a>
  {% endif %}
  Page {{ products.number }} of {{ products.paginator.num_pages }}
  {% if products.has_next %}
    <a href="?page={{ products.next_page_number }}">Next</a>
  {% endif %}
</div>
```

---

## 12. Template Security & Escaping

* **Django automatically escapes variables in templates to prevent XSS** (Cross Site Scripting) attacks.

  **Example:**
  ```django
  {{ user_input }}
  ```
  If `user_input` contains `<script>alert('xss')</script>`, the template will render:
  ```html
  &lt;script&gt;alert('xss')&lt;/script&gt;
  ```
  (The script tags are escaped, so the script won't execute.)

* **Using the `safe` filter:**  
  Only use the `|safe` filter if you're absolutely sure that the content cannot contain harmful scripts (i.e., it has been sanitized).

  **Correct Usage (after sanitizing):**
  ```python
  # views.py
  import bleach

  def my_view(request):
      raw_content = request.POST.get('bio', '')
      clean_content = bleach.clean(raw_content)
      return render(request, "profile.html", {"content": clean_content})
  ```
  ```django
  {# profile.html #}
  {{ content|safe }}
  ```

  Or, when rendering safe HTML generated from Markdown:
  ```python
  # views.py
  import markdown

  def blog_detail(request):
      raw_body = get_blog_body()
      html_body = markdown.markdown(raw_body, extensions=["extra"], output_format="html5")
      return render(request, "blog/detail.html", {"body": html_body})
  ```
  ```django
  {# blog/detail.html #}
  {{ body|safe }}
  ```

* **NEVER do this without sanitizing input:**
  ```django
  {{ request.POST.bio|safe }}
  ```
  Rendering unsanitized user input marked as safe can allow attackers to inject scripts.

**Key Point:**  
🔒 Always sanitize user-generated content before marking it safe.  
🔗 See: [Django docs: Output escaping](https://docs.djangoproject.com/en/stable/topics/templates/#automatic-html-escaping)

---

## 13. Performance & Caching

* Template fragment caching:

```django
{% load cache %}
{% cache 600 product_list %}
  ... expensive HTML generation ...
{% endcache %}
```

* Full-page caching (with caching middleware) for anonymous users.
* Use `select_related` / `prefetch_related` in views to reduce DB hits before rendering templates.
* Use `context` dictionaries that are small — heavy computations should be done in views or background jobs.

---

## 14. Internationalization (i18n) in Templates

* Mark strings:

```django
{% load i18n %}
{% trans "Welcome" %}
```

* Variables:

```django
{% blocktrans %}Hello {{ user.first_name }}{% endblocktrans %}
```

* Compile messages and set up translations with `makemessages` and `compilemessages`.

---

## 15. Testing Templates

* Use `django.test.Client` to render views and assert content:

```python
from django.test import TestCase
from django.urls import reverse

class HomeViewTests(TestCase):
    def test_home_contains_site_name(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "MyShop")
```

* For template tags/filters, write unit tests that call the tag functions directly or render a small template snippet in test.

---

## 16. Advanced Patterns for Full-Scale Apps

* **Componentization**: partials/blocks for nav, footer, product card, filters.
* **Reusable apps**: keep generic templates under `app_name/templates/app_name/` to avoid collisions.
* **Design system**: keep CSS and JS organized (e.g., Tailwind or Bootstrap). Use `static/` for assets.
* **Client-side interactivity**: small JS sprinkles for UX (AJAX forms, live search) but keep main rendering server-side.
* **Progressive Enhancement**: render full HTML on server, then enhance with JS.

---

## 17. Example: Build a Mini E-commerce App (MyShop) — Templates-focused

### Data models (simplified)

```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
```

### Views

* `product_list`, `product_detail`, `category_list`, search view — pass QuerySets to templates.

### Templates

* `base.html`, `partials/navbar.html`, `partials/product_card.html`, `product/list.html`, `product/detail.html`, `cart/detail.html`, `checkout.html`
* Use template inheritance, include, pagination, forms for checkout, CSRF token for POSTs.

### Example `product_card` partial:

```django
<div class="product-card">
  <a href="{% url 'product_detail' product.slug %}">
    <img src="{{ product.image.url }}" alt="{{ product.name }}">
    <h3>{{ product.name }}</h3>
    <p>{{ product.price|floatformat:2 }}</p>
  </a>
</div>
```

### Template for search form in navbar:

```django
<form method="get" action="{% url 'search' %}">
  <input type="search" name="q" value="{{ request.GET.q }}">
  <button type="submit">Search</button>
</form>
```

### Cart count: Example context processor

```python
def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        count = request.user.cart.items.count()
    return {'cart_count': count}
```

Then show `{{ cart_count }}` in navbar.

---

## 18. Serving Templates in Production — Static & Media

* Use `collectstatic` to gather static files to `STATIC_ROOT`.
* Use whitenoise for simple setups (Django + Gunicorn) or serve static via CDN/Nginx.
* Media files: upload to S3 or a dedicated media server or configured Nginx location.
* Ensure `DEBUG = False` and `ALLOWED_HOSTS` set.

Deployment snippet (Nginx + Gunicorn):

* Nginx serves static/media.
* Gunicorn runs Django app; templates are rendered by Django.

---

## 19. SEO & Accessibility

* Use semantic HTML and meta tags (`title`, `description`, `og:` tags) in `head` blocks.
* Breadcrumbs, `<nav>`, alt attributes on images: `alt="{{ product.name }}"`.
* Use server-side rendering for content so crawlers see full HTML.

---

## 20. Common Mistakes & How to Teach Avoiding Them

* Doing heavy DB work in templates (not allowed, but heavy loops can still cause N+1 queries) — teach use of `select_related`.
* Overusing `{% include %}` for tiny fragments that replicate logic — prefer components.
* Marking user input `|safe` without sanitizing.
* Not handling missing images (`{{ obj.image.url }}` can raise if no image — use `if obj.image`).
* Not using `csrf_token` in forms.

---

## 21. Debugging Template Issues

* Use `{{ variable|default:"(missing)" }}` to find why data not present.
* In dev, `DEBUG = True` will show template tracebacks.
* Use `django.template.loader.render_to_string` in shell to test template rendering.

---

## 22. Template-Related Performance Checklist

* Use `select_related`/`prefetch_related` where needed.
* Cache fragments of templates used frequently and expensive to build.
* Avoid database queries inside template tags or context processors where possible.
* Compress and version static assets using pipeline/webpack or ManifestStaticFilesStorage.

---

## 23. Testing & CI

* Write tests for views that render templates (assert presence of key elements).
* Test custom template tags/filters separately.
* Include `collectstatic` in CI to ensure no broken static references.

---

## 24. Deployment & Production Tips (Checklist)

* Set `DEBUG = False`
* Set `ALLOWED_HOSTS`
* Run `python manage.py collectstatic`
* Use whitenoise or serve static via Nginx / CDN
* Configure media file storage (S3 recommended)
* Configure secure headers (HSTS, X-Frame-Options)
* Use template caching if heavy
* Monitor errors (Sentry) — include template tracebacks in dev but not prod

---

## 25. Lesson Plan / Teaching Sequence (Suggested)

1. Intro to templates & syntax (variables, filters, tags) — demo simple page.
2. Template inheritance & includes — build `base.html`, `navbar`, `footer`.
3. Forms & templates — contact form and validation.
4. Static & media — wire up CSS and images.
5. Loops, conditions, and pagination.
6. Custom tags & filters — build one filter and one inclusion tag.
7. Context processors & navbar/cart count.
8. Performance — select_related, fragment caching.
9. Security & escaping — safe/sanitizing user content.
10. Full project workshop — build a small e-commerce app with templates.
11. Deployment and static/media in production.

---

## 26. Assignments & Exercises

### Quick exercises

* Render a list of students using a loop and show “Passed” if marks ≥ 50.
* Create `base.html` and two child templates that extend it.

### Medium

* Build a blog index template with pagination and a sidebar that uses an inclusion tag to display recent posts.
* Create a contact form and render validation errors next to each field.

### Project (capstone)

* **MyShop basic**: product list, product detail, cart, checkout (no payment gateway). Must use template inheritance, forms, context processor for cart count, and include partial templates for product cards. Add unit tests for two views and one custom template tag. Prepare `README` with steps to serve static files.

---

## 27. Cheatsheet — Useful Template Shortcuts

* `{{ var|default:"-" }}` — fallback
* `{% url 'name' arg %}` — reverse URL
* `{% static 'path' %}` — static file
* `{% include '...html' %}` — include partial
* `{% load static %}` — load tag libraries
* `{% block name %}{% endblock %}` — inheritance
* `{% csrf_token %}` — security for forms

---

## 28. Extra Resources to Recommend to Students

* Django docs: Templates, Forms, Static files
* Django Debug Toolbar (inspect DB queries)
* `django-crispy-forms` for nicer form rendering
* `whitenoise` for static serving in simple deployments
* `bleach` for sanitizing HTML if you must allow user HTML

---

## 29. Example: Minimal Files for Product Detail (complete)

`views.py`

```python
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    return render(request, 'product/detail.html', {'product': product, 'related': related})
```

`templates/product/detail.html`

```django
{% extends "base.html" %}
{% block title %}{{ product.name }} - MyShop{% endblock %}
{% block content %}
  <div class="product-detail">
    <img src="{{ product.image.url }}" alt="{{ product.name }}">
    <h1>{{ product.name }}</h1>
    <p>{{ product.description }}</p>
    <p>Price: {{ product.price|floatformat:2 }}</p>

    <h3>Related products</h3>
    <div class="related">
      {% for r in related %}
        {% include 'partials/product_card.html' with product=r %}
      {% empty %}
        <p>No related products.</p>
      {% endfor %}
    </div>
  </div>
{% endblock %}
```

---

## 30. Final Teaching Notes / Best Practices Summary

* Keep templates clean: logic in views/models; presentation in templates.
* Reuse templates via inheritance and includes.
* Test template outputs.
* Keep performance in mind: avoid N+1 queries and heavy context processors.
* Always escape user content by default; sanitize carefully when allowing HTML.
* Use fragment caching for expensive-to-render parts.
* Organize templates by app to avoid name collisions: `templates/<app_name>/...`.

