from pydantic import BaseModel


class Customer(BaseModel):
    id: int


class Provider(BaseModel):
    id: int

