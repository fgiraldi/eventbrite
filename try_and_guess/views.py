from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint


def welcome(request):
    context = {}
    return render(request, 'try_and_guess/welcome.html', context)


def user_starts(request):
    new_game = Game()
    new_game.status = Game.GAME_STATUS_CHOICES['START']
    new_game.guesser = Game.GUESSER_CHOICES['USER']
    new_game.save()
    new_game.guess_number = randint(new_game.range_min, new_game.range_max)
    new_game.save()
    context = {'game': new_game}
    # return HttpResponseRedirect(reverse('user_guesses', args=(new_game.id,)))
    return user_guesses(request, new_game.id)


def user_guesses(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if game.status == Game.GAME_STATUS_CHOICES['START']:
        """ USER must start to guess"""
        game.status = Game.GAME_STATUS_CHOICES['USER_GUESSING']
        game.save()
        clue = 'You have just started'
    elif game.status == Game.GAME_STATUS_CHOICES['USER_GUESSING']:
        """ USER has started to guess.
        We must compare his number with the number to be guessed"""
        try_number = request.POST['user_number']
        # try_number = 0
        if try_number == game.guess_number:
            game.status = Game.GAME_STATUS_CHOICES['FINISHED']
            game.save()
            clue = 'You won'
        elif try_number < game.guess_number:
            clue = 'My number is bigger'
        else:
            clue = 'My number is smaller'
    else:
        clue = 'Estoy en cualquier estado %s' % game.status

    context = {'game': game, 'clue': clue}
    return render(request, 'try_and_guess/user_guesses.html', context)


def machine_starts(request):
    context = {}
    return render(request, 'try_and_guess/machine_starts.html', context)
