from django.urls import path
from . import views

urlpatterns = [
    path('basket/',views.OrderView.as_view(),name='user-basket'),
    path('delete-from-basket/<int:product_id>/',views.delete_from_basket,name='user-delete-basket'),
    path('delete-all-from-basket/',views.delete_all_from_basket,name='user-delete-all-basket'),
]
