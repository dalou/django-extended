# encoding: utf-8
import datetime
from django.utils.safestring import mark_safe

def format_date_range_html(
    start_date=None,
    end_date=None,
    start_hour=None,
    end_hour=None,
    divider='<br/>'):


    if end_date and start_date:
        if  start_date.day == end_date.day and \
            start_date.month == end_date.month and \
            start_date.year == end_date.year:

            if start_hour and end_hour:
                return mark_safe(
                    start_date.strftime("Le %A %d %B ") + divider + "de " + start_hour.strftime("%H:%M") + " à " + end_hour.strftime("%H:%M")
                )
            elif start_hour:
                return mark_safe(
                    start_date.strftime("Le %A %d %B ") + divider + "à partir de " + start_hour.strftime("%H:%M")
                )
            elif end_hour:
                return mark_safe(
                    start_date.strftime("Le %A %d %B ") + divider + "jusqu'à " + end_hour.strftime("%H:%M")
                )
            else:
                return mark_safe(
                    start_date.strftime("Le %A %d %B ") + divider + "toute la journée"
                )


        else:
            if start_hour and end_hour:
                return mark_safe(
                    start_date.strftime("Du %A %d %B ") + divider + "à " + start_hour.strftime("%H:%M") +
                    divider + end_date.strftime("Jusqu'au %A %d %B ") + divider + "à " + end_hour.strftime("%H:%M")
                )
            elif start_hour:
                return mark_safe(
                    start_date.strftime("Du %A %d %B ") + divider + "à " + start_hour.strftime("%H:%M") +
                    divider + end_date.strftime("Jusqu'au %A %d %B")
                )
            elif end_hour:
                return mark_safe(
                    start_date.strftime("Du %A %d %B") +
                    divider + end_date.strftime("Jusqu'au %A %d %B  ") + divider + "à " + end_hour.strftime("%H:%M")
                )
            else:
                return mark_safe(
                    start_date.strftime("Du %A %d %B") +
                    divider + end_date.strftime("Jusqu'au %A %d %B  ") + divider
                )
    elif start_date:
        if start_hour and end_hour:
            return mark_safe(
                start_date.strftime("À partir du  %A %d %B  ") + divider + "de " + start_hour.strftime("%H:%M") + " à " + end_hour.strftime("%H:%M")
            )
        elif start_hour:
            return mark_safe(
                start_date.strftime("À partir du  %A %d %B  ") + divider + "à " + start_hour.strftime("%H:%M")
            )
        elif end_hour:
            return mark_safe(
                start_date.strftime("À partir du  %A %d %B ") + divider + "jusqu'à " + end_hour.strftime("%H:%M")
            )
        else:
            return mark_safe(
                start_date.strftime("À partir du %A %d %B")
            )

    elif end_date:
        if start_hour and end_hour:
            return mark_safe(
                end_date.strftime("Jusqu'au %A %d %B ") + divider + "de " + start_hour.strftime("%H:%M") + " à " + end_hour.strftime("%H:%M")
            )
        elif start_hour:
            return mark_safe(
                end_date.strftime("Jusqu'au %A %d %B ") + divider + "à partir de " + start_hour.strftime("%H:%M")
            )
        elif end_hour:
            return mark_safe(
                end_date.strftime("Jusqu'au %A %d %B ") + divider + "à " + end_hour.strftime("%H:%M")
            )
        else:
            return mark_safe(
                start_date.strftime("Jusqu'au %A %d %B")
            )
    else:
        if start_hour and end_hour:
            return mark_safe(
                "Aujourd'hui " + divider + start_hour.strftime("de %H:%M") + " à " + end_hour.strftime("%H:%M")
            )
        elif start_hour:
            return mark_safe(
                "Aujourd'hui " + divider + start_hour.strftime("à %H:%M")
            )
        elif end_hour:
            return mark_safe(
                "Aujourd'hui " + divider + end_hour.strftime("jusqu'à %H:%M")
            )
        else:
            return None
