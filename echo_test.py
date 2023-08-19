import pjsua2 as pj
import time



class MyCallCallback(pj.Call):
    def __init__(self, aCall=None):
        pj.Call.__init__(self, aCall)

    # Notify application when call state has changed
    def onState(self, prm):
        print("Call state:", self.getInfo().stateText)

    # Notify application when media state in the call has changed
    def onMediaState(self, prm):
        print("Media state:", self.getInfo().mediaState)
        # Connect the call to sound device
        callInfo = self.getInfo()
        if callInfo.mediaState == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            callInfo = self.getInfo()
            self.confConnect(callInfo.confSlot, 0)
            self.confConnect(0, callInfo.confSlot)



class MyAccount(pj.Account):
    def __init__(self):
        pj.Account.__init__(self)

    # Here just to capture any incoming calls, which we will auto-answer
    def onIncomingCall(self, prm):
        print("Incoming call from", prm.srcAddress)
        call = MyCallCallback(self, prm.callId)
        call.answer(200)


def place_and_hangup_call():
    # Create an endpoint
    ep = pj.Endpoint()
    ep.libCreate()

    # Initialize endpoint
    ep_cfg = pj.EpConfig()
    ep.libInit(ep_cfg)

    # Create transport for SIP
    transport_cfg = pj.TransportConfig()
    transport_cfg.port = 5060
    ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, transport_cfg)

    # Start the library (to start receiving and processing events)
    ep.libStart()

    # Create an account configuration
    acc_cfg = pj.AccountConfig()
    acc_cfg.idUri = "sip:anonymous@139.59.179.241:5080"
    acc_cfg.regConfig.registrarUri = "sip:139.59.179.241:5080"
    # If your provider requires authentication, you'd fill these in:
    # acc_cfg.sipConfig.authCreds.push_back(pj.AuthCredInfo("digest", "*", "your_username_here", 0, "your_password_here"))

    # Create and register an account
    acc = MyAccount()
    acc.create(acc_cfg)

    call_prm = pj.CallOpParam()
    call_prm.opt.audioCount = 1
    call_prm.opt.videoCount = 0

    # Place a call
    call = MyCallCallback(acc)
    call.makeCall("sip:3456123@139.59.179.241:5080", call_prm)

    # Wait for 10 seconds
    time.sleep(30)

    # Hang up the call
    call.hangup(200, "Normal Clearing")

    # Cleanup
    acc.delete()
    ep.libDestroy()
    ep.delete()


if __name__ == "__main__":
    place_and_hangup_call()
