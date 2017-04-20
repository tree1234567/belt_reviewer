from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^home$', views.home_page, name="homepage"),
    url(r'^login$', views.login, name="login"),
    url(r'^register$', views.register, name="register"),
    url(r'^add_book$', views.add_book, name="add_book"),
    url(r'^create_book$', views.create_book, name="create_book"),
    url(r'^book_page/(?P<id>\d+)', views.book_page, name="book_page"),
    url(r'^create_review/(?P<id>\d+)$', views.create_review, name='create_review'),
    url(r'logout', views.logout, name="logout"),
    url(r'^user_page/(?P<id>\d+)$', views.user_page, name="user_page"),
    url(r'delete_review/(?P<id>\d+)/book/(?P<book_id>\d+)$', views.delete_review, name="delete_review"),

]
