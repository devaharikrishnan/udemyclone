from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, RedirectView, ListView, DetailView, UpdateView

from courses.models import Category, Lesson, Course
from udemy.models import Enroll
from .models import User,ratings
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm,Coursecreateform,Lessoncreateform,Lessonupdateform
from django.utils import timezone
now = timezone.now()

class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/form.html'
    success_url = '/login'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):

        user_form = self.form_class(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/form.html', {'form': user_form})


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'accounts/form.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())

        return HttpResponseRedirect(self.get_success_url())
        # return super(Login, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


class EnrolledCoursesListView(ListView):
    model = Enroll
    template_name = 'courses/enrolled_courses.html'
    context_object_name = 'enrolls'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('course').all().filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        print("=========================================================")
        print(context)
        return context

def enrolled(request):
    a = Enroll.objects.filter(user=request.user).values("course_id")
    b = Course.objects.filter(pk__in=a).values()
    print(b)
    category = Category.objects.all()
    return render(request,"courses/enrolled_courses.html",{'enrolls':a,'categories':category})
class StartLessonView(DetailView):
    model = Lesson
    template_name = 'lessons/lessons_by_course.html'
    context_object_name = 'lesson'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        queryset = queryset.filter(course=course)
        print("\n\n")
        print(queryset)

        print(course)
        print("\n\n")
        try:
            # Get the single item from the filtered queryset
            obj = queryset[:1].get()
            print("\n\n")
            print(obj)
            # url = obj.video_url
            #url = url.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/")
            # obj.video_url = url
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        context["lessons"] = self.model.objects.filter(course=course)
        context["course"] = course
        return context


class LessonView(DetailView):
    model = Lesson
    template_name = 'lessons/lessons_by_course.html'
    context_object_name = 'lesson'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        lesson_id = self.kwargs['id']
        queryset = queryset.filter(id=lesson_id)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
            # url = obj.video_url
            # url = url.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/")
            # obj.video_url = url
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        context["lessons"] = self.model.objects.filter(course=course)
        context["course"] = course
        return context


class ProfileUpdateView(UpdateView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "user"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("accounts:my-profile")

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_initial(self):
        return {"first_name": self.request.user.first_name, "last_name": self.request.user.last_name}

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def Createcourse(request):
    if request.method == 'POST':
        form = Coursecreateform(request.POST or None,request.FILES or None)
        print("\n\n")
        print(form)
        if form.is_valid():
            print(form.cleaned_data)
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect('/users/viewmycourses')
        else:
            return HttpResponse("Failed credentials ")
    else:
        form = Coursecreateform(initial={'user': request.user})
    return render(request,"courses/createcourse.html",{'form':form})

def Editcourse(request,title):
    instance = get_object_or_404(Course, pk=title)
    if request.method=='POST':
        # print("\n\n")
        # print(request)
        form = Coursecreateform(request.POST or None, instance=instance)
        print("\n\n")
        print(form)
        if form.is_valid():
            
            form.save()
            return redirect('/users/viewmycourses')
    else:
        form = Coursecreateform(request.POST or None, instance=instance)
    print("\n")
    return render(request,"courses/editcourse.html",{'form':form,'pk':title})
    #return render(request, 'my_template.html', {'form': form}) 
def Deletecourses(request,title):
    pass

def viewmycourses(request):
    courses = Course.objects.filter(user=request.user)
    print("\n\n")
    print(courses)
    # for x,y in courses.items():
    #     print(x,y)
    return render(request,"courses/viewcourse.html",{'courses':courses})
    
    
def Createlesson(request,title):    
    print("=========================================================================")
    tit = Course.objects.filter(pk=title).values("title")
    print("=========================================================================")
    if request.method == 'POST':
        print(request.POST)
        # if not request.POST._mutable:
        #     request.POST._mutable = True
        # request.POST['course'] = title
        # request.POST['course'] = title
        form = Lessoncreateform(request.POST or None,request.FILES or None)
        print("\n\n")
        print("create lesson view")
        print(title)
        print(form)
        if form.is_valid():
            print("====================================================================================")
            print(" cleaned_data ")
            print(form.cleaned_data)
            form.save()
            print("====================================================================================")
            # obj = form.save(commit = False)
            # obj.course = title
            # obj.save()
            return redirect('/courses/'+title)
        else:
            return HttpResponse("Failed credentials ")
    else:
        print("====================================================================================")
        print("else")
        print(tit[0]['title'])
        print("====================================================================================")
        form = Lessoncreateform(initial={"course":title,"created_at":now,"updated_at":now})
        #initial={"course":tit[0]['title']}
    return render(request,"courses/createlesson.html",{'form':form,'title':title})

def Editlesson(request,title,pk):
    instance = get_object_or_404(Lesson, pk=pk)
    if request.method=='POST':
        form = Lessonupdateform(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('/courses/'+title)
    else:
        form = Lessonupdateform(request.POST or None, instance=instance)
    print("\n")
    return render(request,"courses/editlesson.html",{'form':form,'pk':pk})
    pass
def Deletelesson(request,title,id):
    pass
def viewmylessons(request,id):
    queryset = Lesson.objects.filter(course=id)
    print("\n\n")
    print(queryset)
    return HttpResponse(queryset)

def review(request,title):
    if request.method == 'POST':
        a = ratings(review = request.POST['review'],rating  = request.POST['rating'],reviewedby=request.user,courseid=title)
        a.save()
        print(a)
    return redirect('/courses/'+title)

def feedback(request,title):
    a = ratings.objects.filter(courseid=title).values()
    print("==========================================")
    print(a)
    print("==========================================")
    return render(request,"courses/feedback.html",{"feed":a})
    # return redirect('/feedback/'+title)
    #return HttpResponse(title)
# class Coursecreateview(CreateView):
#     model = Course
#     form_class = Coursecreateform
#     template_name = 'accounts/form.html'
#     success_url = 'users/mentor'

#     def get_success_url(self):
#         return self.success_url

#     def post(self, request, *args, **kwargs):

#         user_form = self.form_class(data=request.POST)

#         if user_form.is_valid():
#             user = user_form.save(commit=False)
#             password = user_form.cleaned_data.get("password1")
#             user.set_password(password)
#             user.save()
#             return redirect('accounts:login')
#         else:
#             return render(request, 'accounts/form.html', {'form': user_form})