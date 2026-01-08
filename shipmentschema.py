from pydantic import BaseModel
from typing import Optional

from enum import Enum


class Shipment(BaseModel):
    id: int | None
    item: str 
    quantity: int
    status: str

   
class ShipmentStatus(str, Enum):
    pending = "pending"
    in_transit = "in_transit"
    delivered = "delivered"  

class ShipmentPatch(BaseModel):
    status: Optional[ShipmentStatus] = None