from pydantic import BaseModel

class UserDetails(BaseModel):
    name: str
    age: int
    height: float  # in cm
    weight: float  # in kg
    gender: str    # e.g., "male", "female", "other"
    diseases: list[str] = []  # e.g., ["diabetes"]
    allergies: list[str] = [] # e.g., ["nuts"]