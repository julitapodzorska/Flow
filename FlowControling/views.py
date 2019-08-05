from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic


class LandingPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'home.html')
        else:
            return redirect('/accounts/login')

