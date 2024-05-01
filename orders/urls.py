from django.urls import path
from . import views

urlpatterns = [
    # path('',views.HelloOrdersView.as_view(),name='hello-orders'),
    path('',views.OrderCreateListView.as_view(),name='order-create-list'),
    path('<int:order_id>/',views.OrderDetailView.as_view(),name='order-detail'),
    path('update-status/<int:order_id>/',views.UpdateOrderStatusView.as_view(),name='update-order-status'),
    path('user/<int:user_id>/orders/',views.UserOrdersView.as_view(),name='user-orders'),
    path('user/<int:user_id>/orders/<int:order_id>/',views.UserOrderDetail.as_view(),name='user-orders-detail'),
]
