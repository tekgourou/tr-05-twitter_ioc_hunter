def create_sighting(data_json, o_value, o_type):
    sighting = {
        "schema_version": "1.0.11",
        "observables": [
            {"value": o_value, "type": o_type}
        ],
        "type": "sighting",
        "id": data_json['tweet']['id'],
        "title": "Twitter IOC Hunter",
        "count": 1,
        "targets": [],
        "relations": [],
        "tlp": "white",
        "source": "Twitter IOC Hunter",
        "description": "",
        "timestamp": data_json['tweet']['timestamp'],
        "confidence": "Medium",
        "observed_time": {"start_time": data_json['tweet']['timestamp'],
                          "end_time": data_json['tweet']['timestamp']
                          },
        "data": {
            "columns": [
                {
                    "name": "Twitter User",
                    "type": "string"
                },
                {
                    "name": "Tweet",
                    "type": "string"
                },
                {
                    "name": "Hashtags",
                    "type": "string"
                },
                {
                    "name": "Link",
                    "type": "string"
                }
                ],
            "rows": [
                [
                    data_json['tweet']['user'],
                    data_json['tweet']['tweet'],
                    data_json['tweet']['hashtags'],
                    data_json['tweet']['link'],
                ]
            ],
            "row_count": 1
        }
    }

    return sighting