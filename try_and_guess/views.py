from django.shortcuts import render


def welcome(request):
    context = {}
    return render(request, 'try_and_guess/welcome.html', context)
