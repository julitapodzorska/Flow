from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic


class LandingPage(View):
    def get(self, request):
        return render(request, 'home.html')

