from django.urls import path
from notifications import views

app_name = 'notifications'

urlpatterns = [
    path('bulk-notifications', views.BulkNotificationViewList.as_view()),
    path('bulk-notifications/<int:pk>', views.BulkNotificationView.as_view()),

    path('clients', views.ClientViewList.as_view()),
    path('clients/<int:pk>', views.ClientView.as_view())
]
