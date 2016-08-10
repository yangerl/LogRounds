from django.test import TestCase
from datetime import datetime, timedelta

# Create your tests here.
class MissingLogsetCase(TestCase):
	# Tests to see if 'update'
	def setUp(self):
		super(MissingLogsetCase, self).setUp()
		RoundType.objects.all().delete()
		LogSet.objects.all().delete()
		LogDef.objects.all().delete()
		LogEntry.objects.all().delete()
		Period.objects.all().delete()

		hourly = Period.objects.create(
			name='hourly',
			scale=1,
			unit='hours',
			phase_days=0,
			phase_hours=0,
			phase_min=0,
		)

		testRound = RoundType.objects.create(
			rt_name = 'Test',
			rt_desc = 'none',
			start_date = datetime(month=8, day=9, year=2016),
			period = hourly
		)

		testLGDF = LogDef.objects.create(
			rt=testRound,
			name='testLGDF',
			is_qual_data=True
		)

	def test_index(self):
		# test the index view, which uses the update logset
		# view function. 2 birds 1 stone
		 request = 'fake request'
		 response = index(request)
		 self.assertEqual(response.status_code, 200)

	def test_logsets(self):
		round = RoundType.objects.get(rt_name='Test')
		period = Period.objects.get(name='hourly')
		td = None
		phase = timedelta(
			days = period.phase_days,
			hours = period.phase_hours,
			minutes = period.phase_min
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

		# begin at 0 iterate till now
		num_logsets = 0	

		while (start_date < timezone.now()):
			start_date += td
			num_logsets += 1

		logsetQS = LogSet.objects.all()
		assertEqual()(logsetQS.len(), num_logsets)









