from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path("index/", views.index, name="index"),
    path("<int:pid>/detail/", views.detail, name="detail"),
    path("create/", views.create, name="create"),
    path("<int:pid>/likey/", views.likey, name="likey"),
    path("<int:pid>/myprod/", views.myprod, name="myprod"),
    path("mylist/", views.mylist, name="mylist"),
]