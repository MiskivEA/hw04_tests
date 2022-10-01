from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'text',
            'group',
            'image'
        ]
        widgets = {
            'text': forms.Textarea(attrs={'cols': 10,
                                          'rows': 10,
                                          }
                                   ),

        }
