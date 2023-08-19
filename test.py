import pjsua2 as pj
import sys
import time
from collections import deque
import struct

write=sys.stdout.write

def ua_data_test():
    #
    # AuthCredInfo
    #
    write("UA data types test..")
    the_realm = "pjsip.org"
    ci = pj.AuthCredInfo()
    ci.realm = the_realm
    ci.dataType = 20

    ci2 = ci
    assert ci.dataType == 20
    assert ci2.realm == the_realm

    #
    # UaConfig
    # See here how we manipulate std::vector
    #
    uc = pj.UaConfig()
    uc.maxCalls = 10
    uc.userAgent = "Python"
    uc.nameserver = pj.StringVector(["10.0.0.1", "10.0.0.2"])
    uc.nameserver.append("NS1")

    uc2 = uc
    assert uc2.maxCalls == 10
    assert uc2.userAgent == "Python"
    assert len(uc2.nameserver) == 3
    assert uc2.nameserver[0] == "10.0.0.1"
    assert uc2.nameserver[1] == "10.0.0.2"
    assert uc2.nameserver[2] == "NS1"

    write("  Dumping nameservers: " + "\r\n")
    for s in uc2.nameserver:
        write(s  + "\r\n")
    write("\r\n")

#
# main()
#
if __name__ == "__main__":
    ua_data_test()