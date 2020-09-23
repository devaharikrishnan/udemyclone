from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from courses.models import Category, Lesson, Course
from .models import User


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    # username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].icon = '<span class="input-field-icon"><i class="fas fa-envelope"></i></span>'
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter Last Name'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Again password'})
        # self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label or 'email@address.nl'

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2")

        # widgets = {
        #     'password1': forms.TextInput(attrs={'placeholder': 'Password'}),
        #     'password2': forms.TextInput(attrs={'placeholder': 'Repeat your password'}),
        # }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError('Enter valid email')
        return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({'placeholder': 'Enter first name'})
        self.fields["last_name"].widget.attrs.update({'placeholder': 'Enter last name'})

    class Meta:
        model = User
        fields = ["first_name", "last_name"]

class Coursecreateform(forms.ModelForm):
    user = forms.ChoiceField(required=False,widget=forms.HiddenInput())
    # is_published = forms.BooleanField(forms.HiddenInput())
    class Meta:
        model = Course
        fields = ["user","title","category","slug","short_description","description","outcome","requirements","language","price","level","thumbnail"]

class Courseupdateform(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'#["first_name", "last_name"]
class Lessoncreateform(forms.ModelForm):
    # course = forms.ChoiceField(required=False,widget=forms.HiddenInput())
    # course = forms.ChoiceField(required=False,widget=forms.TextInput())
    created_at = forms.DateTimeField(required=False,widget=forms.HiddenInput())
    updated_at = forms.DateTimeField(required=False,widget=forms.HiddenInput())
    class Meta:
        model = Lesson
        fields = '__all__'#["course","title","duration","video_url"] #'__all__'#["first_name", "last_name"]

class Lessonupdateform(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title","duration","video_url"] #'__all__'#["first_name", "last_name"]

#    title = models.CharField(max_length=200)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#     slug = models.SlugField(max_length=200, unique=True, primary_key=True, auto_created=False)
#     short_description = models.TextField(blank=False, max_length=60)
#     description = models.TextField(blank=False)
#     outcome = models.CharField(max_length=200)
#     requirements = models.CharField(max_length=200)
#     language = models.CharField(max_length=200)
#     price = models.FloatField(validators=[MinValueValidator(9.99)])
#     level = models.CharField(max_length=20)
#     thumbnail = models.ImageField(upload_to='thumbnails/')
#     video_url = models.CharField(max_length=100)
#     is_published = models.BooleanField(default=True)
#     created_at = models.DateTimeField(default=now)
#     updated_at = models.DateTimeField(default=now)
