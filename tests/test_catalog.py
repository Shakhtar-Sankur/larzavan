from larzavan.catalog import parse_feature


def test_parse_usgs_feature():
    feature = {
        "id": "us6000qw60",
        "geometry": {"coordinates": [160.4, 52.5, 20.7]},
        "properties": {
            "time": 1753826092000,
            "mag": 8.8,
            "magType": "mww",
            "place": "2025 Kamchatka Peninsula, Russia Earthquake",
        },
    }
    e = parse_feature(feature)
    assert (e.id, e.magnitude, e.magnitude_type, e.depth_km) == ("us6000qw60", 8.8, "mww", 20.7)
    assert e.time.year == 2025 and e.latitude == 52.5 and e.longitude == 160.4
