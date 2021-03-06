import linphone
import logging
import sys
from gui import Dialer
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

def main():
	logging.basicConfig(level=logging.INFO)

	app = QApplication(sys.argv)

	def log_handler(level, msg):
		method = getattr(logging, level)
		method(msg)

	def global_state_changed(*args, **kwargs):
		logging.warning("global_state_changed: %r %r" % (args,kwargs))

	def registration_state_changed(core, call, state, message):
		logging.warning("registration_state_changed: " + str(state) + ", " + message)

	def call_state_changed(core, call, state, message):
		logging.warning("call_state_changed: " + str(state) + ", " + message)
		
		if state == linphone.CallState.IncomingReceived:
			dialer.call_incoming(call)
		if state == linphone.CallState.OutgoingProgress:
			dialer.call_state = state
		if state == linphone.CallState.Connected:
			dialer.call = call
			dialer.call_state = state
		if state == linphone.CallState.End:
			dialer.num_bar.setText('')
		if state == linphone.CallState.Released:
			dialer.incoming_terminated()


	callbacks = {
		'global_state_changed': global_state_changed,
		'registration_state_changed': registration_state_changed,
		'call_state_changed': call_state_changed,
	}

	linphone.set_log_handler(log_handler)
	core = linphone.Core.new(callbacks, None, None)
	address = linphone.Address.new("sip:100@shookke.fl.3cx.us")
	auth = linphone.AuthInfo.new(None,None,None,None,None,None)
	auth.username = "100"
	auth.passwd = "g2RfaXrwNg"
	auth.userid = "zlE7Ln8bvD"
	core.add_auth_info(auth)
	proxy_cfg = core.create_proxy_config()
	core.provisioning_uri = "https://shookke.fl.3cx.us/provisioning/wuvqph5halzuac4"
	proxy_cfg.identity_address = address
	proxy_cfg.server_addr = "sip:shookke.fl.3cx.us"
	proxy_cfg.register_enabled = True
	core.add_proxy_config(proxy_cfg)
	core.terminate_all_calls()
	audio = core.sound_devices
	#core.playback_device = audio[1]
	core.mic_gain_db = 11.0
	core.ring = '/usr/local/lib/python2.7/dist-packages/linphone/share/sounds/linphone/rings/orig.wav'
	print (audio)
	iterate_timer = QTimer()
	iterate_timer.timeout.connect(core.iterate)
	#stop_timer = QTimer()
	#stop_timer.timeout.connect(app.quit)
	iterate_timer.start(20)
	#stop_timer.start(60000)
	
	dialer = Dialer(core)
	
	
	exitcode = app.exec_()
	sys.exit(exitcode)

main()

