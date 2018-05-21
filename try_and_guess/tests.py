from django.urls import reverse
from django.test import TestCase
from .models import Game
from random import randint
import math


class GameModelTests(TestCase):
    def test_game_initializes_correctly(self):
        """Verifies correct game status (START)
        right after initialization
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_USER)
        self.assertIs(game.status, Game.GAME_STATUS_CHOICE_START,
                      'Game does not init ok')

    def test_has_just_started(self):
        """After initialization, has_just_started()
        must return True
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_USER)
        self.assertTrue(game.has_just_started(),
                        'has_just_started() should be True')

    def test_user_guesses(self):
        """"After guesser (USER) choice being choosed
        user_guesses must inform correct status (USER_GUESSING)
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_USER)
        game.user_guesses()
        self.assertIs(game.status, Game.GAME_STATUS_CHOICE_USER_GUESSING,
                      'User should be guessing')

    def test_machine_guesses(self):
        """"After guesser (MACHINE) choice being choosed
        machine_guesses must inform correct status (MACHINE_GUESSING)
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_MACHINE)
        game.machine_guesses()
        self.assertIs(game.status, Game.GAME_STATUS_CHOICE_MACHINE_GUESSING,
                      'The machine should be guessing')

    def test_in_progress_when_user_guesses(self):
        """Verify in_progress() correct behaviour
        for both after-status (FINISHED and CANCEL)
        when the user is the guesser
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_USER)
        self.assertIs(game.in_progress(), True)
        game.user_guesses()
        self.assertIs(game.in_progress(), True)
        game.finish()
        self.assertIs(game.in_progress(), False)
        game.initialize(Game.GUESSER_CHOICE_USER)
        game.cancel()
        self.assertIs(game.in_progress(), False)

    def test_in_progress_when_machine_guesses(self):
        """Verify in_progress() correct behaviour
        for both after-status (FINISHED and CANCEL)
        when the machine is the guesser
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_MACHINE)
        self.assertIs(game.in_progress(), True)
        game.machine_guesses()
        self.assertIs(game.in_progress(), True)
        game.finish()
        self.assertIs(game.in_progress(), False)
        game.initialize(Game.GUESSER_CHOICE_MACHINE)
        game.cancel()
        self.assertIs(game.in_progress(), False)

    def test_compares_correctly(self):
        """Given an user number, Game must be able
        to compare it against its own guess_number.
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_USER)
        game.set_guess_number()
        must_return_bigger = game.guess_number - 1
        must_return_smaller = game.guess_number + 1
        must_return_equal = game.guess_number
        self.assertIs(game.compare_number(must_return_bigger), 'BIGGER')
        self.assertIs(game.compare_number(must_return_smaller), 'SMALLER')
        self.assertIs(game.compare_number(must_return_equal), 'EQUAL')

    def test_finish_when_user_guesses(self):
        """Confirm correct status after game is finished
        when the user is the guesser.
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_USER)
        game.user_guesses()
        game.finish()
        self.assertIs(game.status, Game.GAME_STATUS_CHOICE_FINISHED)

    def test_finish_when_machine_guesses(self):
        """Confirm correct status after game is finished
        when the user is the guesser.
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_MACHINE)
        game.machine_guesses()
        game.finish()
        self.assertIs(game.status, Game.GAME_STATUS_CHOICE_FINISHED)

    def test_is_finished_when_user_guesses(self):
        """Verify is_finished() correct behaviour
        when the user is the guesser.
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_USER)
        game.user_guesses()
        self.assertIs(game.is_finished(), False)
        game.finish()
        self.assertIs(game.is_finished(), True)

    def test_is_finished_when_machine_guesses(self):
        """Verify is_finished() correct behaviour
        when the machine is the guesser.
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_MACHINE)
        game.machine_guesses()
        self.assertIs(game.is_finished(), False)
        game.finish()
        self.assertIs(game.is_finished(), True)

    def test_cancel_when_user_guesses(self):
        """Verify cancel() correct behaviour
        when the user is the guesser
        for the three status (START, USER_GUESSING and MACHINE_GUESSING)
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_USER)
        game.cancel()
        self.assertIs(game.status, Game.GAME_STATUS_CHOICE_CANCELED)
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_USER)
        game.user_guesses()
        game.cancel()
        self.assertIs(game.status, Game.GAME_STATUS_CHOICE_CANCELED)

    def test_cancel_when_machine_guesses(self):
        """Verify cancel() correct behaviour
        when the machine is the guesser
        for the three status (START, USER_GUESSING and MACHINE_GUESSING)
        """
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_MACHINE)
        game.cancel()
        self.assertIs(game.status, Game.GAME_STATUS_CHOICE_CANCELED)
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_MACHINE)
        game.machine_guesses()
        game.cancel()
        self.assertIs(game.status, Game.GAME_STATUS_CHOICE_CANCELED)

    def test_effectiveness_at_guessing(self):
        """Can the machine guess ANY number in the given range?"""
        """First, grab a random number within the specified range."""
        user_number = randint(Game.GAME_DEFAULT_RANGE_MIN,
                              Game.GAME_DEFAULT_RANGE_MAX)
        """The algorythm used to let the machine guess is O(log2(n))
        since it's based in a binaty search. So, the maximum number of tries
        in order to guess a given unmber will be, in the worst case log2(n) + 1

        If, for any reason, someone wants to assure that this test works
        properly, just need to set the number_of_tries variable to a
        lower value than default (computed from the algorythm's Big O ).
        E.g. :
            number_of_tries = int(math.log2(Game.GAME_DEFAULT_RANGE_MAX) / 2)
        """
        number_of_tries = int(math.log2(Game.GAME_DEFAULT_RANGE_MAX)) + 1
        game = Game()
        game.initialize(Game.GUESSER_CHOICE_MACHINE)
        tried = 1
        user_response = ''
        while tried <= number_of_tries and user_response != 'EQUAL':
            if game.has_just_started():
                my_min, my_max, my_number = game.guess_user_number(
                    min=Game.GAME_DEFAULT_RANGE_MIN,
                    max=Game.GAME_DEFAULT_RANGE_MAX
                )
                game.machine_guesses()
            else:
                my_min, my_max, my_number = game.guess_user_number(
                    min=my_min,
                    max=my_max,
                    last=my_number,
                    comparison=user_response
                )
            user_response = simulate_user_response(user_number, my_number)
            tried += 1
        self.assertIs(user_response,
                      'EQUAL',
                      'Could not guess number %s in %s tries' % (user_number,
                                                                 tried)
                      )


def simulate_user_response(user_number, machine_number):
    """Simulates the answer provided by the user
    in order to provide feedback to test_effectiveness_at_guessing(),
    so I can asure the algorithm can guess any number.

    Args:
        user_number (int): user selected number to be guessed
        machine_number (int): returned value from Game.guess_user_number

    Returns:
        str: The result of comparing both numbers
            'BIGGER', 'SMALLER', 'EQUAL' accordingly
    """
    return ('EQUAL' if machine_number == user_number else
            'BIGGER' if machine_number < user_number else
            'SMALLER')
