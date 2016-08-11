from django import template
from datetime import datetime, timedelta
register = template.Library()

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

@register.filter(name='key')
def key(dict):
    return dict.keys()[0]

@register.filter(name='mytype')
def mytype(entry):
    return type(entry)

@register.filter(name='logtime')
def logtime(entry):
    if entry.log_time:
        return entry.log_time
    else:
        return 'failed'

@register.filter(name='due')
def due(start,end):
    return (end - start)/2 + start
