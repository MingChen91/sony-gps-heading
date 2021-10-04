import math
from copy import copy


class GeoPostion:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"{self.latitude, self.longitude}"


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class SimpleProjection(object):

    def __init__(self, datum: GeoPostion):
        self.datum = copy(datum)

    @classmethod
    def distance(cls, lat1, lon1, lat2, lon2):
        R = 6371
        lat_delta = lat2 - lat1
        long_delta = lon2 - lon1
        latDistance = math.radians(lat_delta)
        lonDistance = math.radians(long_delta)
        a = math.sin(latDistance / 2) * math.sin(latDistance / 2) + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * \
            math.sin(lonDistance / 2) * math.sin(lonDistance / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c * 1000
        return distance

    def __call__(self, other: GeoPostion):
        x = self.distance(self.datum.latitude, other.longitude,
                          self.datum.latitude, self.datum.longitude)
        y = self.distance(other.latitude, self.datum.longitude,
                          self.datum.latitude, self.datum.longitude)
        if other.longitude < self.datum.longitude:
            x *= -1
        if other.latitude < self.datum.latitude:
            y *= -1
        return Point(x, y)


def cartesion_mag(p):
    return math.sqrt(p.x * p.x + p.y * p.y)


def calculate_delta(p1: GeoPostion, p2: GeoPostion):
    projection = SimpleProjection(p1)
    pp = projection(p2)
    heading = math.degrees(math.atan2(pp.x, pp.y))
    return cartesion_mag(pp), heading
