from django.conf.urls import url


from . import views


urlpatterns = [

 #url(r'^admin/', admin.site.urls),
 url(r'^account/', views.accountSettings, name='account'),
 url(r'^user/', views.userPage, name='user'),

 url(r'^logout/', views.logOut, name='logout'),
 url(r'^login/', views.loginPage, name='login'),
 url(r'^register/', views.register, name='register'),

 url(r'^delete_order/(?P<pk>\d+)/$', views.deleteOrder, name='delete_order'),
 url(r'^update_order/(?P<pk>\d+)/$', views.updateOrder, name='update_order'),
 url(r'^create_order/', views.createOrder, name='create_order'),

 url(r'^products/', views.products, name='products'),
 url(r'^customer/(?P<pk>\d+)/$', views.customer, name='customer'),
 
 url(r'', views.home, name='home'),
 
   

]