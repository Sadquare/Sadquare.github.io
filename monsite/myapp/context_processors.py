# context_processors.py

from .models import Notification

def notifications(request):
    notifications_exist = Notification.objects.exists()
    notifications_operations_count = Notification.objects.filter(type_notif='Operations').count()
    notifications_organes_count = Notification.objects.filter(type_notif='Organes').count()
    context = {
        'notifications_exist':notifications_exist,
        'notif_op' : notifications_operations_count,
        'notif_or' : notifications_organes_count,
    }
    return context