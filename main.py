from pcars2.stream import PCarsStreamReceiver
from pcars2.packet import Packet

import time
import json

class MyPCarsListener(object):
    def handlePacket(self, data: Packet):
        print(json.dumps(data.__dict__))
        # print(data['speed'])
        print(data.packetType)
        # You probably want to do something more exciting here
        # You probably also want to switch on data.packetType
        # See listings in packet.py for packet types and available fields for each
        print(data)


listener = MyPCarsListener()
stream = PCarsStreamReceiver()
stream.addListener(listener)
time.sleep(10)
stream.run()