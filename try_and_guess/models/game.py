from django.db import models
from enum import Enum
from random import randint


class Game(models.Model):
    GUESSER_CHOICE_USER = 'USER'
    GUESSER_CHOICE_MACHINE = 'MACHINE'

    GAME_STATUS_CHOICE_START = 'START'
    GAME_STATUS_CHOICE_USER_GUESSING = 'USER_GUESSING'
    GAME_STATUS_CHOICE_MACHINE_GUESSING = 'MACHINE_GUESSING'
    GAME_STATUS_CHOICE_FINISHED = 'FINISHED'
    GAME_STATUS_CHOICE_CANCELED = 'CANCELED'

    GAME_DEFAULT_RANGE_MIN = 1
    GAME_DEFAULT_RANGE_MAX = 100

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

    def initialize(self, guesser):
        self.status = Game.GAME_STATUS_CHOICE_START
        self.guesser = guesser
        self.range_min = Game.GAME_DEFAULT_RANGE_MIN
        self.range_max = Game.GAME_DEFAULT_RANGE_MAX
        self.save()

    def set_guess_number(self):
        """Chooses a random number to be guessed by the user."""
        self.guess_number = randint(self.range_min, self.range_max)
        self.save()

    def has_just_started(self):
        return self.status == Game.GAME_STATUS_CHOICE_START

    def user_guesses(self):
        """Sets the USER as the guesser."""
        self.status = Game.GAME_STATUS_CHOICE_USER_GUESSING
        self.set_guess_number()
        self.save()

    def compare_number(self, user_number):
        """Informs how the guess_number compares to
        the number introduced by the user.

        Args:
            user_number (int): The number introduced by the user

        Returns:
            str: The result of comparing both numbers
                'BIGGER', 'SMALLER', 'EQUAL' accordingly
        """
        return ('EQUAL' if self.guess_number == user_number else
                'BIGGER' if self.guess_number > user_number else
                'SMALLER')

    def machine_guesses(self):
        """Sets the MACHINE as the guesser."""
        self.status = Game.GAME_STATUS_CHOICE_MACHINE_GUESSING
        self.save()

    def get_magical_number(self, min, max):
        """Performs the binary search between min and max."""
        return (min + max) // 2

    def guess_user_number(self, min, max, last=0, comparison=''):
        """Try to guess the user designed mistery number
        Args:
            min, max (int): parameters for shrinking the scope of values
            last (int): last attempted number
            comparison (str): 'BIGGER', 'SMALLER' according to user input.
        """
        if self.has_just_started():
            return_min = min
            return_max = max
        elif comparison == 'BIGGER':
            return_min = last + 1
            return_max = max
        else:
            return_min = min
            return_max = last - 1
        return_last = self.get_magical_number(return_min, return_max)
        return return_min, return_max, return_last

    def finish(self):
        """Ends the game, establishing the FINISHED status."""
        self.status = Game.GAME_STATUS_CHOICE_FINISHED
        self.save()

    def is_finished(self):
        return (self.status == Game.GAME_STATUS_CHOICE_FINISHED)

    def in_progress(self):
        in_progress_status = [Game.GAME_STATUS_CHOICE_MACHINE_GUESSING,
                              Game.GAME_STATUS_CHOICE_USER_GUESSING,
                              Game.GAME_STATUS_CHOICE_START]
        return self.status in in_progress_status

    def cancel(self):
        """Cancels a game due to user decition."""
        self.status = Game.GAME_STATUS_CHOICE_CANCELED
        self.save()
