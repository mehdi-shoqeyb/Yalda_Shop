from django.urls import path 
from . import views

urlpatterns = [
    path('counter/',views.CounterPage.as_view(), name='user-panel-counter'),
    path('info/',views.InformationPage.as_view(), name='user-panel-info'),
    path('last-orders/',views.LastOrdersView.as_view(), name='user-panel-last-orders'),
    path('order-detail/<int:order_id>',views.OrderDetailView.as_view(),name='order-detail'),
    path('order-factor/<int:order_id>',views.OrderDetailView.as_view(),name='order-factor'),
    path('favorites/',views.FavoriteProductsPage.as_view(), name='user-panel-favorite-products'),
    path('change-password',views.ChangePasswordPage.as_view(),name='user-panel-change-password-page'),
]
