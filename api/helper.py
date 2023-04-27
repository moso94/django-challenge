from api.models import Reservation, Room
from django.utils import timezone
from django.db.models import Q


def checkReservationData(res, orig: Reservation = None):
    now = timezone.now()
    if orig is None or orig.start > now:
        if res['start_at'] > now:
            if res['start_at'] < res['end_at']:
                reservations = list(Reservation.objects.filter(~Q(Q(start_at__lt=res['start_at'],
                                                                    end_at__lte=res['start_at'])
                                                                  | Q(start_at__gte=res['end_at'],
                                                                      end_at__gt=res['end_at'])),
                                                               room_id=res['room'].id))
                if len(reservations) == 0:
                    return (True, '')
                else:
                    reason = "This space is occupied at the requested time"
            else:
                reason = 'Unable to schedule reservations that ends before start'
        else:
            reason = 'Unable to schedule reservations for the past'
    else:
        reason = 'Unable to edit reservations that have already started'
    return (False, reason)


def getEmptyRooms(params):
    if 'start_at' in params and 'end_at' in params:
        roomIds = list(Reservation.objects.filter(~Q(Q(start_at__lt=params['start_at'],
                                                       end_at__lte=params['start_at'])
                                                     | Q(start_at__gte=params['end_at'],
                                                         end_at__gt=params['end_at'])))
                       .values_list('room_id', flat=True).distinct())
        return (True, Room.objects.exclude(id__in=roomIds))
    return (False, None)
