from django.db import models


# Create your models here.
class About(models.Model):
    banner_first_header = models.ImageField(null=True, upload_to='images/Banner/', verbose_name="عکس درباره ما هدر")
    text_our_view = models.TextField(verbose_name='متن دید ما')
    text_mission = models.TextField(verbose_name='متن ماموریت ما')
    banner_second = models.ImageField(null=True, upload_to='images/Banner/', verbose_name="عکس درباره ما وسط شماره 1")
    banner_third = models.ImageField(null=True, upload_to='images/Banner/', verbose_name="عکس درباره ما وسط شماره 2")
    text_who_we_are = models.TextField(verbose_name='متن ما که هستیم')
    banner_logo1 = models.ImageField(null=True, upload_to='images/Banner/logo/', verbose_name="عکس لوگو1")
    banner_logo2 = models.ImageField(null=True, upload_to='images/Banner/logo/', verbose_name="عکس لوگو2")
    banner_logo3 = models.ImageField(null=True, upload_to='images/Banner/logo/', verbose_name="عکس لوگو3")
    banner_logo4 = models.ImageField(null=True, upload_to='images/Banner/logo/', verbose_name="عکس لوگو4")
    banner_logo5 = models.ImageField(null=True, upload_to='images/Banner/logo/', verbose_name="عکس لوگو5")
    banner_logo6 = models.ImageField(null=True, upload_to='images/Banner/logo/', verbose_name="عکس لوگو6")
    banner_logo7 = models.ImageField(null=True, upload_to='images/Banner/logo/', verbose_name="عکس لوگو7")
    banner_logo8 = models.ImageField(null=True, upload_to='images/Banner/logo/', verbose_name="عکس لوگو8")
    banner_logo9 = models.ImageField(null=True, upload_to='images/Banner/logo/', verbose_name="عکس لوگو9")
    text_logo = models.TextField(verbose_name='متن معرفی لوگو')
    banner_person1 = models.ImageField(null=True, upload_to='images/Banner/person/', verbose_name="عکس اعضای تیم 1")
    text_person1 = models.TextField(verbose_name='اسم عضو تیم 1')
    text_job1 = models.TextField(verbose_name='شغل عضو تیم 1')
    text_bio1 = models.TextField(verbose_name='بیوگرافی عضو تیم 1')

    banner_person2 = models.ImageField(null=True, upload_to='images/Banner/person/', verbose_name="عکس اعضای تیم 2")
    text_person2 = models.TextField(verbose_name='اسم عضو تیم 2')
    text_job2 = models.TextField(verbose_name='شغل عضو تیم 2')
    text_bio2 = models.TextField(verbose_name='بیوگرافی عضو تیم 2')

    banner_person3 = models.ImageField(null=True, upload_to='images/Banner/person/', verbose_name="عکس اعضای تیم 3")
    text_person3 = models.TextField(verbose_name='اسم عضو تیم 3')
    text_job3 = models.TextField(verbose_name='شغل عضو تیم 3')
    text_bio3 = models.TextField(verbose_name='بیوگرافی عضو تیم 3')

    phone = models.CharField(max_length=13, verbose_name='شماره تماس')
    email = models.EmailField(max_length=200, verbose_name='ادرس ایمیل')
    address = models.CharField(max_length=300, verbose_name='ادرس محل')

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'
