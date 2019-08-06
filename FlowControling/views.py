from django.shortcuts import render, redirect
from django.views import View
from datetime import timedelta, date
from FlowControling.models import HealthData, User
from FlowControling.forms import HealthForm



class HomePage(View):
    def get(self, request):
        form = HealthForm()
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            cycle_day = date.today() - user.last_cycle
            cycle_day = int(cycle_day.days) +1
            context = {'cycle_length':range(1, request.user.avg_cycle +1), 'cycle_day' : cycle_day, 'form': form}
            return render(request, 'home.html', context)
        else:
            return redirect('/accounts/login')

    def post(self, request):
        form = HealthForm(request.POST)
        if form.is_valid():
            bleeding = form.cleaned_data['bleeding']
            pain = form.cleaned_data['pain']
            mood = form.cleaned_data['mood']
            sex = form.cleaned_data['sex']
            energy = form.cleaned_data['energy']
            notes = form.cleaned_data['notes']
            date_offset = form.cleaned_data['date_offset']
            print(date_offset)
            if ( HealthData.objects.filter(date = date.today() ).exists() ):
                health_data = HealthData.objects.filter(date= date.today()).first()
            else:
                health_data = HealthData()
            health_data.date = date.today()
            health_data.bleeding = bleeding
            health_data.pain = pain
            health_data.mood = mood
            health_data.sex = sex
            health_data.energy = energy
            health_data.notes = notes
            health_data.user = User.objects.get(username=request.user.username)
            health_data.save()
        return redirect("/")

