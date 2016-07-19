from django import template
from datetime import datetime, timedelta
register = template.Library()

@register.filter(name='lookup')
def lookup(value, arg):
	return value[arg]

@register.filter(name='due')

def due(start,end):
	return (end - start)/2 + start
