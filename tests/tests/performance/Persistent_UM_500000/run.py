# $Copyright (c) 2015 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or Terracotta Inc., San Francisco, CA, USA, and/or Software AG (Canada) Inc., Cambridge, Ontario, Canada, and/or, Software AG (UK) Ltd., Derby, United Kingdom, and/or Software A.G. (Israel) Ltd., Or-Yehuda, Israel and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG

from industry.framework.AnalyticsBaseTest import AnalyticsBaseTestfrom pysys.constants import *


class PySysTest(AnalyticsBaseTest):
	def execute(self):
		simulatorPersistenceDir = os.path.join(self.output, 'simulatorPersistence')
		AnalyticPersistenceDir = os.path.join(self.output, 'AnalyticPersistence')
		os.mkdir(simulatorPersistenceDir)
		os.mkdir(AnalyticPersistenceDir)
						
		# Start the correlator
		simulatorCorrelator = self.startTest(logfile='simulatorCorrelator.log', enableJMS=True,
											 persistence=True, persistenceStoreLocation=simulatorPersistenceDir,
											 jmsConfigPath=os.path.join(self.TEST_JMS_SETTINGS, 'SimulatorCorrelatorAtLeastOnceJMS') )
		# Start the correlator
		AnalyticCorrelator = self.startTest(logfile='AnalyticCorrelator.log', enableJMS=True,
											 persistence=True, persistenceStoreLocation=AnalyticPersistenceDir,
											 jmsConfigPath=os.path.join(self.TEST_JMS_SETTINGS, 'AnalyticCorrelatorAtLeastOnceJMS') )
		 
		self.injectAnalytic(AnalyticCorrelator)
		self.injectDataSourceService(AnalyticCorrelator)
		self.injectAverage(AnalyticCorrelator)
		self.injectThreshold(AnalyticCorrelator)
		self.injectEventRate(AnalyticCorrelator)
		self.injectReflector(AnalyticCorrelator)
		
		self.injectDataSimulator(simulatorCorrelator)
		
		AnalyticCorrelator.sendLiteral('com.industry.analytics.EnableDataReflector()')
		AnalyticCorrelator.receive(filename='EventRate.evt', channels=['EventRate'])

		self.waitForSignal('simulatorCorrelator.log',
						   expr='DataSourceService cache ready',
						   condition='==1',
						   timeout=5)
		simulatorCorrelator.send('Assets.evt')
		self.waitForSignal('AnalyticCorrelator.log',
						   expr='DataSourceService cache ready',
						   condition='==1',
						   timeout=5)
		AnalyticCorrelator.send('Assets.evt')
		
		AnalyticCorrelator.send('Config.evt')
		self.waitForSignal('AnalyticCorrelator.log',
						   expr='Analytic Average started for inputDataNames',
						   condition='==1',
						   timeout=5)
		self.waitForSignal('AnalyticCorrelator.log',
						   expr='Analytic Threshold started for inputDataNames',
						   condition='==1',
						   timeout=5)
		self.waitForSignal('AnalyticCorrelator.log',
						   expr='Analytic EventRate started for inputDataNames',
						   condition='==1',
						   timeout=5)
		
		simulatorCorrelator.send('StartSimulator.evt')
		self.waitForSignal('EventRate.evt', expr='com.industry.analytics\.Data', condition='==10', timeout=20)
		
		simulatorCorrelator.stop()
		self.waitForSignal('EventRate.evt', expr='com.industry.analytics\.Data\("EventRate","c","A",\d*(\.\d*)?,0,"",\{\}\)', condition='>=2', timeout=600)

		
	def validate(self):
		self.checkSanity(correlatorLog='simulatorCorrelator.log')
		self.checkSanity(correlatorLog='AnalyticCorrelator.log')
		self.addOutcome(INSPECT)
