# Reads in the stops.txt and stop_times.txt and stations.csv
# Writes the edges.csv file with source_id, target_id, start_time, end_time
import csv

stops_reader = csv.reader(open('stops.txt', 'r'))
next(stops_reader) # header
stop_times_reader = csv.reader(open('stop_times.txt', 'r'))
next(stop_times_reader) # header
stations_reader = csv.reader(open('../stations.csv', 'r'))
next(stations_reader) # header

stop_names = {}
stop_ids = {}

for line in stations_reader:
    stop_ids[line[1]] = line[0]

for line in stops_reader:
    stop_id = line[0]
    stop_code = line[1]
    stop_name = line[2]
    location_type = line[6]
    longlat = (line[3], line[4])
    platform_code = line[8]
    if stop_code:
        # Main station
        assert location_type=='1'
        stop_names[stop_code] = stop_name
    else:
        # Only track
        pass

connections = []

i = 0
last_trip_id = None
last_dep_time = None
last_stop_code = None
double_time_lines = []
for line in stop_times_reader:
    trip_id = line[0]
    arrival_time = line[1]
    departure_time = line[2]
    stop_id = line[3]
    stop_code = stop_id.split('|')[0]
    arrival_stop_id = line[4]
    if arrival_stop_id:
        print(line)
    stop_sequence = line[5]
    pickup_type = line[6]
    drop_off_type = line[7]

    # if last_dep_time == arrival_time:
    #     if arrival_time == departure_time:
    #         double_time_lines.append(line)
    #     else:
    #         if len(double_time_lines) > 0:
    #             print("Double times")
    #             for dtl in double_time_lines:
    #                 print(dtl)
    #         double_time_lines = []

    if pickup_type == '0' and drop_off_type == '0':
        if last_trip_id == trip_id:
            # Next stop
            connections.append((last_stop_code, stop_code, last_dep_time, arrival_time))
        # Store for next row
        last_trip_id = trip_id
        last_dep_time = departure_time
        last_stop_code = stop_code
    else:
        # print("%d %s" % (i, line))
        last_trip_id = None
    i += 1


print("Stops found: %s" % len(stop_names))
print("Edges found: %s" % len(connections))
print("Stop ids: %s" % stop_ids)


def extract_minutesOfDay(time_str):
    time_str = time_str.split(':')
    time = int(time_str[0]) * 60 + int(time_str[1])
    return time


with open('../edges.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(['source_id', 'target_id', 'start_time', 'end_time', 'start_mod', 'end_mod'])
    for c in connections:
        start_mod = extract_minutesOfDay(c[2])
        end_mod = extract_minutesOfDay(c[3])
        spamwriter.writerow([stop_ids[c[0]], stop_ids[c[1]], c[2], c[3], start_mod, end_mod])