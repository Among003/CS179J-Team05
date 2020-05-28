import os
import requests as req 
import sys
import time

from RequestTest import serverAndClientTest

def main():
	serverAndClientTest(0.12,0.80,0.10,"open_hand")
	serverAndClientTest(0.13,0.81,0.11,"open_hand")	
	serverAndClientTest(0.14,0.82,0.12,"open_hand")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
