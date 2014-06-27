from flask import Flask, make_response

import dbus
import dbus.service
import sys
from wicd import misc

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

app = Flask(__name__)

@app.route('/')
def list():
	result = '#\tBSSID\t\t\tChannel\tEnc\tStr\tESSID\n'

	for network_id in range(0, wireless.GetNumberOfNetworks()):

		encryption = 'Off'
		if wireless.GetWirelessProperty(network_id, 'encryption'):
			encryption = wireless.GetWirelessProperty(network_id, 'encryption_method')

		result += '%s\t%s\t%s\t%s\t%s\t%s\n' % (network_id,
			wireless.GetWirelessProperty(network_id, 'bssid'),
			wireless.GetWirelessProperty(network_id, 'channel'),
			encryption,
			wireless.GetWirelessProperty(network_id, 'quality'),
			wireless.GetWirelessProperty(network_id, 'essid'))

	return (result, 200, { 'Content-Type': 'text/plain' })

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




if __name__ == "__main__":
	app.run(host='0.0.0.0', debug = True)
