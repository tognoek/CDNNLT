from pydantic import BaseModel
class HotDestination(BaseModel):
    id_post: int
    tour_type_category: str
    image: str
    name: str
    url: str
    type: str
    count: int

class ListTour(BaseModel):
    id_post: int
    name: str
    image: str
    url: str
    type: str
    count: int

class ListTourAll(BaseModel):
    id_post: int
    name: str
    url: str
    category: str
    price: float
    image: str
    type: str
    location: str
    code: str