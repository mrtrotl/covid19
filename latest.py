from influxdb import InfluxDBClient
import COVID19Py

covid19 = COVID19Py.COVID19()

locations = covid19.getLocations()

for location in locations:
    for status, cases in location['latest'].items():
        influx_payload = [
            {
                "measurement": status,
                "tags": {
                    "country": location['country'],
                },
                "time": location["last_updated"],
                "fields": {
                    "value": cases
                }
            }
        ]
        if location['province']:
            influx_payload[0]['tags']['province'] = location['province']

        client = InfluxDBClient('localhost', 8086, "", "", 'covid')
        client.write_points(influx_payload)
