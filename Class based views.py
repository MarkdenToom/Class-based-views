>django-admin startproject advcbv
>cd advcbv
>django-admin startapp basic_app
Add TEMPLATE_DIR to TEMPLATES and add INSTALLED_APPS to settings.py
Create templates/base.html:
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Base</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
  </head>
  <body>
    <nav class="navbar navbar-default navbar-static-top">
      <ul class="nav navbar-nav">
        <li><a class="navbar-brand" href="{%url 'basic_app:list'%}">Schools</a></li>
        <li><a class="navbar-link" href="{%url 'admin:index'%}">Admin</a></li>
        <li><a class="navbar-link" href="">temp</a></li>
      </ul>
    </nav>
    <div class="container">
      {%block body_block%}
      {%endblock%}
    </div>
  </body>
</html>

and index.html:
{%extends "base.html"%}
{%block body_block%}
<div class="jumbotron">
  <h1>Home page!</h1>
</div>
{%endblock%}

views.py:
from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from . import models
from django.urls import reverse_lazy
class SchoolListView(ListView):
    context_object_name = 'schools'
    model = models.School
class SchoolDetailView(DetailView):
    context_object_name = 'school_detail'
    model = models.School
    template_name = 'basic_app/school_detail.html'
class IndexView(TemplateView):
    template_name = 'index.html'
class SchoolCreateView(CreateView):
    fields = ('name', 'principal', 'location')
    model = models.School
class SchoolUpdateView(UpdateView):
    fields = ('name', 'principal')  # location of school will probably not change
    model = models.School
class SchoolDeleteView(DeleteView):
    model = models.School
    success_url = reverse_lazy("basic_app:list")

project/urls.py:
from django.contrib import admin
from django.urls import path
from basic_app import views
from django.conf.urls import include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view()),
    path('basic_app/', include('basic_app.urls', namespace='basic_app'))
]

create app/urls.py:
from django.conf.urls import url
from basic_app import views
app_name = 'basic_app'
urlpatterns = [
    url(r'^$', views.SchoolListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.SchoolDetailView.as_view(), name='detail'),
    url(r'^create/$', views.SchoolCreateView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', views.SchoolUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.SchoolDeleteView.as_view(), name='delete'),
]

models.py:
from django.db import models
from django.urls import reverse
class School(models.Model):
    name = models.CharField(max_length=256)
    principal = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("basic_app:detail", kwargs={'pk': self.pk})
class Student(models.Model):
    name = models.CharField(max_length=256)
    age = models.PositiveIntegerField()
    school = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

admin.py:
from django.contrib import admin
from basic_app.models import School, Student
admin.site.register(School)
admin.site.register(Student)

create \basic_app\templates\basic_app\basic_app_base.html:
<copy/paste templates/base.html>

and school_list.html:
{%extends "basic_app/basic_app_base.html"%}
{%block body_block%}
<h1>Welcome to a list of all the school!</h1>
<ol>
  {%for school in schools%}
  <h2><li><a href="{{school.id}}">{{school.name}}</a></li></h2>
  {%endfor%}
</ol>
{%endblock%}

and school_detail.html:
{%extends "basic_app/basic_app_base.html"%}
{%block body_block%}
<div class="jumbotron">
  <h1>Welcome to the school detail page!</h1>
  <h2>School details:</h2>
  <p>Name: {{school_detail.name}}</p>
  <p>Principal: {{school_detail.principal}}</p>
  <p>Location: {{school_detail.location}}</p>
  <h3>Students:</h3>
  {%for student in school_detail.students.all%}
    <p>{{student.name}} who is {{student.age}} years old.</p>
  {%endfor%}
</div>
{%endblock%}

and school_list.html:
{%extends "basic_app/basic_app_base.html"%}
{%block body_block%}
<h1>
  {%if not form.instance.pk%}
  Create School
  {%else%}
  Update School
  {%endif%}
</h1>
<form method="post">
  {%csrf_token%}
  {{form.as_p}}
  <input type="submit" class="btn btn-primary" value="Submit">
</form>
{%endblock%}

and school_confirm_delete.html:
{%extends "basic_app/basic_app_base.html"%}
{%block body_block%}
<h1>Delete: {{school.name}}?</h1>
<form method="post">
  {%csrf_token%}
  <input type="submit" class='btn btn-danger' value="Delete">
  <a href="{%url 'basic_app:detail' pk=school.pk%}">Cancel</a>
</form>
{%endblock%}

>python manage.py migrate
>python manage.py makemigrations basic_app
>python manage.py migrate
>python manage.py createsuperuser
>python manage.py runserver
