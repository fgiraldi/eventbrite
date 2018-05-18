from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Game
from .models.game import GameStatusChoice, GuesserChoice
from random import randint


def welcome(request):
    context = {}
    return render(request, 'try_and_guess/welcome.html', context)


def user_starts(request):
    new_game = Game()
    new_game.status = GameStatusChoice.START
    new_game.guesser = GuesserChoice.USER
    new_game.save()
    new_game.guess_number = randint(new_game.range_min, new_game.range_max)
    new_game.save()
    context = {'game': new_game}
    return HttpResponseRedirect(reverse('user_guesses', args=(new_game.id,)))


def user_guesses(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    context = {'game': game}
    return render(request, 'try_and_guess/user_guesses.html', context)


def machine_starts(request):
    context = {}
    return render(request, 'try_and_guess/machine_starts.html', context)
