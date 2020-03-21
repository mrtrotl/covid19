from influxdb import InfluxDBClient
import COVID19Py

covid19 = COVID19Py.COVID19()

locations = (covid19.getLocations(timelines=True))

for location in locations:
    for key, value in location['timelines'].items():
        for timestamp, cases in value['timeline'].items():
            influx_payload = [
                {
                    "measurement": key,
                    "tags": {
                        "country": location['country'],
                    },
                    "time": timestamp,
                    "fields": {
                        "value": cases
                    }
                }
            ]
            if location['province']:
                influx_payload[0]['tags']['province'] = location['province']

            client = InfluxDBClient('localhost', 8086, "", "", 'covid')
            client.write_points(influx_payload)
