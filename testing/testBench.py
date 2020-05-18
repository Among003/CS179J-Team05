import sys
import os

sys.path.insert(0, os.path.abspath("../object detection/"))
sys.path.insert(0, os.path.abspath("../object detection/testing"))
sys.path.insert(0, os.path.abspath("../ClientAndServerTesting"))


from test import TestVideoHarness 
import RequestTest


TestVideoHarness()
serverAndClientTest(4.0, 4.6, 1.4, "open")
