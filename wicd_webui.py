#!/usr/bin/python

from flask import Flask, render_template,jsonify

import dbus
import dbus.service
import sys
from wicd import misc

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/list')
def list():
	results = []
	for network_id in range(wireless.GetNumberOfNetworks()):
		result = {}
		result['encryption'] = 'Off'
		if wireless.GetWirelessProperty(network_id, 'encryption'):
			result['encryption'] = wireless.GetWirelessProperty(network_id, 'encryption_method')

		result['network_id'] = network_id
		result['bssid'] = wireless.GetWirelessProperty(network_id, 'bssid')
		result['channel'] = wireless.GetWirelessProperty(network_id, 'channel')
		result['quality'] = wireless.GetWirelessProperty(network_id, 'quality')
		result['essid'] = wireless.GetWirelessProperty(network_id, 'essid')

		# check if there's key/passphrase stored (WPA1/2 and WEP only, sorry)
		result['known'] = (wireless.GetWirelessProperty(network_id, 'key') or wireless.GetWirelessProperty(network_id, 'apsk') or wireless.GetWirelessProperty(network_id, 'apsk') or False) and True
		results.append(result)

	return jsonify(data = results)

@app.route('/scan')
def scan():
	wireless.Scan(True)
	return list()

@app.route('/connect/<network_id>')
def connect(network_id):
	'''
	name = wireless.GetWirelessProperty(options.network, 'essid')
		encryption = wireless.GetWirelessProperty(options.network, 'enctype')
		print "Connecting to %s with %s on %s" % (name, encryption,
				wireless.DetectWirelessInterface())
		wireless.ConnectWireless(options.network)

		check = lambda: wireless.CheckIfWirelessConnecting()
		status = lambda: wireless.CheckWirelessConnectingStatus()
		message = lambda: wireless.CheckWirelessConnectingMessage()
	'''
	network_id = int(network_id)
	wireless.ConnectWireless(network_id)

	return (
		'connecting to %s' % wireless.GetWirelessProperty(network_id, 'essid'),
		200,
		{ 'Content-Type': 'text/plain' }
		)

@app.route('/current')
def current():
	if daemon.NeedsExternalCalls():
		iwconfig = wireless.GetIwconfig()
	else:
		iwconfig = ''

	result = {}

	network = wireless.GetCurrentNetwork(iwconfig)
	
	if network:
		result['network'] = network

		if daemon.GetSignalDisplayType() == 0:
			result['quality'] = wireless.GetCurrentSignalStrength(iwconfig)
		else:
			result['quality'] = wireless.GetCurrentDBMStrength(iwconfig)

		result['ip'] = wireless.GetWirelessIP("")

	return jsonify(data = result)

# functions
def is_valid_wireless_network_id(network_id):
	if not (network_id >= 0 \
			and network_id < wireless.GetNumberOfNetworks()):
		return False
	return True

# init

if getattr(dbus, 'version', (0, 0, 0)) < (0, 80, 0):
	import dbus.glib
else:
	from dbus.mainloop.glib import DBusGMainLoop
	DBusGMainLoop(set_as_default=True)

bus = dbus.SystemBus()
try:
	daemon = dbus.Interface(bus.get_object('org.wicd.daemon', '/org/wicd/daemon'),
			'org.wicd.daemon')
	wireless = dbus.Interface(bus.get_object('org.wicd.daemon', '/org/wicd/daemon/wireless'),
			'org.wicd.daemon.wireless')
	config = dbus.Interface(bus.get_object('org.wicd.daemon', '/org/wicd/daemon/config'),
			'org.wicd.daemon.config')
except dbus.DBusException:
	print 'Error: Could not connect to the daemon. Please make sure it is running.'
	sys.exit(3)

if not daemon:
	print 'Error connecting to wicd via D-Bus.  Please make sure the wicd service is running.'
	sys.exit(3)

if __name__ == "__main__":
	app.run(host='0.0.0.0')
