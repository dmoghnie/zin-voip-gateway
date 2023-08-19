import pjsua2 as pj

class MyCallCallback(pj.Call):
    def __init__(self, acc, call=None):
        pj.Call.__init__(self, acc, call)

    def onState(self, prm):
        global secondary_call
        # If the primary call (incoming) is answered, we initiate a secondary call.
        if self.getInfo().state == pj.PJSIP_INV_STATE_CONNECTING and not secondary_call:
            secondary_call = MyCallCallback(acc)
            call_prm = pj.CallOpParam(True)
            secondary_call.makeCall("sip:destination_number@sip_proxy", call_prm)

    def onMediaState(self, prm):
        # When both calls are active, bridge their media
        if self.getInfo().mediaState == pj.PJSUA_CALL_MEDIA_ACTIVE and secondary_call.getInfo().mediaState == pj.PJSUA_CALL_MEDIA_ACTIVE:
            pj.Endpoint.instance().mediaActive(self.getInfo().confSlot, secondary_call.getInfo().confSlot)

class MyAccount(pj.Account):
    def onIncomingCall(self, prm):
        call = MyCallCallback(self, prm.callId)
        call_op_param = pj.CallOpParam()
        call_op_param.statusCode = pj.PJSIP_SC_OK
        call.answer(call_op_param)

ep = pj.Endpoint()
ep.libCreate()

# Initialize endpoint
ep_cfg = pj.EpConfig()
ep.libInit(ep_cfg)

# Create transport for SIP
transport_cfg = pj.TransportConfig()
transport_cfg.port = 5060
ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, transport_cfg)
ep.libStart()

# Account configuration
acc_cfg = pj.AccountConfig()
acc_cfg.idUri = "sip:your_user@sip_proxy"
acc_cfg.regConfig.registrarUri = "sip:sip_proxy"
# Add your SIP proxy authentication credentials if needed
acc_cfg.sipConfig.authCreds.append(pj.AuthCredInfo("digest", "*", "your_user", 0, "your_password"))

# Register account
acc = MyAccount()
acc.create(acc_cfg)

# Placeholder for the secondary call
secondary_call = None

try:
    # Wait for events
    input("Press Enter to exit...\n")
except KeyboardInterrupt:
    pass

# Cleanup
acc.delete()
ep.libDestroy()
ep.delete()
