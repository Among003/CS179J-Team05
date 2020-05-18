import sys, os

cwd = os.getcwd()

os.chdir('..')
os.chdir('ClientAndServerTesting')
from RequestTest import serverAndClientTest
os.chdir(r'../object detection')
from test import TestVideoOnObjectDetectionHarness

os.chdir(cwd)

def main():
    
    report = {}
    
    report['TestVideoOnObjectDetectionHarness'] = TestVideoOnObjectDetectionHarness()
    report['serverAndClientTest'] = serverAndClientTest(4.0, 4.6, 1.4, "open")
    
    
if __name__ == '__main__':
    main()
