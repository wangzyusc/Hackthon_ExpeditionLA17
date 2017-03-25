import json, math, sys

def load_json_file(filename):
    plain_text = open(filename).read()

    # Make the plain text can be recognized by the json module.
    plain_text = plain_text.replace(',}', '}')
    plain_text = plain_text.replace(',]', ']')
    plain_text = plain_text.replace('}]}]}', '}]}')
    plain_text = " ".join(plain_text.split("\n"))
    plain_text = plain_text.replace("\\", "")

    data = json.loads(plain_text)
    return data

def get_roads(geojson_obj):
    road_list = dict()
    vertex_set = set()
    for feature in geojson_obj['features']:
        if 'properties' in feature and 'LENGTH' in feature['properties']:
            LENGTH = feature['properties']['LENGTH']

        if 'geometry' in feature and 'coordinates' in feature['geometry']:
            first = feature['geometry']['coordinates'][0]
            second = feature['geometry']['coordinates'][-1]
            if (first[0], first[1]) not in vertex_set:
                vertex_set.add((first[0], first[1]))
            if (second[0], second[1]) not in vertex_set:
                vertex_set.add((second[0], second[1]))
            road_list[((first[0], first[1]), (second[0], second[1]))] = LENGTH
            road_list[((second[0], second[1]), (first[0], first[1]))] = LENGTH

    return road_list, vertex_set

def degree_to_km(degree):
    radius = 6378.1
    north = 35
    south = 28
    ratio = math.cos(north / 180 * math.pi) + math.cos(south / 180 * math.pi)
    return degree / 180 * math.pi * ratio * radius

if __name__ == '__main__':
    json_data = load_json_file('RoadNetwork.geojson')
    roads, vertices = get_roads(json_data)
    print '----------------------\nvertices\n----------------------'
    for key in vertices:
        print key
    print '----------------------\nvertices\n----------------------'
    for key, value in roads.iteritems():
        print str(key) + " -> " + str(degree_to_km(value))
    print 'reading finish'