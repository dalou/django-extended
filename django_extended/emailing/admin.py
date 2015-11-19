# encoding: utf-8

from django.conf import settings
from django.contrib import admin
from django.db import models
from django import forms
from django.shortcuts import render_to_response, redirect


from .models import *

class EmailingUserActivationTokenAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'is_used', 'expiration_date')
admin.site.register(EmailingUserActivationToken, EmailingUserActivationTokenAdmin)

class EmailingTestEmailAdmin(admin.ModelAdmin):
    list_display = ('email', )
admin.site.register(EmailingTestEmail, EmailingTestEmailAdmin)


class EmailingTransactionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'emailing', 'receiver', 'date_created', 'send_count')

    def get_readonly_fields(self, *args, **kwargs):
        return [f.name for f in self.model._meta.fields]
admin.site.register(EmailingTransaction, EmailingTransactionAdmin)



class EmailingForm(forms.ModelForm):
    # template = forms.CharField(widget=forms.Textarea, required=True)
    # test_emails = forms.CharField(label=u"Emails de test", widget=forms.Textarea, required=False)

    class Meta:
        model = Emailing
        fields = ('send_count', 'test_count', 'name', 'subject', 'sender', 'template', 'receivers', 'receivers_test',)


    def __init__(self, *args, **kwargs):
        super(EmailingForm, self).__init__( *args, **kwargs)
        self.fields['send_count'].widget.attrs['readonly'] = True
        self.fields['test_count'].widget.attrs['readonly'] = True




class EmailingAdmin(admin.ModelAdmin):
    change_form_template = 'django_extended/emailing/admin/send_form.html'
    list_display = ('name', 'subject', 'sender', 'get_receivers', 'date_created', 'send_count', 'test_count')

    form = EmailingForm


    def get_receivers(self, obj):
        receivers = obj.receivers.split(',')
        return u"""%s destinataires réels : %s [..]""" % ( len(receivers), ", ".join(receivers[0:10]))

    def get_changeform_initial_data(self, request):

        receivers = []
        if request.session.get('django_extended-emailing_receivers'):
            receivers = request.session.get('django_extended-emailing_receivers')
            del request.session['django_extended-emailing_receivers']
        return {
            'sender': getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@exemple.fr'),
            'template': 'Template du mail (compatible mailchimp)',
            'receivers': receivers,
            'receivers_test': ", ".join(list(set(EmailingTestEmail.objects.all().values_list('email', flat=True))))
        }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.get_changeform_initial_data(request))
        return super(EmailingAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)

    def response_change(self, request, obj):

        send = '_sendreal' in request.POST or '_sendtest' in request.POST
        test = '_sendtest' in request.POST

        if send:
            receivers = obj.send(force=test, test=test)
            messages.success(request,
                u"%s emails de test vont être envoyés. %s [..]" % (len(receivers), receivers[0:10])
            )

            request.POST['_continue'] = "1"

        return super(EmailingAdmin, self).response_change( request, obj)



admin.site.register(Emailing, EmailingAdmin)

class SendMailMixin(object):

    emailing_form_template_name = 'django_extended/emailing/admin/send_form.html'

    def __init__(self, *args, **kwargs):
        super(SendMailMixin, self).__init__(*args, **kwargs)
        self.actions += ('send_mail', )

    def send_mail_receivers(self):
        return []

    def send_mail(modeladmin, request, queryset):
        receivers = list(set(modeladmin.send_mail_receivers(request, queryset)))
        request.session['django_extended-emailing_receivers'] = ", ".join(receivers)
        return redirect(reverse('admin:django_extended_emailing_add'))
    send_mail.short_description = u"Envoyer un email à la selection"