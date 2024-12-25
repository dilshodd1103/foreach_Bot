# from django.utils.timezone import now
# from foreach_django.informations.models import Obunachilar
#
# def update_user_activity(telegram_id, username=None, full_name=None):
#     """
#     Foydalanuvchining oxirgi faollik vaqtini yangilaydi yoki yangi foydalanuvchi qo'shadi.
#     """
#     try:
#         user = Obunachilar.objects.get(telegram_id=telegram_id)
#         user.last_active_at = now()
#         user.save()
#     except Obunachilar.DoesNotExist:
#         Obunachilar.objects.create(
#             telegram_id=telegram_id,
#             username=username,
#             full_name=full_name,
#             last_active_at=now()
#         )
