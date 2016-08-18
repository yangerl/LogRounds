from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from datetime import date, datetime, time, timedelta
from django.core.exceptions import ValidationError
import re

# Create your models here.


@python_2_unicode_compatible
class Period (models.Model):
    """ This defines the periodicity of the Round. """
    
    CONV_DICT = {
        'Days' : 'days',
        'Hours' : 'hours',
        'Minutes' : 'minutes',
    }

    name = models.CharField(max_length=100,unique=True)
    scale = models.IntegerField(null=False, blank=False, help_text="Time between Sets")
    unit = models.CharField(max_length=10, help_text="Units for the scale (days, hours, or minutes)")

    def parse_period(self):
        try:
            return timedelta(**{self.CONV_DICT[self.unit] : self.scale})
        except KeyError:
            raise Exception("uncaught unit type")
    def __str__(self):
        return self.name

class RoundType(models.Model):
    """ This defines a series of columns. """

    name = models.CharField(max_length=50)
    #describe the purpose of the round etc.
    desc = models.TextField(max_length=None)
    start_date = models.DateTimeField()

    period = models.ForeignKey(Period, on_delete = models.CASCADE)

    phase_days = models.IntegerField()
    phase_hours = models.IntegerField()
    phase_min = models.IntegerField()
    def parse_phase(self):
        return timedelta(days = self.phase_days,
            minutes = self.phase_min,
            hours = self.phase_hours)

    def get_absolute_url(self):
        return reverse('logrounds:detail', args=[str(self.pk)])

    def __str__(self):
        return self.name

class LogDef(models.Model):
    """ This represents a 'column' of data """
    rt = models.ForeignKey(RoundType, on_delete=models.CASCADE,
            related_name = 'col')
    name = models.CharField(max_length=100)
    # Give info about the data being collected, location, safety etc.
    desc = models.TextField(max_length=None, null=True, blank=True)
    is_qual_data = models.BooleanField(default=False)
    units = models.CharField(null=True, max_length=20, blank=True)
    # units might be moved to 'data types class'

    low_low = models.FloatField(null=True, blank=True, verbose_name='Absolute Minimum Bound')
    high_high = models.FloatField(null=True, blank=True, verbose_name='Absolute Maximum Bound')
    low = models.FloatField(null=True, blank=True, verbose_name='Expected Minimum Bound')
    high = models.FloatField(null=True, blank=True, verbose_name='Expected Maximum Bound')

class LogSet(models.Model):
    MISSED_PARTIAL = -1
    MISSED = 0
    IN_PROGRESS = 1
    IN_PROGRESS_LATE = 2
    COMPLETE = 3
    COMPLETE_LATE = 4
    Status = (
        (MISSED_PARTIAL, 'Missed (Partial)'),
        (MISSED, 'Missed'),
        (IN_PROGRESS,'In Progress'),
        (IN_PROGRESS_LATE, 'In Progress (Late)'),
        (COMPLETE, 'Complete'),
        (COMPLETE_LATE, 'Complete (Late)')
    )
    #  This represents a 'row' in a log
    rt = models.ForeignKey(RoundType, on_delete=models.CASCADE, 
                        related_name='row')

    # NOTE: Unsure what's going on here.

    start_time = models.DateTimeField()
    next_time = models.DateTimeField()
    log_time = models.TimeField(null=True, blank=True)
    status = models.IntegerField(null=True, choices=Status)
    # objects = LogSetManager()

    

    def latest_logtime(self):
        logentry_qs = LogEntry.objects.filter(lg_set=self).order_by('-log_time')
        if not logentry_qs:
            return None
        else:
            return logentry_qs[0].log_time

    def duedate(self):
        my_logdef = LogDef.objects.filter(rt = self.rt).count()
        if (my_logdef != 0):
            return (self.next_time-self.start_time)/2 + self.start_time
        else:
            return None
    def status_update(self,logdef_qs):
        logentry_qs = LogEntry.objects.filter(lg_set=self)
        this_lgdf_set  = logentry_qs.values_list('lg_def', flat=True)

        due_date = self.duedate()
        latest_logtime = self.latest_logtime()

        newstatus = None
        # True if completed, False if incomplete, default=False
        complete = False
        # True if empty, false if non-empty, default=False
        empty = False

        if this_lgdf_set.count() == 0:
            empty = True
        elif logdef_qs.count() >= this_lgdf_set.count():

            # if number of LogEntries w/ distinct LogDefs == total number
            # of LogDefs, then the LogSet has all values filled, hence
            # complete = True

            # >= because if there are 5 hourly logdefs, and 10 daily logdefs
            # this_lgdf_set will only have 5 if working with hourly, while
            # logdef_qs will have 15 (5+10). probably depracated

            complete = True

        if (not empty) and (complete) and (latest_logtime <= due_date):
            # set status to Complete (ontime) (3)
            newstatus = LogSet.COMPLETE
        elif (not empty) and (complete) and (latest_logtime > due_date):
            # set status to Complete (late) (4)
            newstatus = LogSet.COMPLETE_LATE
        elif (empty) and (not complete):
            # set status to missed (full) (0)
            newstatus = LogSet.MISSED

        elif (not empty) and (not complete):
            # set status to missed (partial) (-1)
            newstatus = LogSet.MISSED_PARTIAL
        else:
            raise Exception('something went wrong with status settings')

        return newstatus

    def __str__(self):
        name = RoundType.objects.get(pk=self.rt.id).name
        return  "Round Name: " + name \
                + "\tStart:\t" + str(self.start_time) \
                + "\tNext:\t" + str(self.next_time)


class LogEntry(models.Model):
    lg_set = models.ForeignKey(LogSet, on_delete=models.CASCADE)

    lg_def = models.ForeignKey(LogDef, on_delete=models.CASCADE)

    parent = models.OneToOneField('self', null=True, blank=True, 
                related_name='prev_edit')
    num_value = models.FloatField(null=True, blank=True)
    select_value = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    log_time = models.DateTimeField(null=False, blank=False, 
                default=timezone.now)

    def check_value_type(self):
        # Checks and corrects the entry values.
        # If the logdef is qual value then it nulls all quantative values.
        # If the logdef is quant value then it nulls out select value.

        this_logdef = self.lg_def
        qual_val = this_logdef.is_qual_data
        if (qual_val):
            self.num_value = None
        else:
            self.select_value = None


    def create_flags(self):
        # Create Flags to determine if it is out of bounds
        # If flag exists already toggle the boolean
        self.check_bounds()

        # Create flags determining the Timelyness of the entry
        # Missed and Not Started entries don't exist in DB so
        # they do not have flags. Late flags (0 is not late, 1 is late .
        # In-progress is not-applcable b/c an entry is either completed
        # or has not been started, no such thing so doesnt have flag

        self.check_tardy()

    def check_tardy(self):
        # Creates a flag for whether the entry is on-time or late
        this_logset = self.lg_set
        this_start = self.lg_set.start_time
        this_next = this_logset.next_time
        this_duedate = (this_next - this_start)/2 + this_start
        is_late = 0

        note = 'if entry is on-time value=0, if late value=1'
        if (self.log_time > this_duedate):
            is_late = 1

        # NOTE: You can replace this whole block with this:
        #   flag_type, c = FlagTypes.objects.get_or_create(flag_name="Late")

        flag_type, created = FlagTypes.objects.get_or_create(flag_name = "Late")


        # NOTE: try/except/else - your else block will run every time after a
        #       try block succeeds. So if exists_already is set, else will be
        #       called.
        try:
            exists_already = Flags.objects.get(log_entry=self, flag=flag_type)
        except Flags.DoesNotExist:
            #if doesnt exist, create it
            new_flag=Flags(
                log_entry=self,
                flag=flag_type,
                flag_value=is_late,
                note=note
            )
            new_flag.save()


    def check_bounds(self):
        # Checks that the values are inside bounds.
        low = self.lg_def.low
        high = self.lg_def.high
        val = self.num_value
        note = 'if inside range value=0,if outside range value=1'
        boolean = 0
        if(val < low or val > high):
            boolean = 1
        flag_type, created = FlagTypes.objects.get_or_create(flag_name = "Outside Range")
        try:
            exists_already = Flags.objects.get(log_entry=self,flag=flag_type)
        except Flags.DoesNotExist:
            new_flag = Flags(
                log_entry=self,
                flag=flag_type,
                flag_value=boolean,
                note=note,
            )
            new_flag.save()

    def save(self, *args, **kwargs):
        # create next logset if possible
        try:
            self.check_data()
            self.check_unique()

        except Exception as inst:
            if (inst.args == ('high',) or inst.args ==('low',)):
                raise ValidationError('Outside of Absolute Range, check your data')
            elif inst.args == ('nuts',):
                raise inst
            else:
                raise inst
        self.check_value_type()
        super(LogEntry,self).save(*args,**kwargs)
        self.lg_set.log_time = self.log_time
        self.lg_set.save()
        self.create_flags()

    def check_data(self):
        # Checks if the data is within the boundaries defined in LogDef.
        # Raises Exception if outside the absolute range,
        # If within soft bounds, flag 'outside normal range' is false,
        # if outside bounds, flag 'outside normal range' is true
        low_low = self.lg_def.low_low
        high_high = self.lg_def.high_high
        val = self.num_value
        # NOTE: So if we set a high_high but no low_low, this will never
        # execute. Is this correct? if low_low and val <= low_low?
        if low_low and high_high:
            if(val <= low_low):
                raise Exception('low')
            elif (val >= high_high):
                raise Exception('high')

    def check_unique(self):
        # Custom method to check that the object is unique
        # (if a better or default method is found, remove this)
        # NOTE: What defines unique? I would guess
        is_unique = LogEntry.objects.filter(
            lg_set = self.lg_set,
            lg_def = self.lg_def,
            parent = self.parent,
            num_value = self.num_value,
            select_value = self.select_value,
            note = self.note,
        )
        if is_unique.exists():
            raise Exception('Already Exists')
        

    def __str__(self):
        if self.parent:
            prev_id = str(self.parent.id)
        else:
            prev_id = 'None'
        return 'LS Id: ' + str(self.lg_set.id) + ' LD Id: '\
                + str(self.lg_def.id) + ' Prev ID: ' + prev_id

class FlagTypes(models.Model):
    flag_name = models.CharField(max_length=24, null=False, blank=False)

    def __str__(self):
        return self.flag_name

class Flags(models.Model):
    log_entry = models.ForeignKey(LogEntry, on_delete=models.CASCADE, 
                    related_name='logentry')
    flag = models.ForeignKey(FlagTypes, on_delete=models.CASCADE,
                    related_name='flagtype')
    # NOTE: does flag_value have any utility? what about note?

    # Flag value is an integer corresponding to a specific boolean value
    # that is described by the note. 
    # Ex: note = '0 = on, 1 = scheduled off, 2 = unscheduled off, 3 = standby'
    # then the flag value would map to one of these. 
    flag_value = models.IntegerField(null=False, blank=False)
    note = models.CharField(max_length=50)

    def __str__(self):
        return 'Entry Id: ' + str(self.log_entry.id) + ' FlagType Id: '\
                + str(self.flag.id) + ' name: ' + str(self.flag)
