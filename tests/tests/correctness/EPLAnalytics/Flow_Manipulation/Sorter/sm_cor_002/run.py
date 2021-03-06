# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTest
from pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest(Xclock=True)
		self.injectAnalytic(correlator)
		self.injectSorter(correlator)
		self.ready(correlator)
		correlator.receive('All.evt')
		correlator.receive('Output1.evt', channels=['Output1'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out', expr='Analytic Sorter started for inputDataNames', condition='==1', timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('All.evt',
						   expr='com\.industry\.analytics\.Data\("Output1","a","s1",0,1\.3,"",1,2,3,\{"anomalySource":"Sorter"\}\)',
						   condition='==1',
						   timeout=5)
		
	def validate(self):
		self.assertDiff('correlator.out', 'correlator.log',
						sort=True,
						includes=['SorterService'],
						ignores=self.IGNORE,
						replace=self.REPLACE)
		self.assertDiff('Output1.evt', 'Output1.evt')
		self.assertDiff('All.evt', 'All.evt')
		self.checkSanity()	
