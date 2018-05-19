from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Game


def welcome(request):
    context = {}
    return render(request, 'try_and_guess/welcome.html', context)


def user_starts(request):
    new_game = Game()
    new_game.initialize(Game.GUESSER_CHOICE_USER)
    # context = {'game': new_game}
    return user_guesses(request, new_game.id)


def user_guesses(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if game.has_just_started():
        """USER must start to guess"""
        game.user_guesses()
        clue = 'You have just started'
    elif game.status == Game.GAME_STATUS_CHOICE_USER_GUESSING:
        """USER has started to guess.
        We must compare his number with the number to be guessed
        """
        try:
            user_number = int(request.POST['user_number'])
        except ValueError as ve:
            clue = 'You must enter a unmber in order to try to guess'
        else:
            comparison = game.compare_number(user_number)
            if comparison == 'EQUAL':
                game.finish()
                clue = 'You won'
            elif comparison == 'BIGGER':
                clue = 'My number is bigger'
            else:
                clue = 'My number is smaller'
    else:
        clue = 'Estoy en cualquier estado %s' % game.status

    context = {'game': game, 'clue': clue}
    if game.is_finished():
        return render(request, 'try_and_guess/user_win.html', context)
    else:
        return render(request, 'try_and_guess/user_guesses.html', context)


def machine_starts(request):
    new_game = Game()
    new_game.initialize(Game.GUESSER_CHOICE_MACHINE)    
    context = {'game': new_game}
    return render(request, 'try_and_guess/machine_starts.html', context)


def machine_guesses(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if game.has_just_started():
        """MACHINE must start to guess"""
        my_min, my_max, my_number = game.guess_user_number(
            min=int(request.POST['minimal_value']),
            max=int(request.POST['maximal_value'])
        )
        game.machine_guesses()
        clue = 'Is it your number %s?' % my_number
    elif game.status == Game.GAME_STATUS_CHOICE_MACHINE_GUESSING:
        """MACHINE has started to guess."""
        if request.POST['comparison'] == 'EQUAL':
            context = {}
            return render(request, 'try_and_guess/machine_win.html', context)
        else:
            my_min, my_max, my_number = game.guess_user_number(
                min=int(request.POST['minimal_value']),
                max=int(request.POST['maximal_value']),
                last=int(request.POST['last_attempt']),
                comparison=request.POST['comparison']
            )
            clue = 'Is it your number %s?' % my_number
    else:
        clue = 'Estoy en cualquier estado %s' % game.status

    context = {'game': game,
               'clue': clue,
               'minimal_value': my_min,
               'maximal_value': my_max,
               'last_attempt': my_number
               }
    return render(request, 'try_and_guess/machine_guesses.html', context)
