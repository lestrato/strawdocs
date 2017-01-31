from django.shortcuts import render
from basesite.views import *

class Team(BaseView):
    def get_fetch(self, request, template_items):
        return render(request, 'team.html', template_items)
    def post_fetch(self, request):
        return HttpResponseRedirect('/')

class Support(BaseView):
    def get_fetch(self, request, template_items):
        return render(request, 'support.html', template_items)
    def post_fetch(self, request):
        return HttpResponseRedirect('/')
