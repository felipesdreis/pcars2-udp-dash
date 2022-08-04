from pcars2.packet import Packet, TelemetryPacket
from io import BytesIO
import unittest
import os

_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class TestPacket(unittest.TestCase):

    def TestPacketType0(self):
        with open(os.path.join(_location, "packetbin_type_0.bin"), "rb") as f:
            p = Packet.readFrom(f)
        self.assertEqual(0, p.packetType)
        self.assertEqual(0.11948990821838379, p["extentsCentreZ"])

    def testPacketType3(self):
        with open(os.path.join(_location, "packetbin_type_3.bin"), "rb") as f:
            p = Packet.readFrom(f)
        self.assertEqual(3, p.packetType)
        self.assertEqual(p['ParticipantsChangedTimestamp'], 373537025)
        self.assertEqual(6.64613997892458e+35, p["participants_time_stats"][0]['sFastestLapTime'])

    def testPacketType4(self):
        with open(os.path.join(_location, "packetbin_type_4.bin"), "rb") as f:
            p = Packet.readFrom(f)
        self.assertEqual(4, p.packetType)
        self.assertEqual(-72, p["windDirectionY"])

    def testPacketType7(self):
        with open(os.path.join(_location, "packetbin_type_7.bin"), "rb") as f:
            p = Packet.readFrom(f)
        self.assertEqual(7, p.packetType)
        self.assertEqual(6.058903471481429e-39, p["sSplitTimeBehind"])

if __name__ == '__main__':
    unittest.main()
