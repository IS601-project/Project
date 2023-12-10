from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  # Admin
                  path('admin/', views.admin, name='admin'),
                  path('admin', views.admin, name='admin'),
                  path('admin/add_category/', views.add_category, name='add_category'),
                  path('admin/list_categories/', views.list_categories, name='list_categories'),
                  path('admin/edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
                  path('admin/delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
                  path('admin/add_product/', views.add_product, name='add_product'),
                  path('admin/list_products/', views.list_products, name='list_products'),
                  path('admin/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
                  path('admin/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
                  path('list_checkout', views.list_checkout, name='list_checkout'),
                  path('list_checkout/', views.list_checkout, name='list_checkout'),

                  # Site
                  path('', views.index, name='index'),
                  path('index/', views.index, name='index'),
                  path('index', views.index, name='index'),
                  path('home/', views.index, name='home'),
                  path('women', views.women, name='women'),
                  path('women/', views.women, name='women'),
                  path('shop_all', views.women, name='shop_all'),
                  path('shop_all/', views.women, name='shop_all'),
                  path('cart/', views.cart, name='cart'),
                  path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
                  path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
                  path('product_detail/<int:product_id>', views.product_detail, name='product_detail'),
                  path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
                  path('checkout', views.checkout, name='checkout'),
                  path('checkout/', views.checkout, name='checkout'),
                  path('checkout_success', views.checkout, name='checkout_success'),
                  path('checkout_success/', views.checkout, name='checkout_success'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
