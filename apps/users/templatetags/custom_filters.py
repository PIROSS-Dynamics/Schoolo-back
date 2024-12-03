from django import template
from django.utils.timezone import localtime

register = template.Library()

@register.filter
def calculate_top_position(start_date):
    start_date = localtime(start_date)  # Convert to localized time
    # Calculate the top position within the hour slot (50px per hour)
    return (start_date.minute / 60) * 50

@register.filter
def calculate_task_height(start_date, end_date):
    start_date = localtime(start_date)
    end_date = localtime(end_date)
    # Calculate the duration in minutes and set height accordingly
    duration_minutes = (end_date - start_date).seconds // 60
    return (duration_minutes / 60) * 50  # Adjust if your CSS hour height differs
