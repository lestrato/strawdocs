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
from account.views import *
from account.views import recover_email

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # all documents/about page
    url(r'^$', Home.as_view(), name="home"),
    url(r'^doc/(?P<doc_slug>[a-z||A-Z||0-9]+)$', DocumentOverview.as_view(), name="overview"),
    url(r'^doc/(?P<doc_slug>[a-z||A-Z||0-9]+)/(?P<question_slug>[a-z||A-Z||0-9||_]+)$', QuestionView.as_view(), name="question"),

    # information, login not required
    url(r'^team/$', Team.as_view(), name="team"),
    url(r'^support/$', Support.as_view(), name="support"),

    # document creation
    url(r'^create/$', CreateDocument.as_view(), name="create"),

    # account settings
    url(r'^account/$', Settings.as_view(), name="settings"),
    url(r'^account/recovery/$', Recovery.as_view(), name="recovery"),

    url(r'^recover_email/$', recover_email, name="recover_email"),

    # misc
    url(r'^logout/$', logout_page, name="logout"),
    url(r'^admin/', admin.site.urls, name="admin"),

    # # testing error urls, these get changed when the server is in production
    # url(r'^400/$', bad_request.as_view(), name="400"),
    # url(r'^403/$', permission_denied.as_view(), name="403"),
    # url(r'^404/$', page_not_found.as_view(), name="404"),
    # url(r'^500/$', server_error.as_view(), name="500"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
