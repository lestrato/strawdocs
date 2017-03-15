from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, JsonResponse
from uuid import uuid4
from hashlib import sha1
from django.core.mail import send_mail
from smtplib import SMTPException
from django.template import loader
from django.utils import timezone

from basesite.views import *
from account.forms import *
from account.models import *

def login_forbidden(function=None, redirect_field_name=None, redirect_to='/account/'):
    """
    Decorator for views that checks that the user is NOT logged in, redirecting
    to the homepage if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated(),
        login_url=redirect_to,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)

    return actual_decorator

@method_decorator(login_required, name='dispatch')
class Settings(BaseView):
    def get_fetch(self, request, template_items):
        PCForm = PasswordChangeForm()
        ECForm = EmailChangeForm()
        template_items['PCForm'] = PCForm
        template_items['ECForm'] = ECForm
        return render(request, 'settings.html', template_items)

    def post_fetch(self, request):
        data = {}
        if 'passwordResetSubmit' in request.POST:
            PCForm = PasswordChangeForm(request.POST)
            if PCForm.is_valid():
                # check if the existing password for the account is correct
                if request.user.check_password(PCForm.cleaned_data['current_password']):
                    # check if the two new passwords are the same
                    if PCForm.cleaned_data['password1'] != PCForm.cleaned_data['password2']:
                        data['error_message'] = 'Your two new passwords do not match.'
                    else:
                        request.user.set_password(PCForm.cleaned_data['password1'])
                        request.user.save()
                        data['success_message'] = 'Password changed.'

                else:
                    data['error_message'] = 'The existing password you inputted is wrong.'

                return JsonResponse(data)

        if 'emailResetSubmit' in request.POST:
            ECForm = EmailChangeForm(request.POST)
            if ECForm.is_valid():
                request.user.email = ECForm.cleaned_data['email']
                request.user.save()
                return JsonResponse({'success_message' : 'Email changed to ' + ECForm.cleaned_data['email']})

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@method_decorator(login_forbidden, name='dispatch')
class Recovery(BaseView):
    def get_fetch(self, request, template_items):
        token = request.GET.get('token', False)
        if token:
            # check to see if the token is still valid
            try:
                recovery_string = AccountRecoveryString.objects.get(
                    recovery_string = sha1(token).hexdigest(),
                )
                # check to see if 1 day has passed since it was created
                time_difference = timezone.now() - recovery_string.created_on
                if time_difference.days >= 1:
                    template_items['token'] = 'expired'
                else:
                    template_items['token'] = 'valid'
                    template_items['token_value'] = token

                    PRForm = PasswordResetForm()
                    template_items['PRForm'] = PRForm
            except AccountRecoveryString.DoesNotExist:
                template_items['token'] = 'doesnotexist'

        ERForm = EmailRecoveryForm()
        template_items['ERForm'] = ERForm

        return render(request, 'recovery.html', template_items)

    def post_fetch(self, request):
        print request.POST
        if 'emailRecoverySubmit' in request.POST:
            ERForm = EmailRecoveryForm(request.POST)
            data = {}
            if ERForm.is_valid():
                try:
                    user = User.objects.get(
                        email=ERForm.cleaned_data['email']
                    )
                    # delete all previous instances of an email password reset request, if it exists
                    all_account_recovery = AccountRecoveryString.objects.filter(
                        created_for = user,
                    )
                    all_account_recovery.delete()

                    # make a random UUID and hash it with sha1
                    uuid_string = str(uuid4())
                    hashed_uuid = sha1(uuid_string).hexdigest()
                    new_account_recovery_string = AccountRecoveryString(
                        recovery_string=hashed_uuid,
                        created_for=user,
                    )
                    new_account_recovery_string.save()

                    html_message = loader.render_to_string('recovery_email.html', {
                        'username': user.username,
                        'recovery_link':  uuid_string,
                    })

                    try:
                        # send the unhashed uuid_string to the user's email
                        send_mail(
                            '[strawdocs] Reset Your Password',
                            'Here is the message.',
                            'do-not-reply@strawdocs.com',
                            [ERForm.cleaned_data['email']],
                            fail_silently=False,
                            html_message=html_message,
                        )
                        data['success_message'] = 'Email sent - if it doesn\'t show up at first, check your junk mailbox. If you\'d like, you can send another email.'
                        return JsonResponse(data)


                    except SMTPException:
                        # catch the failure to send the email
                        data['error_message'] = 'We had trouble sending you an email just now; please try again later.'
                        return JsonResponse(data)

                except User.DoesNotExist:
                    data['error_message'] = 'That email address isn\'t registered with us.'
                    return JsonResponse(data)
            else:
                data['error_message'] = 'That\'s not a valid email address.'
                return JsonResponse(data)

        if 'passwordResetSubmit' in request.POST:
            PRForm = PasswordResetForm(request.POST)
            data = {}
            if PRForm.is_valid():
                try: # get the user
                    user = User.objects.get(
                        username = PRForm.cleaned_data['username'],
                    )
                    try: # get the recovery string instance and delete it
                        recovery_string = AccountRecoveryString.objects.get(
                            created_for = user,
                            recovery_string = sha1(request.POST['passwordResetSubmit']).hexdigest(),
                        )

                        if PRForm.cleaned_data['password1'] != PRForm.cleaned_data['password2']:
                            data['error_message'] = 'Your two passwords do not match.'

                        else:
                            user.set_password(PRForm.cleaned_data['password1'])
                            user.save()
                            recovery_string.delete()
                            data['success_message'] = 'Password changed!'

                    except AccountRecoveryString.DoesNotExist:
                        data['error_message'] = 'This recovery link no longer exists.'

                except User.DoesNotExist:
                    data['error_message'] = 'The wrong username for this recovery link was inputted.'

                return JsonResponse(data)

        return HttpResponseRedirect('/')

def recover_email(request):
    return render(request, 'recovery_email.html', {'username': 'test_username', 'recovery_link': 'test_token'})
