from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification, User
from apps.users.models import Relation, Student
from .serializers import NotificationSerializer

class NotificationListView(APIView):

    def get(self, request):
        """
        Retrieve all notifications for the user whose ID is sent in the request.
        If `unread=true` is in the parameters, return only unread notifications.
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=user_id)
        unread_only = request.query_params.get('unread') == 'true'
        notifications = Notification.objects.filter(receiver=user)

        if unread_only:
            notifications = notifications.filter(is_read=False)

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NotificationDetailView(APIView):

    def get(self, request, pk):
        """
        Retrieve details of a specific notification.
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        notification = get_object_or_404(Notification, pk=pk, receiver=user)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """
        Mark a notification as read.
        """
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        notification = get_object_or_404(Notification, pk=pk, receiver=user)
        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Delete a notification.
        """
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        notification = get_object_or_404(Notification, pk=pk, receiver=user)
        notification.delete()
        return Response({"message": "Notification deleted"}, status=status.HTTP_204_NO_CONTENT)

class SendRelationRequestView(APIView):

    def post(self, request):
        """
        Allow a teacher or a parent to send a relationship request using the recipient's email.
        """
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        if getattr(user, "role", None) not in ['teacher', 'parent']:
            return Response({"error": "Only teachers and parents can send relationship requests."}, 
                            status=status.HTTP_403_FORBIDDEN)

        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        receiver = get_object_or_404(User, email=email)
        
        # Check if a relationship request already exists
        existing_notification = Notification.objects.filter(
            sender=user, receiver=receiver, type='relation', is_read=False
        ).exists()
        if existing_notification:
            return Response({"error": "A pending relationship request already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the notification for the relationship request
        notification = Notification.objects.create(
            type='relation',
            title='New Relationship Request',
            description=f'{user.first_name} {user.last_name} has sent you a relationship request.',
            sender=user,
            receiver=receiver
        )
        
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRelationsView(APIView):

    def get(self, request):
        """
        Retrieve all relations for the user whose ID is sent in the request.
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=user_id)

        # Vérifier si l'utilisateur est un élève
        try:
            student = Student.objects.get(id=user.id)
            relations = Relation.objects.filter(student=student)
        except Student.DoesNotExist:
            # Sinon, on suppose qu'il est parent ou prof
            relations = Relation.objects.filter(sender=user)

        # Sérialiser les relations
        relations_data = [
            {
                'relation_type': relation.relation_type,
                'sender': {
                    'id': relation.sender.id,
                    'name': f'{relation.sender.first_name} {relation.sender.last_name}'
                },
                'student': {
                    'id': relation.student.id,
                    'name': f'{relation.student.first_name} {relation.student.last_name}'
                }
            }
            for relation in relations
        ]

        return Response(relations_data, status=status.HTTP_200_OK)


    
class AcceptRelationView(APIView):

    def post(self, request, notification_id):
        """
        Accept a relationship request (either from a teacher or a parent).
        """
        # Récupérer la notification et l'utilisateur actuel
        notification = get_object_or_404(Notification, id=notification_id)
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Trouver l'utilisateur
        user = get_object_or_404(User, id=user_id)

        # Vérifier si la notification est de type 'relation'
        if notification.type != 'relation':
            return Response({"error": "Not a relation request."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier que l'utilisateur actuel est bien le destinataire de la notification
        if notification.receiver != user:
            return Response({"error": "You are not the recipient of this notification."}, status=status.HTTP_403_FORBIDDEN)

        # Récupérer l'instance de Student si l'utilisateur est un étudiant
        if user.role == 'student':
            student = get_object_or_404(Student, id=user.id)  # Chercher l'étudiant avec le même ID que l'utilisateur
        else:
            return Response({"error": "Only students can have relations."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier le rôle du sender et créer la relation en fonction
        if notification.sender.role == 'teacher':
            teacher = notification.sender
            # Créer une relation de type 'school' (scholaire)
            relation = Relation(student=student, sender=teacher, relation_type='school')
            relation.save()
            print(f"Relation créée: {relation}")
        elif notification.sender.role == 'parent':
            parent = notification.sender
            # Créer une relation de type 'parent' (parental)
            relation = Relation(student=student, sender=parent, relation_type='parent')
            relation.save()
            print(f"Relation créée: {relation}")
        else:
            return Response({"error": "Sender must be either a Teacher or Parent."}, status=status.HTTP_400_BAD_REQUEST)

        # Marquer la notification comme lue
        notification.is_read = True
        notification.save()

        # Réponse confirmant l'ajout de la relation
        return Response({"message": "Relation request accepted and relationship established."}, status=status.HTTP_200_OK)
