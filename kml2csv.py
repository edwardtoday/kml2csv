from __future__ import print_function
from zipfile import ZipFile
import sys
import os

import fastkml
from pygeoif import geometry


def parse_all_features(feature_list, output):
    for feature in feature_list:
        if type(feature) is fastkml.kml.Placemark:
            if type(feature.geometry) is geometry.Point:
                print("{},{},{}".format(feature.name, feature.geometry.x, feature.geometry.y), file=output)
        elif type(feature) is fastkml.kml.Folder or type(feature) is fastkml.kml.Document:
            parse_all_features(list(feature.features()), output)


if __name__ == "__main__":
    output_name = "output.csv"
    try:
        os.remove(output_name)
    except OSError:
        pass
    if sys.argv[1]:
        filename = sys.argv[1]
        kmz = ZipFile(filename, 'r')
        kml = kmz.open('doc.kml', 'r')
        k = fastkml.kml.KML()
        k.from_string(kml.read())
        try:
            output_file = open(output_name, 'w')
            parse_all_features(list(k.features()), output_file)
            output_file.close()
        except OSError:
            exit(1)
    else:
        exit(1)
