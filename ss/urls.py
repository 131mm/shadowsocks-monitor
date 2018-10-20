from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name='ss'
urlpatterns=[
    url(r'^$',views.home,name='home'),
    url(r'^user/$',views.user_info,name='user_info'),
    url(r'^add',views.add_user,name='add_user'),
    url(r'^delete',views.delete_user,name='delete_user')
]
urlpatterns += staticfiles_urlpatterns()
