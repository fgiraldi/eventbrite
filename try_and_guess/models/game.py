from django.db import models
from enum import Enum


class GuesserChoice(Enum):
    USER = 'USER',
    MACHINE = 'MACHINE'

    def __str__(self):
        return self.name


class GameStatusChoice(Enum):
    START = 'START',
    USER_GUESSING = 'USER_GUESSING',
    MACHINE_GUESSING = 'MACHINE_GUESSING',
    FINISHED = 'FINISHED'

    def __str__(self):
        return self.name


class Game(models.Model):
    status = models.CharField(
      max_length=25,
      choices=[(tag, tag.value) for tag in GameStatusChoice],
      default=GameStatusChoice.START
    )
    guess_number = models.IntegerField(default=0)
    range_min = models.IntegerField(default=1)
    range_max = models.IntegerField(default=100)
    guesser = models.CharField(
      max_length=15,
      choices=[(tagg, tagg.value) for tagg in GuesserChoice],
      default=GuesserChoice.USER
    )

    def __str__(self):
        return "%s, %s is guessing [%s]" % (self.id, self.guesser, self.status)
