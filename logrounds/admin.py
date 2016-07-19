from django.contrib import admin
from logrounds.models import *
# Register your models here.
admin.site.register(RoundType)
admin.site.register(LogDef)
admin.site.register(Period)
admin.site.register(Flags)
admin.site.register(FlagTypes)
admin.site.register(LogEntry)
admin.site.register(LogSet)