from pydantic import BaseModel


class RouteStatistics(BaseModel):
    route_id: str
    total_trips: int
    stops_served: int
    average_stops_per_trip: float


class TripsByHour(BaseModel):
    hour: int
    trip_count: int


class BusiestStop(BaseModel):
    stop_id: str
    stop_name: str
    scheduled_events: int


class TripsPerRoute(BaseModel):
    route_id: str
    route_short_name: str
    route_long_name: str | None
    trip_count: int