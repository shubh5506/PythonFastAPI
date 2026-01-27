
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class Shipment(BaseModel):
    id: Optional[int] = None
    item: str 
    quantity: int
    status: str
    order_date: datetime
    is_duplicate: bool = False
   
class ShipmentStatus(str, Enum):
    pending = "pending"
    in_transit = "in_transit"
    delivered = "delivered"  

class ShipmentPatch(BaseModel):
    status: Optional[ShipmentStatus] = None