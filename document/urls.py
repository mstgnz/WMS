from django.urls import path
from document import views

app_name = 'document'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('minutes/add/', views.MinutesCreateView.as_view(), name='minutes_add'),
    path('minutes/list/', views.MinutesListView.as_view(), name='minutes_list'),
    path('minutes/list/<int:pk>/update/', views.MinutesUpdateView.as_view(), name='minutes_update'),
    path('writing/add/', views.WritingCreateView.as_view(), name='writing_add'),
    path('writing/list/', views.WritingListView.as_view(), name='writing_list'),
    path('writing/list/<int:pk>/update/', views.WritingUpdateView.as_view(), name='writing_update'),
    path('report/daily/add/', views.DailyReportCreateView.as_view(), name='report_add'),
    path('report/daily/list/', views.DailyReportListView.as_view(), name='report_list'),
]
