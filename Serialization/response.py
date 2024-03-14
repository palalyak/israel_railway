from pydantic import BaseModel
from typing import List, Optional

class StopStation(BaseModel):
    stationId: int
    arrivalTime: str
    departureTime: str
    platform: int
    crowded: float

class RouteStation(BaseModel):
    stationId: int
    arrivalTime: str
    crowded: float
    platform: int

class TrainPosition(BaseModel):
    currentLastStation: int
    nextStation: int
    calcDiffMinutes: int
class Train(BaseModel):
    trainNumber: int
    orignStation: int
    destinationStation: int
    originPlatform: int
    destPlatform: int
    freeSeats: int
    arrivalTime: str
    departureTime: str
    stopStations: List[StopStation]
    handicap: int
    crowded: float
    trainPosition: Optional[TrainPosition] = None
    routeStations: List[RouteStation]

class Travel(BaseModel):
    departureTime: str
    arrivalTime: str
    freeSeats: int
    travelMessages: List[str] = []
    trains: List[Train]

class Result(BaseModel):
    numOfResultsToShow: int
    startFromIndex: int
    onFocusIndex: int
    clientMessageId: int
    freeSeatsError: bool
    travels: List[Travel]

class ApiResponse(BaseModel):
    creationDate: str
    version: str
    successStatus: int
    statusCode: int
    errorMessages: Optional[str] = None
    result: Result