from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from courses.models import Course, Category
from .models import Enroll
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404,HttpResponse

def index(request):
    print(request.user.is_anonymous)
    if request.user.is_anonymous:
        return HttpResponseRedirect('/login')
    else:
        return HttpResponseRedirect('/home')
    #return HttpResponse(request.user.is_anonymous)


class HomeListView(ListView):
    model = Course
    template_name = 'index.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("\n\n")
        a = Enroll.objects.filter(user=self.request.user).values("user")
        print(a)
        if a:
            context['top_courses'] = self.model.objects.all().order_by('?').filter(~Q(user = a[0]["user"]))
        else:
            context['top_courses'] = self.model.objects.all().order_by('?')
        return context


class SearchView(ListView):
    model = Course
    template_name = 'search.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(title__contains=self.request.GET['q'])
