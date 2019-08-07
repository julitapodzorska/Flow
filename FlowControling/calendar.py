from calendar import HTMLCalendar
from .models import HealthData
from datetime import date


class Calendar(HTMLCalendar):
    def __init__(self, year, month, data):
        self.year = year
        self.month = month
        self.data = data
        super(Calendar, self).__init__()

    def formatday(self, day, weekday):
        if day != 0:
            current_day = date(self.year, self.month, day)
            events_from_day = self.data.filter(date=current_day)
            events_html = ''
            for event in events_from_day:
                if event.bleeding:
                    events_html += f'<li style="color: red"> Krwawienie {event.get_bleeding_display()} </li>'
                if event.pain:
                    events_html += f'<li style="color: blue"> Ból {event.get_pain_display()} </li>'
                if event.energy:
                    events_html += f'<li style="color: green"> Poziom energii {event.get_energy_display()} </li>'
                if event.sex:
                    events_html += f'<li style="color: purple"> Seks {event.get_sex_display()} </li>'
                if event.mood:
                    events_html += f'<li style="color: deeppink"> Nastrój {event.get_mood_display()} </li>'
            if current_day == date.today():
                return f"<td class='today'><span class='date'>{day}</span><ul> {events_html} </ul></td>"
            return f"<td><span class='date'>{day}</span><ul> {events_html} </ul></td>"
        return '<td></td>'

