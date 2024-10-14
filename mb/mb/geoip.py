import errno
import os
import sys
from subprocess import PIPE, Popen
import geoip2.database
import socket


database = '/usr/share/GeoIP/GeoLite2-City.mmdb'

def lookup_country_code(addr):
    with geoip2.database.Reader(database) as reader:
        response = reader.city(socket.gethostbyname(addr))
        return str(response.country.iso_code).lower()


def lookup_region_code(addr):
    # Beware that MirrorBrain region is indeed MaxMind continent
    with geoip2.database.Reader(database) as reader:
        response = reader.city(socket.gethostbyname(addr))
        return str(response.continent.code).lower()


def lookup_coordinates(addr):
    with geoip2.database.Reader(database) as reader:
        response = reader.city(socket.gethostbyname(addr))
        return round(float(response.location.latitude),3), round(float(response.location.longitude), 3)


if __name__ == "__main__":
    print("country:", lookup_country_code(sys.argv[1]))
    print("region:", lookup_region_code(sys.argv[1]))
