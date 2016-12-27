from django.shortcuts import render
from basesite.views import *

class Team(BaseView):
    def fetch(self, request):
        self.template_to_view = 'team.html'

class Support(BaseView):
    def fetch(self, request):
        self.template_to_view = 'support.html'
