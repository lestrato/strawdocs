from django.shortcuts import render
from basesite.views import *

class Team(BaseView):
    def get_fetch(self, request):
        self.template_to_view = 'team.html'

class Support(BaseView):
    def get_fetch(self, request):
        self.template_to_view = 'support.html'
