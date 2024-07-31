from .models import CustomUser, Invitation, Blum, SocialMedia, Tasks
from .serializers import UserSerializer, BlumSerializer, TasksSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from django.utils import timezone
from rest_framework.generics import CreateAPIView, ListAPIView
import datetime
from .permissions import IsAdminOrReadOnly, IsAdmin
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

@api_view(['POST'])
@permission_classes([AllowAny])
def register_or_login(request):
    if request.method == 'POST':
        telegram_id = request.data.get('telegram_id')
        username = request.data.get('username')
        name = request.data.get('first_name')
        avatar = request.data.get('avatar')
        if not telegram_id or not username:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(telegram_id=telegram_id, username=username)
            login(request, user)
            return Response({"message": "Welcome back"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(telegram_id=telegram_id, username=username, first_name=name, avatar=avatar)
            user.save()
            blum = Blum.objects.create(user=user, blum_amount=0, start_time=timezone.now())
            link = f"https://t.me/blum_azizbek_bot/Python Engeneer?start=er_{telegram_id}"
            invite = Invitation.objects.create(user=user, invite_link = link)
            blum.save()
            invite.save()
            return Response({"message": "Registered successfully"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def invitation_user_add(request, telegram_id, user_id):
    try:
        # Retrieve the user who is inviting
        user = CustomUser.objects.get(telegram_id=telegram_id)
        
        # Retrieve the user who is being invited
        invitation_user = CustomUser.objects.get(telegram_id=user_id)
        
        # Check if the invitation_user is already in the invited_users list of any invitation
        if Invitation.objects.filter(invited_users=invitation_user).exists():
            return Response({
                'message': 'User is already invited'
            }, status=status.HTTP_200_OK)
        
        # Retrieve or create the Invitation for the user
        invite, created = Invitation.objects.get_or_create(user=user)
        
        # Add the invitation_user to the invited_users list
        invite.invited_users.add(invitation_user)
        
        return Response({'message': 'Successfully invited'}, status=status.HTTP_201_CREATED)
    
    except CustomUser.DoesNotExist:
        return Response({'message': 'User or invited user not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def start_farming(request):
    id = request.data.get("id")
    user = CustomUser.objects.get(telegram_id=id)
    blum = Blum.objects.get(user=user)
    current_time = timezone.now()

    time_elapsed = current_time - blum.start_time
    hours_passed = time_elapsed.total_seconds() / 3600
    print(hours_passed)
    if hours_passed < 9:
        return Response({
            "message": "Farming doesn't end yet."
        }, status=status.HTTP_200_OK)
    elif blum.claim == True:
        return Response({
            "message": "Blum coins doesn't claimed."
        }, status=status.HTTP_200_OK)
    else:
        blum.start_time = current_time
        blum.save()
        return Response({
            "message": "Farming has been started."
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def claim(request):
    id = request.data.get("id")
    user = CustomUser.objects.get(telegram_id = id)
    blum = Blum.objects.get(user=user)


    blum.blum_amount += 57
    blum.claim = False
    blum.save()
    return Response({
        "message": "Coins has been claimed."        
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_blum_status(request):
    id = request.data.get("id")
    user = CustomUser.objects.get(telegram_id=id)
    blum = Blum.objects.get(user=user)
    
    current_time = timezone.now()
    
    time_elapsed = current_time - blum.start_time
    hours_passed = time_elapsed.total_seconds() / 3600

    if hours_passed >= 9:
        blum.claim = True
        blum.save()
        return Response({
            "message": "Claim is opened"
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "message": "Time limit is not reached..."
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def daily_reward_checker(request):
    id = request.data.get("id")
    if not id:
        return Response({"error": "Missing user ID"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(telegram_id=id)
        blum = Blum.objects.get(user=user)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    current_date = timezone.now().date()

    if blum.date:
        if blum.date < current_date:
            blum.date = current_date
            blum.blum_amount += 57
            blum.save()
            return Response({
                "message": "Daily Reward has been claimed"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Daily Reward already claimed today"
            }, status=status.HTTP_200_OK)
    
    blum.date = current_date
    blum.save()
    return Response({
        "message": "Day has been added."
    }, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_blum(request, id):
    user = CustomUser.objects.get(telegram_id=id)
    blum = Blum.objects.get(user=user)

    return Response({
        "count": blum.blum_amount,
        "username": blum.user.username,
        "avatar": blum.user.avatar.url
    },
    status=status.HTTP_200_OK)


class TaskViewSet(ModelViewSet):
    queryset = Tasks.objects.all()  
    serializer_class = TasksSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(task_status=True).exclude(task_users=user)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def start_task_handler(request):
    user_id = request.data.get("user_id")
    task_id = request.data.get("task_id")

    user = get_object_or_404(CustomUser, telegram_id=user_id)
    task = get_object_or_404(Tasks, id=task_id)
    blum = get_object_or_404(Blum, user=user)

    if not task.task_users.filter(id=user.id).exists():
        task.task_users.add(user)
        blum.blum_amount += task.task_prize_amount
        task.save()
        blum.save()
        return Response({
            "message": f"User has been added to {task.task_name} task."
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "message": "User already done this task."
        }, status=status.HTTP_200_OK)

class GetUSers(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class BlumUserViewSet(ModelViewSet):
    queryset = Blum.objects.all()
    serializer_class = BlumSerializer
    permission_classes = [IsAdmin]

@api_view(["POST"])
@permission_classes([AllowAny])
def check_admin(request):
    id = request.data.get("telegram_id")
    user = CustomUser.objects.get(telegram_id=id)
    if user:
        if user.is_admin == True:
            return Response({
                "message": "Ok"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "It is not admin"
            }, status=status.HTTP_403_FORBIDDEN)
    return Response({
        "message": "User not found"
    }, status=status.HTTP_404_NOT_FOUND)