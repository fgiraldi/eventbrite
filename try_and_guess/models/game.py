from django.db import models
from enum import Enum


class Game(models.Model):
    GUESSER_CHOICE_USER = 'USER'
    GUESSER_CHOICE_MACHINE = 'MACHINE'

    GAME_STATUS_CHOICE_START = 'START'
    GAME_STATUS_CHOICE_USER_GUESSING = 'USER_GUESSING'
    GAME_STATUS_CHOICE_MACHINE_GUESSING = 'MACHINE_GUESSING'
    GAME_STATUS_CHOICE_FINISHED = 'FINISHED'

    status = models.CharField(
      max_length=25,      
      default=GAME_STATUS_CHOICE_START
    )
    guess_number = models.IntegerField(default=0)
    range_min = models.IntegerField(default=1)
    range_max = models.IntegerField(default=100)
    guesser = models.CharField(
      max_length=25,
      default=GUESSER_CHOICE_USER
    )

    def __str__(self):
        return "%s, %s is guessing [%s]" % (self.id, self.guesser, self.status)
