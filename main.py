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
		
		if state == 1:
			dialer.call_incoming(call)
		if state == 6:
			dialer.call = call
			dialer.call_state = state
		if state == 18:
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
	#account.password = "3l4bgu0r0wmt"
	#account.username = "000"
	#account.test_validation()
	proxy_cfg = core.create_proxy_config()
	core.provisioning_uri = "https://shookke.fl.3cx.us/provisioning/wuvqph5halzuac4"
	proxy_cfg.identity_address = address
	proxy_cfg.server_addr = "sip:shookke.fl.3cx.us"
	proxy_cfg.register_enabled = True
	core.add_proxy_config(proxy_cfg)
	#core.invite("sip:000@shookke.fl.3cx.us")
	#core.invite("sip:3213013301@shookke.fl.3cx.us")
	core.terminate_all_calls()
	audio = core.sound_devices
	#core.playback_device = audio[1]
	core.mic_gain_db = 11.0
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

