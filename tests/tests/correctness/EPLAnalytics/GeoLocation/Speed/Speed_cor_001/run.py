# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectSpeed(correlator)
		self.ready(correlator)

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Speed started for inputDataNames',
						   condition='==3',
						   timeout=5)

		
	def validate(self):
		self.assertGrep('correlator.out', expr='inputDataNames sequence should only have one entry')
		self.assertGrep('correlator.out', expr='outputDataNames sequence should only have one entry')
		self.assertGrep('correlator.out', expr='Param speedUnit must be either MPH or KMPH')
		
		self.assertLineCount('correlator.out', expr='Error spawning Speed instance', condition='==2')
		self.assertLineCount('correlator.out', expr='Analytic [s|S]peed started for inputDataNames', condition='==3')

		self.checkSanity()	
