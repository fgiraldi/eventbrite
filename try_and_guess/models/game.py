from django.db import models
from enum import Enum


class GameStatusChoice(Enum):
    START = 'START',
    USER_GUESSING = 'USER_GUESSING',
    MACHINE_GUESSING = 'MACHINE_GUESSING',
    FINISHED = 'FINISHED'


class GuesserChoice(Enum):
    USER = 'USER',
    MACHINE = 'MACHINE'


class Game(models.Model):
    GUESSER_CHOICES = (
        ('USER', 'USER'),
        ('MACHINE', 'MACHINE')
    )
    GAME_STATUS_CHOICES = (
        ('START', 'START'),
        ('USER_GUESSING', 'USER_GUESSING'),
        ('MACHINE_GUESSING', 'MACHINE_GUESSING'),
        ('FINISHED', 'FINISHED')
    )
    status = models.CharField(
      max_length=25,
      choices=GAME_STATUS_CHOICES,
      default='START'
    )
    guess_number = models.IntegerField(default=0)
    range_min = models.IntegerField(default=1)
    range_max = models.IntegerField(default=100)
    guesser = models.CharField(
      max_length=15,
      choices=GUESSER_CHOICES,
      default='USER'
    )

    def __str__(self):
        return "%s, %s is guessing [%s]" % (self.id, self.guesser, self.status)
