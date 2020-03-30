from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from datetime import timedelta, date
from FlowControling.models import HealthData, User, CycleLength
from FlowControling.forms import HealthForm,  ChangeDetailsForm
from .calendar import Calendar
from django.utils.safestring import mark_safe
from django.core.mail import send_mail

def welcome_mail(user_mail):
    email = [str(user_mail)]
    send_mail('Witaj we Flow!', 'Twoje konto zostało utworzone. '
                                'Cieszę się, że ze mną jesteś! \n '
                                'Jeśli masz pytania lub chciałabyś opowiedzieć'
                                ' mi o '
                                'swoim doświadczeniu z Flow napisz do mnie!'
                                ' ☺️ \n \n \n \n '
                                'Ściskam \n '
                                'Julita \n'
                                '❤️',
              'wedoourbestatflow@gmail.com', email, fail_silently=False)

class HomePage(View):
    def get(self, request):
        form = HealthForm()
        if request.user.is_authenticated:

            user = User.objects.get(username=request.user.username)
            if not CycleLength.objects.filter(user=user):
                cycle_length = CycleLength.objects.create(length= user.avg_cycle, user=user)
                welcome_mail(user.email)
                print("works!")

            ovulation_end = int(user.avg_cycle /2)
            ovulation_start = ovulation_end - 6

            cycle_day = date.today() - user.last_cycle
            cycle_day = int(cycle_day.days) +1

            if cycle_day > user.avg_cycle:
                cycle_length = cycle_day
            else:
                cycle_length = user.avg_cycle


            cycle_list = []
            for i in range(cycle_length):
                day = user.last_cycle + timedelta(days=i)
                if HealthData.objects.filter(user=user).filter(date=day).filter(bleeding__gte=1):
                    cycle_list.append("bleeding")
                elif ovulation_start <= i <= ovulation_end:
                    cycle_list.append("ovulation")
                else:
                    cycle_list.append("none")
            # cycle_list[0] = "bleeding" #pierwszy element cyklu = bleeding(foreva)

            context = {'cycle_list': cycle_list,'cycle_day' : cycle_day, 'form': form}
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
            cycle_day = form_date - user.last_cycle
            cycle_day = int(cycle_day.days)


            if (cycle_day >= 7 or cycle_day < 0) and int(bleeding) > 0:
                if cycle_day > 0:
                    cycle_length = CycleLength()
                    cycle_length.length = cycle_day
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
        data = HealthData.objects.filter(user=user)
        calendar = Calendar(year, month, data)
        html_calendar = calendar.formatmonth(year, month)
        context = {'calendar':mark_safe(html_calendar), "next_month": next_month, "prev_month": prev_month}
        return render(request, 'calendar.html', context)


class AccountView(View):
    def get(self, request):
        form = ChangeDetailsForm()
        if request.user.is_authenticated:
            context = {'form': form}
            return render(request, 'account.html', context)
        else:
            return redirect('/accounts/login')

    def post(self, request):
        form = ChangeDetailsForm(request.POST)
        user = User.objects.get(username=request.user.username)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            last_cycle = form.cleaned_data['last_cycle']
            avg_cycle = form.cleaned_data['avg_cycle']

            if first_name != None and first_name:
                user.first_name = first_name
            if last_name != None and last_name:
                user.last_name = last_name
            if email != None and email:
                user.email = email
            if last_cycle != None:
                user.last_cycle = last_cycle
            if avg_cycle != None:
                CycleLength.objects.filter(user=user).delete()
                user.avg_cycle = avg_cycle
            user.save()
            print(user.first_name, user.last_cycle, user.email, user.last_cycle, user.avg_cycle)
        return redirect('/account')


class StartView(View):
    def get(self, request):
        return render(request, 'start.html')


