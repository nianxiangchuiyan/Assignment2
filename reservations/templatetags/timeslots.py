from django import template
from datetime import datetime, timedelta

register = template.Library()


@register.filter
def to(value, end):
    return range(value, end)


@register.filter
def add_time(start_time_str, minutes):
    h, m = map(int, start_time_str.split(':'))
    t = datetime(2000, 1, 1, h, m) + timedelta(minutes=minutes)
    return t.strftime('%H:%M')


@register.simple_tag
def half_hour_range():
    return [i * 30 for i in range(20)]  # 0, 30, ..., 570


@register.filter
def multiply(value, arg):
    return int(value) * int(arg)
