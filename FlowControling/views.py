from django.shortcuts import render, redirect
from django.views import View
from datetime import timedelta, date
from FlowControling.models import HealthData, User, CycleLength
from FlowControling.forms import HealthForm
from .calendar import Calendar
from django.utils.safestring import mark_safe

class HomePage(View):
    def get(self, request):
        form = HealthForm()
        if request.user.is_authenticated: #jesli uzytkownik jest zautentyfikowany
            user = User.objects.get(username=request.user.username) # pobieramy jego dane

            if not CycleLength.objects.filter(user=user): # jesli uzytkownik nie ma danych dotyczacych dlugosci cyklu
                cycle_length = CycleLength.objects.create(length= user.avg_cycle, user=user) # tworzymy obiekt z wprowadzonymi danymi

            ovulation_end = int(user.avg_cycle /2)
            ovulation_start = ovulation_end - 6

            cycle_day = date.today() - user.last_cycle # aktualny dzien cyklu zwraca datę
            cycle_day = int(cycle_day.days) +1 # zamieniamy na dni w incie i dodajemy 1, jesli roznica jest rowna 0 znaczy, ze jestesmy w pierwszym dniu cyklu

            if cycle_day > user.avg_cycle: # jesli aktualny cykl jest dluzszy od sredniej dlugosci cyklu
                cycle_length = cycle_day # to przypisujemy mu wartosc aktualnego dnia cyklu
            else:
                cycle_length = user.avg_cycle # jesli nie to dlugosc jest rowna sredniej dlugosci

            cycle_list = [] # kontener na zawartosc paska
            for i in range(cycle_length): # petla wykona się tyle razy ile dni jest w cyklu
                day = user.last_cycle + timedelta(days=i) #bierzemy kolejno dni cyklu
                if HealthData.objects.filter(user=user).filter(date=day).filter(bleeding__gte=1): # i dla każdego po kolei sprawdzamy, jakie ma dane w bazie
                    cycle_list.append("bleeding") # jesli bleeding jest wiekszy niz 1(choices) to znaczy, ze bleeding
                elif ovulation_start <= i <= ovulation_end: # jesli dzien jest w zakresie owulacji, oznacza, że na ten dzien jest dana owulacja
                    cycle_list.append("ovulation")
                else:
                    cycle_list.append("none") #jesli nie ma zadnej danej = none
            # cycle_list[0] = "bleeding" #pierwszy element cyklu = bleeding(foreva)

            context = {'cycle_list': cycle_list,'cycle_day' : cycle_day, 'form': form} # do html'a wysyłamy cały kontener z danymi, aktualny dzien cyklu i formularz.
            return render(request, 'home.html', context)
        else:
            return redirect('/accounts/login')

    def post(self, request):
        form = HealthForm(request.POST)
        user = User.objects.get(username=request.user.username)
        if form.is_valid():
            bleeding = form.cleaned_data['bleeding']
            pain = form.cleaned_data['pain']
            mood = form.cleaned_data['mood']
            sex = form.cleaned_data['sex']
            energy = form.cleaned_data['energy']
            form_date = form.cleaned_data['date']

            form_date = date.today() - timedelta(days=int(form_date))
            date_diff = form_date - user.last_cycle
            date_diff = int(date_diff.days)


            if (date_diff >= 7 or date_diff < 0) and int(bleeding) > 0:
                if date_diff > 0:
                    cycle_length = CycleLength()
                    cycle_length.length = date_diff
                    cycle_length.user = user
                    cycle_length.save()
                    user.avg_cycle = computeAverageCycle(CycleLength.objects.filter(user=user))

                user.last_cycle = form_date
                user.save()


            if HealthData.objects.filter(user=user).filter(date=form_date):
                health_data = HealthData.objects.filter(user=user).filter(date=form_date).first()
            else:
                health_data = HealthData()

            health_data.date = form_date
            health_data.bleeding = bleeding
            health_data.pain = pain
            health_data.mood = mood
            health_data.sex = sex
            health_data.energy = energy
            health_data.user = user
            health_data.save()
        return redirect("/")



def computeAverageCycle(cycles_lengths):
    print(cycles_lengths)
    average = 0
    for cycle_length in cycles_lengths:
        average += cycle_length.length
    average /= len(cycles_lengths)
    return int(average)


class CalendarView(View):
    def get(self, request, delta):
        day = date.today().day
        year = date.today().year
        month = date.today().month - delta
        if month < 1:
            month = 12 + month
            year -= 1

        prev_month = delta+1
        next_month = delta-1 if delta > 0 else 0
        user = User.objects.get(username=request.user.username)
        dupa = HealthData.objects.filter(user=user)
        calendar = Calendar(year, month, dupa)
        html_calendar = calendar.formatmonth(year, month)
        context = {'calendar':mark_safe(html_calendar), "next_month": next_month, "prev_month": prev_month}
        return render(request, 'calendar.html', context)
