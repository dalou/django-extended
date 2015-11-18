# encoding: utf-8

from django import forms
from django.forms.models import modelformset_factory, inlineformset_factory
from fields_bundle.forms import HtmlField, HtmlInput, TextField, TextInput
from ..models import *

class PostForm(forms.ModelForm):

    TINYMCE_MINIMAL = {
        'toolbar': 'undo redo'
    }
    TINYMCE_MIDDLE = {
        'toolbar': "undo redo | removeformat | link image base64img",
    }

    # title  = TextField(label=u"Titre de l'article", tinymce=TINYMCE_MINIMAL, inline=True)
    content  = HtmlField(label=u"Contenu de l'article", tinymce=TINYMCE_MIDDLE, inline=True, required=False)

    class Meta:
        model = Post
        fields = ('title', 'content')


    def __init__(self, *args, **kwargs):

        super(PostForm, self).__init__(*args, **kwargs)

PostFormSet = modelformset_factory(Post, PostForm, extra=0, can_delete=True)