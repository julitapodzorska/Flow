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
            bleeding_days = len(HealthData.objects.filter(date__gte=user.last_cycle).filter(bleeding__gte=1).filter(user = user))
            cycle_day = date.today() - user.last_cycle
            cycle_day = int(cycle_day.days) +1
            print(bleeding_days, cycle_day)
            context = {'cycle_length':range(1, request.user.avg_cycle+1), 'cycle_day' : cycle_day, 'form': form, 'bleeding_days': bleeding_days}
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
            date_offset = form.cleaned_data['date']
            date_offset = date.today() - timedelta(days= int(date_offset))

            date_diff = date_offset - request.user.last_cycle
            date_diff = int(date_diff.days)
            print(date_diff)

            if (date_diff > 2 or date_diff < 0) and int(bleeding) > 0:
                print(date_diff)
                user = User.objects.get(username=request.user.username)
                user.last_cycle = date_offset
                user.save()


            if ( HealthData.objects.filter(date = date_offset )):
                health_data = HealthData.objects.filter(date= date_offset).first()
            else:
                health_data = HealthData()
            health_data.date = date_offset
            health_data.bleeding = bleeding
            health_data.pain = pain
            health_data.mood = mood
            health_data.sex = sex
            health_data.energy = energy
            health_data.user = User.objects.get(username=request.user.username)
            health_data.save()
        return redirect("/")

