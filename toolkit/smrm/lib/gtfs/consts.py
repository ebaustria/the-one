# -*- coding: utf-8 -*-

# map gtfs files to dataframes
GTFS_FILES = [
    ('services', 'calendar.txt'),  # service days by service id
    ('exceptions', 'calendar_dates.txt'),  # exceptions from regular service days
    ('stop_times', 'stop_times.txt'),  # stop times at each stop for each trip
    ('trips', 'trips.txt'),  # trips by route id
    ('stops', 'stops.txt'),  # stop names and ids
    ('routes', 'routes.txt')  # routes for each service id
]

# services headers
SERVICE_ID = 'service_id'
MON = 'monday'
TUE = 'tuesday'
WED = 'wednesday'
THU = 'thursday'
FRI = 'friday'
SAT = 'saturday'
SUN = 'sunday'

# exceptions headers
DATE = 'date'
TYPE = 'exception_type'

# trips headers
TRIP_ID = 'trip_id'
DIRECTION_ID = 'direction_id'

# routes headers
ROUTE_ID = 'route_id'
ROUTE_NAME = 'route_short_name'

# stops headers
STOP_ID = 'stop_id'
STOP_NAME = 'stop_name'

# stop_times headers
ARR_TIME = 'arrival_time'
STOP_SEQ = 'stop_sequence'

# derived headers
STOPS = 'stops'
STOPS_SIZE = STOPS + '_size'
STOPS_SIZE_X = STOPS_SIZE+'_x'
STOPS_SIZE_Y = STOPS_SIZE+'_y'
STOP_NAME_FIRST = STOP_NAME + '_first'
STOP_NAME_LAST = STOP_NAME + '_last'
REF_NAME_FIRST = 'ref_name_first'
REF_NAME_LAST = 'ref_name_last'
ARR_TIME_FIRST = ARR_TIME + '_first'
DIRECTION_ID_X = DIRECTION_ID + '_x'
DIRECTION_ID_Y = DIRECTION_ID + '_y'
SCORE = 'score'
MINS = 'mins'
MINS_PREV = 'mins_prev'
DURATION_TO = 'duration_to'

# options for pandas csv reader
# giving explicit dtypes to columns speeds up
# the parsing for big tables
PD_CSV_OPTIONS = {
    'dtype': {
        STOP_ID: object,
        TRIP_ID: object
    },
    'low_memory': False
}