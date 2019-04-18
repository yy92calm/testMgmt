"""EasyTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from base.views import *

urlpatterns = [

    url(r'/project/', project_index),
    url(r'/project_add/', project_add),
    url(r'/project_update/', project_update),
    url(r'/project_delete/', project_delete),

    url(r'/case/', case_index),
    url(r'/case_xmind/', case_xmind),
    url(r'/case_export/', case_export),
    url(r'/case_update/', case_update),

    url(r'/reports/', emailList),
]

