from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from userApi.serializers import *
from rest_framework.response import Response
from datetime import datetime
from .utils import *
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db.models import Q
from .models import *
from .serializers import *

# Create your views here.
# MESSAGES
@api_view(["POST"])
def send_email(request):
    print(request.data)
    if request.method == "POST":
        subject="Email From Portfolio Website",
        from_email = request.data["email"]
        to_email = "contact@rickykristianbutarbutar.com"
        name = request.data["name"]
        message_body = request.data["messageBody"].split("\n")

        context = {
                    "name": name,
                    "from_email": from_email,
                    "message": message_body
                }
        
        message=render_to_string("send_mail.html", context)

        try:
            send_mail(
                subject[0],
                message,
                from_email,
                [to_email],
                fail_silently=False, 
                html_message=message
                )
        except Exception as err:
            context = {
                "error": "Could not send email"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            context = {
                "success": "Your message has been sent to \n contact@rickykristianbutarbutar.com"
            }
            return Response(context, status=status.HTTP_200_OK)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request):
    try:
        user = request.user
        data = request.data
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile)
        try:
            recipient = Profile.objects.get(user__email=(data.get("to_user")).lower())

            Message.objects.create(
                sender=user_profile, 
                recipient=recipient,
                name=serializer.data["name"],
                email=serializer.data["email"],
                subject=data.get("subject"),
                body=data.get("message_body"),
                created=datetime.now())
            return Response({"success": "Message send"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Recipient {data.get("to_user").lower()} not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_reply_message(request):
    try:
        user = request.user
        data = request.data
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile)
        message_body = data["formData"]["message_body"]
        recipient_reply_data = data["reply_data"]
        try:
            msg_recipient = Profile.objects.get(user__email=(recipient_reply_data["sender"]["email"]).lower())
            Message.objects.create(
                sender=user_profile, 
                recipient=msg_recipient,
                name=msg_recipient.name,
                email=msg_recipient.email,
                subject=recipient_reply_data["subject"],
                body=message_body,
                prev_reply_message=recipient_reply_data["body"],
                created=datetime.now())
            return Response({"success": "Message sent"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Recipient {data.get("to_user").lower()} not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_message(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        message = Message.objects.filter(recipient=user_profile, is_deleted_by_recipient=False)
        count_is_read = message.filter(is_read=False).count()
        serializer = MessageSerializer(message, many=True)
        
        context = {
            "data": serializer.data,
            "is_read_count": count_is_read
        }
        return Response(context, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def on_read_message(request, id):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        message = Message.objects.get(recipient=user_profile, id=id)
        message.is_read = True
        message.date_read = datetime.now()
        message.save()
        return Response({"success": "read"},status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_message(request, id):
    try:
        user = request.user
        try:
            user_profile = Profile.objects.get(user=user)
            message = Message.objects.get(recipient=user_profile, id=id)
            message.is_deleted_by_recipient = True
            message.save()
            return Response({"success": "Message deleted"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_message_forever(request, id):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        try:
            delete_message_forever = Message.objects.get(recipient=user_profile, id=id)
            MessageDeleted.objects.create(message=delete_message_forever)
        except Exception as e:
            delete_message_forever = Message.objects.get(sender=user_profile, id=id)
            MessageDeleted.objects.create(message=delete_message_forever)
        finally:
            return Response({"success": "Message deleted forever."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_deleted_messages(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        deleted_messages = Message.objects.filter(
                Q(recipient=user_profile, is_deleted_by_recipient=True) |
                Q(sender = user_profile, is_deleted_by_sender = True)
        ).exclude(
            Q(messagedeleted__deleted_at__isnull=False)
        )
        serializer = MessageSerializer(deleted_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_200_OK)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_sent_messages(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        message = Message.objects.filter(sender=user_profile, is_deleted_by_sender=False)
        count_is_read = message.filter(is_read=False).count()
        serializer = MessageSerializer(message, many=True)
        context = {
            "data": serializer.data,
            "is_read_count": count_is_read
        }
        return Response(context, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def delete_sent_message(request, id):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        message = Message.objects.get(sender=user_profile, id=id)
        message.is_deleted_by_sender = True
        message.save()
        return Response({"success": "Sent message has been deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_total_inbox_message(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        total_inbox_message = Message.objects.filter(recipient=user_profile, is_deleted_by_recipient=False).count()
        return Response({"total": total_inbox_message}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_inbox_pagination(request):
    '''GET MESSAGES BASED ON PAGE PAGINATED'''
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        message = Message.objects.filter(recipient=user_profile, is_deleted_by_recipient=False)
        total_inbox_message = Message.objects.filter(recipient=user_profile, is_deleted_by_recipient=False).count()
                
        # PAGINATOR
        paginator = MessagesResultsSetPagination()
        result_page = paginator.paginate_queryset(message, request)
        serializer = MessageSerializer(result_page, many=True)

        context = {
            "data": serializer.data,
            "total_inbox": total_inbox_message
        }

        return Response(context, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def count_unread_messages(request):
    '''FOR INBOX UNREAD MESSAGE NOTIFICATION'''
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        total_unread_message = Message.objects.filter(recipient=user_profile, is_read=False, is_deleted_by_recipient=False).count()
        return Response(total_unread_message, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_sent_message_pagination(request):
    '''GET SENT MESSAGES BASED ON PAGE PAGINATED'''
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        message = Message.objects.filter(sender=user_profile, is_deleted_by_sender=False)
        total_sent_message = Message.objects.filter(sender=user_profile, is_deleted_by_sender=False).count()
        # PAGINATOR
        paginator = MessagesResultsSetPagination()
        result_page = paginator.paginate_queryset(message, request)
        serializer = MessageSerializer(result_page, many=True)

        context ={
            "data": serializer.data,
            "total_sent_message": total_sent_message
        }

        return Response(context, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_deleted_message_pagination(request):
    '''GET DELETED MESSAGES BASED ON PAGE PAGINATED'''
    try:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        deleted_messages = Message.objects.filter(
                Q(recipient=user_profile, is_deleted_by_recipient=True) |
                Q(sender = user_profile, is_deleted_by_sender = True,)
        ).exclude(
            Q(messagedeleted__deleted_at__isnull=False)
        )

        total_deleted_message = deleted_messages.count()

        # PAGINATOR
        paginator = MessagesResultsSetPagination()
        result_page = paginator.paginate_queryset(deleted_messages, request)
        serializer = MessageSerializer(result_page, many=True)

        context_page = {
            "data": serializer.data,
            "total_deleted_message": total_deleted_message
        }

        return Response(context_page, status=status.HTTP_200_OK)
    except Exception as e:
        serializer = MessageSerializer(deleted_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)