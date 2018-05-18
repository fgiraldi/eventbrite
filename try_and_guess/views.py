from django.shortcuts import render


def welcome(request):
    context = {}
    return render(request, 'try_and_guess/welcome.html', context)


def user_starts(request):
    context = {}
    return render(request, 'try_and_guess/user_starts.html', context)


def machine_starts(request):
    context = {}
    return render(request, 'try_and_guess/machine_starts.html', context)
