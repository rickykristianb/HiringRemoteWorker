from django.urls import path
from . import views 

urlpatterns = [
    # MESSAGES
    path('send_email/', views.send_email, name='send_email'),
    path('reply_email/', views.send_reply_message, name='send_reply_message'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_message/', views.get_message, name='get_message'),
    path('read_message/<str:id>/', views.on_read_message, name='on_read_message'),
    path('get_sent_messages/', views.get_sent_messages, name='get_sent_messages'),
    path('get_deleted_messages/', views.get_deleted_messages, name='get_deleted_messages'),
    path('delete_message/<str:id>/', views.delete_message, name='delete_message'),
    path('delete_message_forever/<str:id>/', views.delete_message_forever, name='delete_message_forever'),
    path('delete_sent_message/<str:id>/', views.delete_sent_message, name='delete_sent_message'),
    path('total_inbox_message/', views.get_total_inbox_message, name='get_total_inbox_message'),
    path('get_inbox_pagination/', views.get_inbox_pagination, name='get_inbox_pagination'),
    path('count_unread_messages/', views.count_unread_messages, name='count_unread_messages'),
    path('get_sent_message_pagination/', views.get_sent_message_pagination, name='get_sent_message_pagination'),
    path('get_deleted_message_pagination/', views.get_deleted_message_pagination, name='get_deleted_message_pagination'),
]