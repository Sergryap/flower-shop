from django.shortcuts import render
import json


def card(request):
    return render(request, 'card.html', context={})


def catalog(request):
    return render(request, 'catalog.html', context={})


def consultation(request):
    return render(request, 'consultation.html', context={})


def index(request):
    return render(request, 'index.html', context={})


def order_step(request):
    return render(request, 'order-step.html', context={})


def order(request):
    return render(request, 'order.html', context={})


def card(request):
    return render(request, 'card.html', context={})


def quiz(request):
    return render(request, 'order.html', context={})


def result(request):
    return render(request, 'result.html', context={})

