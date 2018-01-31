"""GoLearing URL Configuration

The `urlpatterns` list routes URLs to index. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function index
    1. Add an import:  from my_app import index
    2. Add a URL to urlpatterns:  url(r'^$', index.home, name='home')
Class-based index
    1. Add an import:  from other_app.index import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from GoEdu import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^GoLearing/hls/download/(.*)/(.*)/(.*)/$',index.download,name="download"),
    url(r'^GoLearing/hls/echo/(.*)/(.*)/$',index.echo),
    url(r'^GoLearing/hls/(.*)/(.*)/$',index.hlsroompage),
]
