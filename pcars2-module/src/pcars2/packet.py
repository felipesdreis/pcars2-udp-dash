from pcars2.enums import GameState, SessionState, RaceState, Tyres, FlagColour, FlagReason, \
    Sector, PitMode, PitSchedule
import binio


class Packet(object):

    HEADER = binio.new([
        (1,binio.types.t_uint, 'mPacketNumber'),
        (1,binio.types.t_uint, 'mCategoryPacketNumber'),
        (1,binio.types.t_u8, 'mPartialPacketIndex'),
        (1,binio.types.t_u8, 'mPartialPacketNumber'),
        (1,binio.types.t_u8, 'mPacketType'),
        (1, binio.types.t_u8, 'mPacketVersion'),
    ])

    def __init__(self, buildVersion, sequenceNumber, packetType, buf):
        self.buildVersion = buildVersion
        self.sequenceNumber = sequenceNumber
        self.packetType = packetType
        if hasattr(self.__class__, "STRUCTURE"):
            self._data = self.__class__.STRUCTURE.read_dict(buf)
        else:
            self._data = {}

    def _convertString(self, stringAsBytes):
        # Convert to utf-8 and strip junk from strings after the null character.

        try:
            # Python 2
            convertedValue = unicode(stringAsBytes, encoding='utf-8', errors='ignore')
        except NameError:
            # Python 3
            convertedValue = str(stringAsBytes, encoding='utf-8', errors='surrogateescape')

        return convertedValue.rstrip('\x00')

    @staticmethod
    def readFrom(buf):
        header = Packet.HEADER.read_dict(buf)
        buildVersion = header["mPacketNumber"]
        sequenceNumber = header["mCategoryPacketNumber"]
        packetType = header["mPacketType"]
        pClass = PACKET_TYPES.get(packetType, Packet)
        return pClass(buildVersion, sequenceNumber, packetType, buf)


class TelemetryPacket(Packet):

    STRUCTURE = binio.new([
        (1, binio.types.t_int8, "viewedParticipantIndex"),
        # Unfiltered input
        (1, binio.types.t_u8, "unfilteredThrottle"),
        (1, binio.types.t_u8, "unfilteredBrake"),
        (1, binio.types.t_int8, "unfilteredSteering"),
        (1, binio.types.t_u8, "unfilteredClutch"),
        # Flags
        (1, binio.types.t_u8, "raceStateFlags"),
        # Data
        (1, binio.types.t_int16, "oilTempCelsius"),
        (1, binio.types.t_u16, "oilPressureKPa"),
        (1, binio.types.t_int16, "waterTempCelsius"),
        (1, binio.types.t_u16, "waterPressureKPa"),
        (1, binio.types.t_u16, "fuelPressureKPa"),
        (1, binio.types.t_u8, "fuelCapacity"),
        (1, binio.types.t_u8, "brake"),
        (1, binio.types.t_u8, "throttle"),
        (1, binio.types.t_u8, "clutch"),
        (1, binio.types.t_float, "fuelLevel"),
        (1, binio.types.t_float, "speed"),
        (1, binio.types.t_u16, "rpm"),
        (1, binio.types.t_u16, "maxRpm"),
        (1, binio.types.t_int8, "steering"),
        (1, binio.types.t_u8, "gearNumGears"),
        (1, binio.types.t_u8, "boostAmount"),
        (1, binio.types.t_u8, "crashState"),
        # Motion and device
        (1, binio.types.t_float32, "odometerKM"),
        (1, binio.types.t_float32, "orientationX"),
        (1, binio.types.t_float32, "orientationY"),
        (1, binio.types.t_float32, "orientationZ"),
        (1, binio.types.t_float32, "localVelocityX"),
        (1, binio.types.t_float32, "localVelocityY"),
        (1, binio.types.t_float32, "localVelocityZ"),
        (1, binio.types.t_float32, "worldVelocityX"),
        (1, binio.types.t_float32, "worldVelocityY"),
        (1, binio.types.t_float32, "worldVelocityZ"),
        (1, binio.types.t_float32, "angularVelocityX"),
        (1, binio.types.t_float32, "angularVelocityY"),
        (1, binio.types.t_float32, "angularVelocityZ"),
        (1, binio.types.t_float32, "localAccelerationX"),
        (1, binio.types.t_float32, "localAccelerationY"),
        (1, binio.types.t_float32, "localAccelerationZ"),
        (1, binio.types.t_float32, "worldAccelerationX"),
        (1, binio.types.t_float32, "worldAccelerationY"),
        (1, binio.types.t_float32, "worldAccelerationZ"),
        (1, binio.types.t_float32, "extentsCentreX"),
        (1, binio.types.t_float32, "extentsCentreY"),
        (1, binio.types.t_float32, "extentsCentreZ"),
    ])

    TYRES_STRUCTURE = [  # This is a list of binio typedefs - each is repeated for each wheel before the next typedef.
        (1, binio.types.t_u8, "tyreFlags"),
        (1, binio.types.t_u8, "terrain"),
        (1, binio.types.t_float32, "tyreY"),
        (1, binio.types.t_float32, "tyreRPS"),
        (1, binio.types.t_u8, "tyreTemp"),
        (1, binio.types.t_float32, "tyreHeightAboveGround"),
        (1, binio.types.t_u8, "tyreWear"),
        (1, binio.types.t_u8, "brakeDamage"),
        (1, binio.types.t_u8, "suspensionDamage"),
        (1, binio.types.t_int16, "brakeTempCelsius"),
        (1, binio.types.t_u16, "tyreTreadTemp"),
        (1, binio.types.t_u16, "tyreLayerTemp"),
        (1, binio.types.t_u16, "tyreCarcassTemp"),
        (1, binio.types.t_u16, "tyreRimTemp"),
        (1, binio.types.t_u16, "tyreInternalAirTemp"),
        (1, binio.types.t_u16, "tyreTempLeft"),
        (1, binio.types.t_u16, "tyreTempCenter"),
        (1, binio.types.t_u16, "tyreTempRight"),
        (1, binio.types.t_float32, "wheelLocalPositionY"),
        (1, binio.types.t_float32, "rideHeight"),
        (1, binio.types.t_float32, "suspensionTravel"),
        (1, binio.types.t_float32, "suspensionVelocity"),
        (1, binio.types.t_u16, "suspensionRideHeight"),
        (1, binio.types.t_u16, "airPressure"),
    ]

    STRUCTURE_2 = binio.new([
        (1, binio.types.t_float32, "engineSpeed"),
        (1, binio.types.t_float32, "engineTorque"),
        (1, binio.types.t_u8, "wings1"),
        (1, binio.types.t_u8, "wings2"),
        (1, binio.types.t_u8, "handBrake"),
        (1, binio.types.t_u8, "aeroDamage"),
        (1, binio.types.t_u8, "engineDamage"),
        (1, binio.types.t_uint, "joyPad"),
        (1, binio.types.t_u8, "dPad"),
    ])

    TYRES_STRUCTURE_2 = binio.new([
        (40, binio.types.t_char, "tyreCompound"),
    ])

    def __init__(self, buildVersion, sequenceNumber, packetType, buf):
        super(TelemetryPacket, self).__init__(buildVersion, sequenceNumber, packetType, buf)  # everything up to tyre information
        self._data["tyres"] = [{}, {}, {}, {}]

        for datapoint in TelemetryPacket.TYRES_STRUCTURE:
            self._forEachTyre(datapoint, buf)
        #
        self._data.update(TelemetryPacket.STRUCTURE_2.read_dict(buf))

        # self._forEachTyre(TelemetryPacket.TYRES_STRUCTURE_2, buf)
        # for i in Tyres:
        #     self._data["tyres"][i.value][TelemetryPacket.TYRES_STRUCTURE_2[2]] = thisField.read_dict(buf)[datapoint[2]]

    def _forEachTyre(self, datapoint, buf):
        thisField = binio.new([datapoint])
        for i in Tyres:
            self._data["tyres"][i.value][datapoint[2]] = thisField.read_dict(buf)[datapoint[2]]

    def __getitem__(self, key):
        return self._data[key]


class RaceData(Packet):

    STRUCTURE = binio.new([
        (1,binio.types.t_float32,"sWorldFastestLapTime"),
        (1,binio.types.t_float32,"sPersonalFastestLapTime"),
        (1,binio.types.t_float32,"sPersonalFastestSector1Time"),
        (1,binio.types.t_float32,"sPersonalFastestSector2Time"),
        (1,binio.types.t_float32,"sPersonalFastestSector3Time"),
        (1,binio.types.t_float32,"sWorldFastestSector1Time"),
        (1,binio.types.t_float32,"sWorldFastestSector2Time"),
        (1,binio.types.t_float32,"sWorldFastestSector3Time"),
        (1,binio.types.t_float32,"sTrackLength"),
        (64,binio.types.t_char,"sTrackLocation"),
        (64,binio.types.t_char,"sTrackVariation"),
        (64,binio.types.t_char,"sTranslatedTrackLocation"),
        (64,binio.types.t_char,"sTranslatedTrackVariation"),
        (1,binio.types.t_u8,"sLapsTimeInEvent"),
        (1,binio.types.t_int8,"sEnforcedPitStopLap")
    ])

    def __getitem__(self, key):
        return self._data[key]


class ParticipantsData(Packet):

    STRUCTURE = binio.new([
        (1, binio.types.t_uint, "ParticipantsChangedTimestamp")
    ])

    NAME_STRUCTURE = binio.new([(64, binio.types.t_char, "name")])

    def __init__(self, buildVersion, sequenceNumber, packetType, buf):
        super(ParticipantsData, self).__init__(buildVersion, sequenceNumber, packetType, buf)
        self._data["participants"] = []

        for _ in range(0, 16):
            p = ParticipantsData.NAME_STRUCTURE.read_dict(buf)
            p["name"] = self._convertString(p["name"])
            self._data["participants"].append(p)

    def __getitem__(self, key):
        return self._data[key]

class TimingsData(Packet):

    STRUCTURE = binio.new([
        (1, binio.types.t_u8, "NumParticipants"),
        (1, binio.types.t_uint, "ParticipantsChangedTimestamp"),
        (1, binio.types.t_float32, "sEventTimeRemaining"),
        (1, binio.types.t_float32, "sSplitTimeAhead"),
        (1, binio.types.t_float32, "sSplitTimeBehind"),
        (1, binio.types.t_float32, "sSplitTime")
    ])

    PARTICIPANT_INFO_STRUCTURE = binio.new([
        (1, binio.types.t_int16, "worldPositionX"),
        (1, binio.types.t_int16, "worldPositionY"),
        (1, binio.types.t_int16, "worldPositionZ"),
        (1, binio.types.t_int16, "orientationX"),
        (1, binio.types.t_int16, "orientationY"),
        (1, binio.types.t_int16, "orientationZ"),
        (1, binio.types.t_u16, "currentLapDistance"),
        (1, binio.types.t_u8, "racePosition"),
        (1, binio.types.t_u8, "sector"),
        (1, binio.types.t_u8, "HighestFlag"),
        (1, binio.types.t_u8, "PitModeSchedule"),
        (1, binio.types.t_u8, "CarIndex"),
        (1, binio.types.t_u8, "RaceState"),
        (1, binio.types.t_u8, "currentLap"),
        (1, binio.types.t_u8, "lapsCompleted"),
        (1, binio.types.t_float32, "CurrentSectorTime"),
    ])


    def __init__(self, buildVersion, sequenceNumber, packetType, buf):
        super(TimingsData, self).__init__(buildVersion, sequenceNumber, packetType, buf)
        self._data["participant_timings"] = []

        for _ in range(0, 32):
            p = TimingsData.PARTICIPANT_INFO_STRUCTURE.read_dict(buf)
            self._data["participant_timings"].append(p)

    def __getitem__(self, key):
        return self._data[key]


class GameStateData(Packet):

    STRUCTURE = binio.new([
        (1, binio.types.t_u16, "BuildVersionNumber"),
        (1, binio.types.t_char, "GameState"),
        (1, binio.types.t_int8, "ambientTemperature"),
        (1, binio.types.t_int8, "trackTemperature"),
        (1, binio.types.t_u8, "rainDensity"),
        (1, binio.types.t_u8, "snowDensity"),
        (1, binio.types.t_int8, "windSpeed"),
        (1, binio.types.t_int8, "windDirectionX"),
        (1, binio.types.t_int8, "windDirectionY"),
    ])

    def __getitem__(self, key):
        return self._data[key]

class TimeStatsData(Packet):

    STRUCTURE = binio.new([
        (1, binio.types.t_uint, "ParticipantsChangedTimestamp")
    ])

    PARTICIPANTS_STATS_INFO = binio.new([
        (1, binio.types.t_float, "sFastestLapTime"),
        (1, binio.types.t_float32, "sLastLapTime"),
        (1, binio.types.t_float32, "sLastSectorTime"),
        (1, binio.types.t_float32, "sFastestSector1Time"),
        (1, binio.types.t_float32, "sFastestSector2Time"),
        (1, binio.types.t_float32, "sFastestSector3Time")
    ])

    def __init__(self, buildVersion, sequenceNumber, packetType, buf):
        super(TimeStatsData, self).__init__(buildVersion, sequenceNumber, packetType, buf)
        self._data["participants_time_stats"] = []

        for _ in range(0, 32):
            p = TimeStatsData.PARTICIPANTS_STATS_INFO.read_dict(buf)
            self._data["participants_time_stats"].append(p)

    def __getitem__(self, key):
        return self._data[key]


class ParticipantsVehicleNamesData(Packet):

    VEHICLE_INFO = binio.new([
        (1, binio.types.t_u16, "Index"),
        (1, binio.types.t_uint, "Class"),
        (64, binio.types.t_char, "Name")
    ])

    def __init__(self, buildVersion, sequenceNumber, packetType, buf):
        super(ParticipantsVehicleNamesData, self).__init__(buildVersion, sequenceNumber, packetType, buf)
        self._data["vehicles"] = []

        for _ in range(0, 16):
            p = ParticipantsVehicleNamesData.VEHICLE_INFO.read_dict(buf)
            self._data["vehicles"].append(p)


class VehicleClassNamesData(Packet):

    VEHICLE_CLASS_INFO = binio.new([
        (1, binio.types.t_uint, "Index"),
        (20, binio.types.t_char, "Name")
    ])

    def __init__(self, buildVersion, sequenceNumber, packetType, buf):
        super(VehicleClassNamesData, self).__init__(buildVersion, sequenceNumber, packetType, buf)
        self._data["vehicle_classes"] = []

        for _ in range(0, 60):
            p = VehicleClassNamesData.VEHICLE_CLASS_INFO.read_dict(buf)
            self._data["vehicle_classes"].append(p)
"""
NOTE: If there are less than 16 participants in a race the name and
      fastestLapTime fields may contain old data from a previouse
      race.

      Use numParticipants from TelemetryPacket to work out how many
      participants there are.

"""


PACKET_TYPES = {
    0: TelemetryPacket,
    1: RaceData,
    # 2: ParticipantsData,
    3: TimeStatsData,
    4: GameStateData,
    7: TimingsData,
    # 8: VehicleClassNamesData
}

