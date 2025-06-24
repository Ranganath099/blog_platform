from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, AuthorProfile
# class CustomUserCreationForm(UserCreationForm):
#     identifier = forms.CharField(label="Email or Phone", max_length=100)
#     role = forms.ChoiceField(choices=[('user', 'User'), ('author', 'Author')], label="Register as")  # Updated roles
#     bio = forms.CharField(widget=forms.Textarea, required=False, label="Bio")
#     profile_picture = forms.ImageField(required=False, label="Profile Picture")

#     class Meta:
#         model = CustomUser
#         fields = ('identifier', 'password1', 'password2', 'role')

#     def clean_identifier(self):
#         identifier = self.cleaned_data.get("identifier")
#         if "@" in identifier:  # If it contains '@', assume it's an email
#             if CustomUser.objects.filter(email=identifier).exists():
#                 raise forms.ValidationError("A user with this email already exists.")
#         else:  # Otherwise, assume it's a phone number
#             if CustomUser.objects.filter(phone_number=identifier).exists():
#                 raise forms.ValidationError("A user with this phone number already exists.")
#         return identifier

#     def save(self, commit=True):
#         identifier = self.cleaned_data["identifier"]
#         password = self.cleaned_data["password1"]
#         role = self.cleaned_data["role"]

#         # Create user
#         user = CustomUser.objects.create_user(username=identifier, password=password)
#         user.role = role

#         # If the role is 'author', create an AuthorProfile
#         if role == 'author':
#             AuthorProfile.objects.create(
#                 user=user,
#                 bio=self.cleaned_data.get("bio"),
#                 profile_picture=self.cleaned_data.get("profile_picture")
#             )
        
#         if commit:
#             user.save()
#         return user

# class EmailOrPhoneLoginForm(forms.Form):
#     identifier = forms.CharField(label="Email or Phone")
#     password = forms.CharField(widget=forms.PasswordInput)

# class AuthorProfileForm(forms.ModelForm):
#     class Meta:
#         model = AuthorProfile
#         fields = ['profile_picture', 'bio']




class CustomUserCreationForm(UserCreationForm):
    identifier = forms.CharField(label="Email or Phone", max_length=100)
    role = forms.ChoiceField(choices=[('user', 'User'), ('author', 'Author')], label="Register as")  
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Bio")
    profile_picture = forms.ImageField(required=False, label="Profile Picture")

    class Meta:
        model = CustomUser
        fields = ('identifier', 'password1', 'password2', 'role')

    def clean_identifier(self):
        identifier = self.cleaned_data.get("identifier")
        if "@" in identifier:  
            if CustomUser.objects.filter(email=identifier).exists():
                raise forms.ValidationError("A user with this email already exists.")
        else:  
            if CustomUser.objects.filter(phone_number=identifier).exists():
                raise forms.ValidationError("A user with this phone number already exists.")
        return identifier

    def save(self, commit=True):
        identifier = self.cleaned_data["identifier"]
        password = self.cleaned_data["password1"]
        role = self.cleaned_data["role"]

        if "@" in identifier:
            user = CustomUser.objects.create_user(username=identifier, password=password, role=role)
        else:
            user = CustomUser.objects.create_user(username=identifier, password=password, role=role)
            user.phone_number = identifier  # Ensure phone number is stored

        if role == 'author':
            user.is_staff = True  # Ensure authors can access admin
            user.save()  # Save user role properly
            AuthorProfile.objects.create(
                user=user,
                bio=self.cleaned_data.get("bio"),
                profile_picture=self.cleaned_data.get("profile_picture")
            )

        if commit:
            user.save()
        return user


class EmailOrPhoneLoginForm(forms.Form):
    identifier = forms.CharField(label="Email or Phone")
    password = forms.CharField(widget=forms.PasswordInput)

class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = AuthorProfile
        fields = ['profile_picture', 'bio', 'username', 'age', 'place','email']





































# class CustomUserCreationForm(UserCreationForm):
#     identifier = forms.CharField(label="Email or Phone", max_length=100)
#     role = forms.ChoiceField(choices=[('user', 'User'), ('author', 'Author')], label="Register as")  
#     bio = forms.CharField(widget=forms.Textarea, required=False, label="Bio")
#     profile_picture = forms.ImageField(required=False, label="Profile Picture")

#     class Meta:
#         model = CustomUser
#         fields = ('identifier', 'password1', 'password2', 'role')

#     def clean_identifier(self):
#         identifier = self.cleaned_data.get("identifier")
#         if "@" in identifier:  
#             if CustomUser.objects.filter(email=identifier).exists():
#                 raise forms.ValidationError("A user with this email already exists.")
#         else:  
#             if CustomUser.objects.filter(phone_number=identifier).exists():
#                 raise forms.ValidationError("A user with this phone number already exists.")
#         return identifier

#     def save(self, commit=True):
#         identifier = self.cleaned_data["identifier"]
#         password = self.cleaned_data["password1"]
#         role = self.cleaned_data["role"]

#         # Create user
#         user = CustomUser.objects.create_user(username=identifier, password=password, role=role)

#         if role == 'author':
#             AuthorProfile.objects.create(
#                 user=user,
#                 bio=self.cleaned_data.get("bio"),
#                 profile_picture=self.cleaned_data.get("profile_picture")
#             )

#         if commit:
#             user.save()
#         return user
