from django.db import models
from .groups import Group


class WorkingHours(models.Model):
    days = {
        "monday": "Monday",
        "tuesday": "Tuesday",
        "wednesday": "Wednesday",
        "thursday": "Thursday",
        "friday": "Friday",
        "saturday": "Saturday",
        "sunday": "Sunday",
    }

    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    day = models.CharField(max_length=255, choices=days)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_all_day = models.BooleanField()

    class Meta:
        db_table = "working_hours"
