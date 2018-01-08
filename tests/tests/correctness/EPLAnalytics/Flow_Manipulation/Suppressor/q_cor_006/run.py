# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTest


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		# Start the correlator
		correlator = self.startTest()
		self.injectAnalytic(correlator)
		self.injectSuppressor(correlator)
		self.ready(correlator)
		correlator.receive(filename='Output1.evt', channels=['Output1'])

		correlator.send('Config.evt')
		self.waitForSignal('correlator.out',
						   expr='Analytic Suppressor started for inputDataNames',
						   condition='==1',
						   timeout=5)
		correlator.send('Events.evt')
		self.waitForSignal('Output1.evt', expr='com.industry.analytics\.Data', condition='==10', timeout=5)

		
	def validate(self):
		self.assertDiff('Output1.evt', 'Output1.evt')
		self.assertDiff('correlator.out', 'correlator.log',
						sort=True,
						includes=['SuppressorService'],
						ignores=self.IGNORE,
						replace=self.REPLACE)
		self.checkSanity()	