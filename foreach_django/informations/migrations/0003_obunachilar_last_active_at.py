# Generated by Django 5.1.4 on 2024-12-20 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informations', '0002_alter_kurslar_options_kurslar_matn_kurslar_rasm'),
    ]

    operations = [
        migrations.AddField(
            model_name='obunachilar',
            name='last_active_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Oxirgi faollik vaqti'),
        ),
    ]
