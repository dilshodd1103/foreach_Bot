from django.db import models


# Kurslar modeli
class Kurslar(models.Model):
    nom = models.CharField(verbose_name="Kurs nomi", max_length=255)
    tarif = models.TextField(verbose_name="Kursga ta'rif bering")
    rasm = models.ImageField(
        verbose_name="Kurs rasmi",
        upload_to="kurslar_rasmlari/",
        blank=True,
        null=True
    )
    matn = models.TextField(verbose_name="Kurs uchun matn", blank=True, null=True)

    class Meta:
        verbose_name = "2. Kurslar"
        verbose_name_plural = "2. Kurslar"

    def __str__(self):
        return self.nom


# Obunachilar modeli
class Obunachilar(models.Model):
    username = models.CharField(verbose_name="Foydalanuvchi username", max_length=150, unique=False, null=False)
    full_name = models.CharField(verbose_name="Foydalanuvchining ismi", max_length=150, unique=False, null=True)
    phone_num = models.CharField(verbose_name="Telefon raqami", max_length=15, unique=True, null=True)
    admin = models.BooleanField(default=False)
    language = models.CharField(
        verbose_name="Til",
        max_length=15,
        choices=[('uz', 'O\'zbekcha'), ('ru', 'Русский')],
        default='uz'
    )
    telegram_id = models.BigIntegerField(verbose_name="Telegram ID ", unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_active_at = models.DateTimeField(verbose_name="Oxirgi faollik vaqti", null=True, blank=True)

    class Meta:
        verbose_name = "3.  Obunachilar"
        verbose_name_plural = "3.  Obunachilar"

    def __str__(self):
        return self.full_name


# Xabar yuborish obunachilari bilan bog'lanish (obunachilarni tanlash)
class Xabar_yuborish(models.Model):
    content_type = models.CharField(verbose_name="Xabar turi", max_length=50)
    content = models.TextField(verbose_name="Matn, video yoki rasm uchun link jo'nating")
    sent_date = models.DateTimeField(auto_now_add=True)
    send_to_all = models.IntegerField(default=False)

    # Barcha obunachilarga yuborish yoki alohida tanlangan obunachilarga yuborish uchun alohida maydon
    obunachilar = models.ManyToManyField('Obunachilar', blank=True)

    class Meta:
        verbose_name = "4.  Xabarlar"
        verbose_name_plural = "4.   Xabarlar"

    def __str__(self):
        return self.content


# Statistika modeli
class Statistika(models.Model):
    all_subscribers = models.IntegerField(verbose_name='Barcha obunachilar')
    for_last_month = models.IntegerField(verbose_name='Oxirgi oyda qushilganlar')
    latest_news_readers = models.IntegerField(verbose_name="Oxirgi xabar necha kishiga jo'natilgan")

    class Meta:
        verbose_name = "1.  Statistika"
        verbose_name_plural = "1.   Statistika"

    def __str__(self):
        return str(self.all_subscribers)


# Ma'lumotlar modeli
class Malumotlar(models.Model):
    admins = models.IntegerField()
    last_message_sent_date = models.DateTimeField(null=True)  # Oxirgi xabar yuborilgan sana

    class Meta:
        verbose_name = "6.  Malumotlar"
        verbose_name_plural = "6.   Malumotlar"

    def __str__(self):
        return f"Adminlar  {self.admins}  ta"
