from django.urls import path 
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('cat/<cat>/brand/<brand>/', views.ProductListView.as_view(), name='product-brands-list'),
    path('cat/<cat>/tag/<tag>/', views.ProductListView.as_view(), name='product-tags-list'),
    path('tag/<tag>/', views.ProductListView.as_view(), name='product-no-cat-tags-list'),
    path('cat/<cat>/',views.ProductListView.as_view(),name='product-categories-list'),
    path('detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-product-to-favorite/', views.add_product_to_favorite, name='add-product-to-favorite'),
    path('add-product-to-basket/', views.add_product_to_basket, name='add-product-to-basket'),
    path('qustion-and-answer/',views.QustionAndAnswers,name='qustion-and-answer'),
    path('new-comment/',views.NewComment,name='new-comment'),
    path('comment-likes-and-dislikes/',views.comment_likes_and_dislikes,name='comment-likes-and-dislikes'),
]
