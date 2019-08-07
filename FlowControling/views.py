from django.shortcuts import render, redirect
from django.views import View, generic
from datetime import timedelta, date
from FlowControling.models import HealthData, User, CycleLength
from FlowControling.forms import HealthForm
from .calendar import Calendar
from django.utils.safestring import mark_safe

class HomePage(View):
    def get(self, request):
        form = HealthForm()
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)


            if not CycleLength.objects.filter(user=user):
                cycle_length = CycleLength()
                cycle_length.length = user.avg_cycle
                cycle_length.user = user
                cycle_length.save()


            try:
                bleeding_days = HealthData.objects.filter(date__gte=user.last_cycle).filter(bleeding__gte=1).filter(user = user)
                bleeding_days = bleeding_days.order_by('date')
                bleeding_length = bleeding_days.last().date - user.last_cycle
                bleeding_length = int(bleeding_length.days)+1
                if bleeding_length > 8:
                    bleeding_length = 8
            except:
                bleeding_length = 1

            ovulation_start = int(user.avg_cycle /2)
            ovulation_end = ovulation_start + 5

            cycle_day = date.today() - user.last_cycle
            cycle_day = int(cycle_day.days) +1

            if cycle_day > user.avg_cycle:
                menu_length = cycle_day
            else:
                menu_length = user.avg_cycle

            context = {'cycle_length':range(1, menu_length+1),
                       'cycle_day' : cycle_day, 'form': form, 'bleeding_days': bleeding_length,
                       'ovulation_start': ovulation_start, 'ovulation_end': ovulation_end}
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

            user = User.objects.get(username=request.user.username)

            if (date_diff > 7 or date_diff < 0) and int(bleeding) > 0:
                length = date_offset - user.last_cycle
                length = int(length.days)
                if length > 0:
                    cycle_length = CycleLength()
                    cycle_length.length = length
                    cycle_length.user = user
                    cycle_length.save()
                    user.avg_cycle = computeAverageCycle(CycleLength.objects.filter(user=user))

                user.last_cycle = date_offset
                user.save()


            if HealthData.objects.filter(date=date_offset):
                health_data = HealthData.objects.get(date=date_offset)
            else:
                health_data = HealthData()

            health_data.date = date_offset
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
        print(delta)
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

