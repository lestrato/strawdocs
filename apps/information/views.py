from django.shortcuts import render
from basesite.views import *
from information.forms import *
from information.models import *
from django.core.mail import send_mail

import re

class Team(BaseView):
    def get_fetch(self, request, template_items):
        return render(request, 'team.html', template_items)
    def post_fetch(self, request):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class Support(BaseView):
    def get_fetch(self, request, template_items):
    	TCForm = TicketCreationForm()
    	template_items['TCForm'] = TCForm

        return render(request, 'support.html', template_items)
    def post_fetch(self, request):
    	print request.POST
        if 'ticketCreationSubmit' in request.POST:
            TCForm = TicketCreationForm(request.POST)
            if TCForm.is_valid():
            	if not re.match(r".+@.+\..+", TCForm.cleaned_data['email']):
                	return JsonResponse({'error_message': 'Please enter a valid email address.'})
                # create new ticket object
                new_ticket = SupportTicket(
                    help_topic = TCForm.cleaned_data['topic'],
                    email = TCForm.cleaned_data['email'],
                    creator_name = TCForm.cleaned_data['name'],
                    summary = TCForm.cleaned_data['summary'],
                    details = TCForm.cleaned_data['details']
                )
                new_ticket.save()               
                # send email (don't care if it fails)
                send_mail(
                    '[strawdocs] New Support Ticket',
                    'Check out a new support ticket.',
                    'do-not-reply@strawdocs.com',
                    [TCForm.cleaned_data['email']],
                    fail_silently=True,
                )

            	return JsonResponse({'success_message': 'Ticket created!'})
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))