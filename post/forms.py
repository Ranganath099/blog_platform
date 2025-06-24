from django import forms
from .models import Post, Comment, Category

class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",
        widget=forms.Select(attrs={"class": "form-control", 'style': 'width: 150px; font-size: 14px;'})
        )
    class Meta:
        model = Post
        fields = ["category", 'title', 'content']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "parent"]
        widgets = {"parent": forms.HiddenInput()}
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

