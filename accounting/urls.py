from django.urls import path
from accounting import views

app_name = 'accounting'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('waybill/add/', views.WaybillCreateView.as_view(), name='waybill_add'),
    path('waybill/list/', views.WaybillListView.as_view(), name='waybill_list'),
    path('waybill/list/<int:pk>/', views.WaybillDetailView.as_view(), name='waybill_detail'),
    path('administrative/', views.AdministrativeView.as_view(), name='administrative'),
    path('worker/create/', views.WorkerCreateView.as_view(), name='worker_create'),
    path('worker/list/', views.WorkerListView.as_view(), name='worker_list'),
    path('worker/update/<int:pk>', views.WorkerUpdateView.as_view(), name='worker_update'),
    path('tally/', views.TallyCreateView.as_view(), name='tally'),
    path('tally/list/', views.TallyListView.as_view(), name='tally_list'),
    path('tally/update/<int:pk>', views.TallyUpdateView.as_view(), name='tally_update'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('order/add/', views.OrderCreateView.as_view(), name='order_add'),
    path('order/list/', views.OrderListView.as_view(), name='order_list'),
    path('order/list/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail')
]

