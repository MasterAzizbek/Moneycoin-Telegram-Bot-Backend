from django.urls import path
from .views import register_or_login, TaskViewSet,check_admin, invitation_user_add, claim, start_farming, start_task_handler, check_blum_status, daily_reward_checker, get_blum, GetUSers, BlumUserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('users', GetUSers)
router.register('blum_users', BlumUserViewSet)

urlpatterns = [
    path('enter/', register_or_login),
    path('invite/<int:telegram_id>/<int:user_id>/', invitation_user_add),
    path('claim/', claim),    
    path('start_farming/', start_farming),
    path('start_task/', start_task_handler),
    path('check_blum/', check_blum_status),
    path('daily_reward/', daily_reward_checker),
    path('get_blum/<int:id>/', get_blum),
    path('check/', check_admin),
] + router.urls
