from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from logrounds.models import RoundType, Period, LogDef, \
    LogSet, LogEntry, FlagTypes, Flags
from logrounds.forms import LogDefForm
# Create your tests here.
class LogDefFormCase(TestCase):
    def setUp(self):
        super(LogDefFormCase, self).setUp()
        self.client = Client()
        self.user = User.objects.create_user(
            'test', 'test@tester.com', 'password'
        )
        self.client.login(username='test', password='password')

        hourly = Period.objects.create(
            name='hourly',
            scale=1,
            unit='hours',
        )

        testRound = RoundType.objects.create(
            name = 'Test',
            desc = 'none',
            start_date = make_aware(datetime(month=8, day=9, year=2016)),
            period = hourly,
            phase_days=0,
            phase_hours=0,
            phase_min=0,
        )


    def test_ld_forms(self):
        round = RoundType.objects.get(name='Test')
        # Case: Quantative data, correctly filled out
        form_data = {
            'rt': round.id,
            'name' : 'Test2321',
            'desc' : 'none',
            'is_qual_data': False,
            'units' : 'gal',
            'low_low' : 0,
            'high_high' : 100,
            'low' : 40,
            'high' : 80,
        }
        form = LogDefForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Case: Quantative data, the absolute range is too small
        form_data = {
            'rt': round.id,
            'name' : 'Test2321',
            'desc' : 'none',
            'is_qual_data': False,
            'units' : 'gal',
            'low_low' : 0,
            'high_high' : 50,
            'low' : 40,
            'high' : 80,
        }
        form = LogDefForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Case: Quantative data, the absolute range is reversed
        form_data = {
            'rt': round.id,
            'name' : 'Test2321',
            'desc' : 'none',
            'is_qual_data': False,
            'units' : 'gal',
            'low_low' : 100,
            'high_high' : 0,
            'low' : 40,
            'high' : 80,
        }
        form = LogDefForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Case: Quantative data, the expected range is reversed
        form_data = {
            'rt': round.id,
            'name' : 'Test2321',
            'desc' : 'none',
            'is_qual_data': False,
            'units' : 'gal',
            'low_low' : 0,
            'high_high' : 100,
            'low' : 80,
            'high' : 40,
        }
        form = LogDefForm(data=form_data)
        self.assertFalse(form.is_valid())


        # Case: Qualatative Data, filled out extra data that should be set to 
        # none after form is cleaned
        form_data = {
            'rt': round.id,
            'name' : 'Test2321',
            'desc' : 'none',
            'is_qual_data': True,
            'units' : 'gal',
            'low_low' : 0,
            'high_high' : 100,
            'low' : 40,
            'high' : 80,
        }
        form = LogDefForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['units'] is None)
        self.assertTrue(form.cleaned_data['low_low'] is None)
        self.assertTrue(form.cleaned_data['low'] is None)
        self.assertTrue(form.cleaned_data['high_high'] is None)
        self.assertTrue(form.cleaned_data['high'] is None)



class MissingLogsetCase(TestCase):
    # Tests to see if 'update'
    def setUp(self):
        super(MissingLogsetCase, self).setUp()
        self.client = Client()
        self.user = User.objects.create_user(
            'test', 'test@tester.com', 'password'
        )
        self.client.login(username='test', password='password')

        hourly = Period.objects.create(
            name='hourly',
            scale=1,
            unit='hours',
        )

        testRound = RoundType.objects.create(
            name = 'Test',
            desc = 'none',
            start_date = make_aware(datetime(month=8, day=9, year=2016)),
            period = hourly,
            phase_days=0,
            phase_hours=0,
            phase_min=0,
        )

        testLGDF = LogDef.objects.create(
            rt=testRound,
            name='testLGDF',
            is_qual_data=True
        )

    def test_index(self):
        # test the index view, which uses the update logset
        # view function. 2 birds 1 stone
        response = self.client.get(reverse('logrounds:index'))
        self.assertEqual(response.status_code, 200)

    def test_logsets(self):
        round = RoundType.objects.get(name='Test')
        period = Period.objects.get(name='hourly')
        td = None
        phase = timedelta(
            days = round.phase_days,
            hours = round.phase_hours,
            minutes = round.phase_min
        )

        start_date = round.start_date + phase
        # Get valid timedelta
        if period.unit == 'hours':
            td = timedelta(hours = period.scale)
        elif period.unit == 'mins':
            td = timedelta(minutes = period.scale)
        elif period.unit == 'days':
            td = tiemdelta(days = period.scale)
        else:
            raise Exception("Not a valid period")

        # 'Enter' the index page which should update the Round's logsets 
            
        response = self.client.get(reverse('logrounds:index'))

        # begin at 0 iterate till now to find number of logsets
        num_logsets = 0 
        while (start_date < timezone.now()):
            start_date += td
            num_logsets += 1

        logsetQS = LogSet.objects.all()
        self.assertTrue(num_logsets > 0)
        self.assertEqual(len(logsetQS), num_logsets)

    def test_first_logset(self):
        # tests that there are no logsets before the startdate + phase
        # of the round

        round = RoundType.objects.get(name='Test')
        phase = timedelta(
            days = round.phase_days,
            hours = round.phase_hours,
            minutes = round.phase_min
        )

        # test initial, should have no LogSets
        startDate = round.start_date + phase
        first = LogSet.objects.all().order_by('start_time')
        self.assertEqual(len(first), 0)

        # test again after updating logsets
        response = self.client.get(reverse('logrounds:index'))
        self.assertEqual(response.status_code, 200)
        first = LogSet.objects.filter(rt = round).order_by('start_time')
        for lgst in first:
            self.assertTrue(startDate <= lgst.start_time)


class LogEntryCase(TestCase):
    def setUp(self):
        super(LogEntryCase, self).setUp()
        self.client = Client()
        self.user = User.objects.create_user(
            'test', 'test@tester.com', 'password'
        )

        self.client.login(username='test', password='password')

        hourly = Period.objects.create(
            name='hourly',
            scale=1,
            unit='hours',
        )

        testRound = RoundType.objects.create(
            name = 'Test',
            desc = 'none',
            start_date = make_aware(datetime(month=8, day=9, year=2016)),
            period = hourly,
            phase_days=0,
            phase_hours=0,
            phase_min=0,
        )

        testLGDF1 = LogDef.objects.create(
            rt=testRound,
            name='testLGDF1',
            is_qual_data=True
        )

        testLGDF2 = LogDef.objects.create(
            rt=testRound,
            name='testLGDF2',
            is_qual_data=False,

        )

    def test_qual_or_quant(self):
        # Tests that the save method for LogEntries correctly changes form
        # fields to NULL of they are supposed to be NULL. 
        # Eg. if 'is_qual_value' is chcecked, then the numeric value should be
        # NULL and vice-versa

        # updates all logsets
        response = self.client.get(reverse('logrounds:index'))

        round = RoundType.objects.get(name='Test')
        curr_lgst = LogSet.objects.filter(rt = round).order_by('-start_time')[0]
        qual_logdef = LogDef.objects.get(name='testLGDF1')
        quant_logdef = LogDef.objects.get(name='testLGDF2')

        le1 = LogEntry.objects.create(
            lg_set = curr_lgst,
            lg_def = qual_logdef,
            num_value = 50,
            select_value = 'Should Not Be Null'
        )
        
        self.assertTrue(le1.num_value is None)
        self.assertEqual(le1.select_value, 'Should Not Be Null')

        le2 = LogEntry.objects.create(
            lg_set = curr_lgst,
            lg_def = quant_logdef,
            num_value = 100,
            select_value = 'Should Be Null'
        )

        self.assertTrue(le2.num_value is not None)
        self.assertEqual(le2.select_value, None)