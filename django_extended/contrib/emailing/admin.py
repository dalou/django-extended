# encoding: utf-8

from django.conf import settings
from django.contrib import admin
from django.db import models
from django import forms
from django.shortcuts import render_to_response


from .models import *

class UserActivationTokenAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'is_used', 'expiration_date')
admin.site.register(UserActivationToken, UserActivationTokenAdmin)

class TestEmailAdmin(admin.ModelAdmin):
    list_display = ('email', )
admin.site.register(TestEmail, TestEmailAdmin)

class EmailAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'receivers', 'date_created', 'is_sent')
admin.site.register(Email, EmailAdmin)


class EmailTransactionAdmin(admin.ModelAdmin):
    list_display = ('email', 'receiver', 'date_created', 'is_sent')
admin.site.register(EmailTransaction, EmailTransactionAdmin)



class SendEmailForm(forms.ModelForm):
    template = forms.CharField(widget=forms.Textarea, required=True)
    emails = forms.CharField(widget=forms.Textarea, required=False)
    # test_emails = forms.CharField(label=u"Emails de test", widget=forms.Textarea, required=False)

    class Meta:
        model = Email
        fields = ('name', 'subject', 'template',  'emails',  )

    def __init__(self, *args, **kwargs):
        super(SendEmailForm, self).__init__( *args, **kwargs)

class SendMailMixin(object):

    emailing_form_template_name = 'emailing/admin/send_form.html'

    def __init__(self, *args, **kwargs):
        super(SendMailMixin, self).__init__(*args, **kwargs)
        self.actions += ('send_mail', )

    def emailing_get_emails(self):
        return []

    def send_mail(modeladmin, request, queryset):

        emails = list(set(modeladmin.emailing_get_emails(request, queryset)))


        form = SendEmailForm(initial={
            'emails': ", ".join(emails),
            # 'test_emails': ", ".join()
        })

        return render_to_response(modeladmin.emailing_form_template_name, {
                'receivers': emails,
                'form': form
            },
            context_instance=RequestContext(request),
        )

    send_mail.short_description = u"Envoyer un email à la selection"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        emailing_send = request.POST.get('_emailing_form_send_real') or request.POST.get('_emailing_form_send_test')
        emailing_test = request.POST.get('_emailing_form_send_test')

        if emailing_send:
            form = SendEmailForm(request.POST, initial={
                'test_emails': ", ".join(list(set(TestEmail.objects.all().values_list('email', flat=True))))
            })
            if form.is_valid():
                email = form.save()
                if emailing_test:
                    receivers = email.send_test()
                    messages.success(request,
                        u"%s emails de test vont être envoyés. %s" % (len(receivers), receivers)
                    )
                else:
                    receivers = email.send()
                    messages.success(request,
                        u"%s emails vont être envoyés. %s" % (len(receivers), receivers)
                    )
            return render_to_response(self.emailing_form_template_name, {
                    'form': form
                },
                context_instance=RequestContext(request),
            )

        return super(SendMailMixin, self).changelist_view(request, extra_context=extra_context)