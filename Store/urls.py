from django.urls import path, include

from Store import views 



urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.OrdersList.as_view(), name='orders'),
    path( "latest-products/", views.ProductLatestView.as_view(), name="latest-products"),
    path( "product-list/", views.ProductListView.as_view(), name="product-list"),
    path( "products/search/", views.search, name="product-search"),
    path( "products/<slug:category_slug>/<slug:product_slug>/", views.ProductDetailView.as_view(), name="product"),
    path( "products/<slug:category_slug>/", views.CategoryDetailView.as_view(), name="category-product"),
    
]


