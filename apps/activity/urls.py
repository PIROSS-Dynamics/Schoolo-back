from django.urls import path
from .views import NotificationListView, NotificationDetailView, SendRelationRequestView, AcceptRelationView, UserRelationsView, SendMessageView

urlpatterns = [
    path('api/notifications/', NotificationListView.as_view(), name='notification-list'),
    path('api/notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('api/user-relations/', UserRelationsView.as_view(), name='user-relations'),
    path('api/relation-request/', SendRelationRequestView.as_view(), name='send-relation-request'),
    path('api/accept-relation/<int:notification_id>/', AcceptRelationView.as_view(), name='accept-relation-request'),
    path("api/send-message/", SendMessageView.as_view(), name="send-message"),
]
