from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Schedule


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        scheduled_events = events.filter(start_time_day=day)

        this_day = ''

        for event in scheduled_events:
            this_day += f'<li class="calendar_list">{event.get_calendar_url}</li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span> <ul>{this_day}</ul></td>"

        else:
            return '<td></td>'

    def formatweek(self, this_week, events):

        week = ''

        for this_day, week_day in this_week:
            week += self.formatday(this_day, events)
            return f'<tr>{week}</tr>'

    def formatmonth(self, withyear=True):
        events = Schedule.objects.filter(start_time_year=self.year, start_time_month=self.month)
        this_calendar = f'<table border="0" cellpadding="0" class="calendar">\n'
        this_calendar += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        this_calendar += f'{self.formatweekheader()}\n'

        for week in self.monthdays2calendar(self.year, self.month):
            this_calendar += f'{self.formatweek(week, events)}\n'
            return this_calendar
