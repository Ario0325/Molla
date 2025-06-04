from jalali_date import datetime2jalali
from django.utils import timezone


def jalali_converter(time):
    jmonths = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

    time = timezone.localtime(time)

    j_date = datetime2jalali(time)

    time_string = "{} {} {} ساعت {}:{:02d}".format(
        j_date.day,
        jmonths[j_date.month - 1],
        j_date.year,
        time.hour,
        time.minute,
    )
    return time_string