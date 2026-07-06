from enum import StrEnum


class CotType(StrEnum):
    TANK = "a-.-G-E-V-A-T"
    VEHICLE = "a-.-G-E-V"
    HELI = "a-.-A-M-H"
    PLANE = "a-.-A-M-F"
    MORTAR = "a-.-G-E-W-O"

    GROUND = "a-.-G"


class Affiliation(StrEnum):
    UNKNOWN = "u"
    FRIEND = "f"
    NEUTRAL = "n"
    HOSTILE = "h"
