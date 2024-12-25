from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Xabar_yuborish, Statistika, Malumotlar, Kurslar, Obunachilar

admin.site.unregister(Group)


@admin.register(Statistika)
class StatistikaAdmin(admin.ModelAdmin):
    list_display = ('all_subscribers', 'for_last_month', 'latest_news_readers')


class KurslarAdmin(admin.ModelAdmin):
    list_display = ('nom', 'tarif',)
    search_fields = ('nom',)
    list_filter = ('nom',)


admin.site.register(Kurslar, KurslarAdmin)


class ObunachilarAdmin(admin.ModelAdmin):
    list_display = (
    'username',  'full_name', 'phone_num', 'last_active_at', 'language',
    'admin','telegram_id',  'joined_at')
    search_fields = (
        'username', 'phone_num', 'full_name')
    list_filter = ('language', 'admin')
    ordering = ('-joined_at',)
    readonly_fields = ('joined_at',)


admin.site.register(Obunachilar, ObunachilarAdmin)


@admin.register(Xabar_yuborish)
class Xabar_yuborishAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'sent_date', 'send_to_all')
    search_fields = ('content_type', 'message_content')
    list_filter = ('content_type', 'send_to_all')
    date_hierarchy = 'sent_date'


@admin.register(Malumotlar)
class MalumotlarAdmin(admin.ModelAdmin):
    list_display = ('admins', 'last_message_sent_date')
