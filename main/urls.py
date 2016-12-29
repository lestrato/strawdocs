"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from document.views import *
from basesite.views import *
from information.views import *

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # all documents/about page
    url(r'^$', Home.as_view()),
    url(r'^doc/(?P<doc_slug>[a-z||A-Z||0-9]+)$', DocumentOverview.as_view()),
    url(r'^doc/(?P<doc_slug>[a-z||A-Z||0-9]+)/(?P<question_url>[a-z||A-Z||0-9||_]+)$', QuestionView.as_view()),

    # information, login not required
    url(r'^team/$', Team.as_view()),
    url(r'^support/$', Support.as_view()),

    # only if logged in
    url(r'^create/$', CreateDocument.as_view()),

    # misc
    url(r'^logout/$', logout_page),
    url(r'^admin/', admin.site.urls),

    # testing error urls, these get changed when the server is in production
    url(r'^400/$', bad_request.as_view()),
    url(r'^403/$', permission_denied.as_view()),
    url(r'^404/$', page_not_found.as_view()),
    url(r'^500/$', server_error.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
