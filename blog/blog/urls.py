from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from . import views

admin.autodiscover()

router = routers.SimpleRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
