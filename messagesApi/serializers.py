from rest_framework import serializers
from .models import *

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = "__all__"

    sender = serializers.SerializerMethodField()
    recipient = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    def get_sender(self, obj):

        sender_id = obj.sender.id
        sender_email = obj.sender.user.email.lower()
        sender_name = obj.sender.user.name.lower()
        context = {
            "id": sender_id,
            "email": sender_email,
            "name": sender_name
        }
        return context
    
    def get_recipient(self, obj):

        recipient_id = obj.recipient.id
        recipient_email = obj.recipient.user.email.lower()
        recipient_name = obj.recipient.user.name.lower()
        context = {
            "id": recipient_id,
            "email": recipient_email,
            "name": recipient_name
        }
        return context
    
    def get_created(self, obj):
        date_time = str(obj.created).split(" ")
        date = date_time[0]
        time = date_time[1].split(".")[0]
        context = {
            "date": date,
            "time": time,
        }
        return context
    
class MessageDeletedSerializer(serializers.ModelSerializer):

    message = MessageSerializer()

    class Meta:
        model = MessageDeleted
        fields = "__all__"

    # def to_representation(self, obj):
    #     representation = super().to_representation(obj)
    #     representation['message'] = MessageSerializer(obj.message).data
    #     return representation
