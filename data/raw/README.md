# Raw GTFS Data

This directory contains raw GTFS data used by the Transit Analytics API.

## Source

GTFS data was obtained from Mobility Database:

https://database.mobilitydata.org/

## Important

Raw GTFS files should not be manually modified.

The ETL pipeline will eventually read these files, validate them, transform them, and load the resulting data into PostgreSQL.

## Expected Files

- agency.txt
- calendar.txt
- routes.txt
- shapes.txt
- stops.txt
- stop_times.txt
- trips.txt