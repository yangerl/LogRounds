from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from logrounds.models import RoundType, Period, LogDef, LogSet, LogEntry, FlagTypes, Flags
# Create your tests here.
class MissingLogsetCase(TestCase):
    # Tests to see if 'update'
    def setUp(self):
        super(MissingLogsetCase, self).setUp()
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@tester.com', 'password')
        self.client.login(username='test', password='password')

        hourly = Period.objects.create(
            name='hourly',
            scale=1,
            unit='hours',
        )

        testRound = RoundType.objects.create(
            rt_name = 'Test',
            rt_desc = 'none',
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
        round = RoundType.objects.get(rt_name='Test')
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

        round = RoundType.objects.get(rt_name='Test')
        phase = timedelta(
            days = round.phase_days,
            hours = round.phase_hours,
            minutes = round.phase_min
        )

        # test initial, should have no LogSets
        startDate = round.start_date + phase
        first = LogSet.objects.all().order_by('start_time')
        self.assertEquals(len(first), 0)

        # test again after updating logsets
        response = self.client.get(reverse('logrounds:index'))
        self.assertEqual(response.status_code, 200)
        first = LogSet.objects.all().order_by('start_time')
        for lgst in first:
            self.assertTrue(startDate <= lgst.start_time)


class LogEntryCase(TestCase):
    def setUp(self):
        super(MissingLogsetCase, self).setUp()
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@tester.com', 'password')
        self.client.login(username='test', password='password')

        hourly = Period.objects.create(
            name='hourly',
            scale=1,
            unit='hours',
        )

        testRound = RoundType.objects.create(
            rt_name = 'Test',
            rt_desc = 'none',
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
    








