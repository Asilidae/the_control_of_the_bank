from django.db import models
from django.utils.timezone import localtime

class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def is_strange(self, delta_seconds=3600):
      hour, minute, second, delta = self.get_duration()
      return delta.total_seconds() >= delta_seconds
    
    def get_duration(self):
      if self.leaved_at:
        cur_time = localtime(self.leaved_at) # перевод в местное время
      else:
        cur_time = localtime() # текущее местное время если человек в хранилище
      entered_time = localtime(self.entered_at)
      delta = cur_time - entered_time
      total_minute, second = divmod(delta.seconds, 60)
      hour, minute = divmod(total_minute, 60) 
      return hour, minute, second, delta

    def is_visit_long(self, minutes=60):
      hour, minute, second, delta = self.get_duration()
      return delta.total_seconds() >= (minutes * 60)

    def format_duration(self):
      hour, minute, second, _ = self.get_duration()
      return '{h}:{m}:{s}'.format(h=hour, m=minute, s=second)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved="leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )
