import sys
sys.path.append("..")
import utils.filtersbar as u
import unittest
import os
try:
    import datetime
    from datetime import timedelta, datetime
except ModuleNotFoundError:
    os.system('pip install datetime')


class TestUtils(unittest.TestCase):
	def test_initializeDates(self):
		dtformat = '%Y-%m-%dT%H:%M:%SZ'
		time = datetime.utcnow()
		start_time = time - timedelta(days=7)
		end_time = time - timedelta(seconds=15)
		start_time, end_time = start_time.strftime(dtformat), end_time.strftime(dtformat)
		start_time, end_time = start_time[0:len(start_time)-4], end_time[0:len(end_time)-4]
		
		result = {"minDate":start_time, "minDateValue": start_time, "maxDate": end_time, "maxDateValue": end_time}

		self.assertEqual(u.initializeDates('HTMLFormat'), result)

	def test_initializeResearchMethods(self):
		researchMethods = [
			{'method':"", 'text':'Research by '},
			{'method':'researchByUser', 'text':'Research by user'},
			{'method':'researchByKeyword','text':'Research by keyword'},
			{'method':'researchByHashtag','text':'Research by hashtag'}
		]
		self.assertEqual(u.initializeResearchMethods(), researchMethods)


if __name__ == '__main__':
    unittest.main()