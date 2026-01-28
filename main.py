from fastapi import FastAPI, HTTPException
from scalar_fastapi import get_scalar_api_reference
from datetime import datetime, timedelta    
from shipmentschema import Shipment, ShipmentPatch
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://www.shubhamsarpal.com",
        "https://shubhamsarpal.com",  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

shipmentdata = [
    {"id": 1, "item": "Laptop", "quantity": 2, "status": "in transit", "order_date": datetime.now(), "is_duplicate": False},
    {"id": 2, "item": "Phone", "quantity": 5, "status": "delivered", "order_date": datetime.now(), "is_duplicate": False},
    {"id": 3, "item": "Tablet", "quantity": 3, "status": "pending", "order_date": datetime.now(), "is_duplicate": True}, 
]

DUPLICATE_WINDOW = timedelta(minutes=5)

shipments: List["Shipment"] = []
current_id = 1
   

@app.get("/shipment")
async def get_shipment():
    return {"message": "Welcome to the Shipment API",
            "items": shipmentdata,
        }

@app.get("/shipment/{shipment_id}")
def get_shipment_by_id(shipment_id: int):
    return {"shipment_id": shipment_id,
            "details": "Details for shipment with ID {}".format(shipment_id)
        }

@app.get("/shipments/latest")
def get_latest_shipments():
    return {"latest_shipments": shipmentdata[-2:]}  # Return the last two shipments

@app.get("/shipments/count")
def get_shipments_count():
    return {"total_shipments": len(shipmentdata)}

@app.get("/shipments/search/{shipment_id}")
def search_shipment(shipment_id: int):
    shipment = next((s for s in shipmentdata if s["id"] == shipment_id), None)
    if shipment:
        return {"shipment": shipment}
    if id not in shipmentdata:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
@app.post("/shipments/add")
def add_shipment(item: str, quantity: int, status: str):
    if status != "pending":
        raise HTTPException(status_code=406, detail="Status must be 'pending' for new shipments and quantity must not exceed 99.")
    new_id = max(s["id"] for s in shipmentdata) + 1
    new_shipment = {"id": new_id, "item": item, "quantity": quantity, "status": status}
    shipmentdata.append(new_shipment)
    return {"message": "Shipment added successfully", "shipment": new_shipment}

    
@app.post("/shipments-models/add")
def add_shipment_models(shipment: Shipment):
    if shipment.status != "pending":
        raise HTTPException(status_code=406, detail="Status must be 'pending' for new shipments")
    new_id = max(s["id"] for s in shipmentdata) + 1
    new_shipment = {"id": new_id, "item": shipment.item, "quantity": shipment.quantity, "status": shipment.status}
    shipmentdata.append(new_shipment)
    return {"message": "Shipment added successfully", "shipment": new_shipment}

@app.put("/shipments/update/{shipment_id}")
def update_shipment(shipment_id: int, status: str, quantity: int, item: str):
    shipment = next((s for s in shipmentdata if s["id"] == shipment_id), None)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    shipment["status"] = status
    shipment["quantity"] = quantity
    shipment["item"] = item
    return {"message": "Shipment updated successfully", "shipment": shipment}

@app.patch("/shipments/patch/{shipment_id}")
def patch_shipment(shipment_id: int, status: str = None, quantity: int = None, item: str = None):
    shipment = next((s for s in shipmentdata if s["id"] == shipment_id), None)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    if status:
        shipment["status"] = status
    if quantity:
        shipment["quantity"] = quantity
    if item:
        shipment["item"] = item
    return {"message": "Shipment patched successfully", "shipment": shipment}

@app.patch("/shipments/partial-update/{shipment_id}")
def partial_update_shipment(
    shipment_id: int,
    body: ShipmentPatch
):
    shipment = next((s for s in shipmentdata if s["id"] == shipment_id), None)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    update_data = body.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        shipment[key] = value

    return {
        "message": "Shipment updated successfully",
        "shipment": shipment
    }
@app.delete("/shipments/delete/{shipment_id}")
def delete_shipment(shipment_id: int):
    global shipmentdata
    shipment = next((s for s in shipmentdata if s["id"] == shipment_id), None)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    shipmentdata = [s for s in shipmentdata if s["id"] != shipment_id]
    return {"message": "Shipment deleted{shipment_Id} successfully"}

def is_duplicate(shipment: Shipment) -> bool:
    for existing_shipment in shipments:
        if (existing_shipment.item == shipment.item and
            existing_shipment.quantity == shipment.quantity and
            existing_shipment.status == shipment.status):
            time_diff = abs(shipment.order_date - existing_shipment.order_date)
            if time_diff < DUPLICATE_WINDOW:
                return True
    return False

@app.post("/shipments/check-duplicate")
def check_duplicate(shipment: Shipment):
    global current_id
    shipment.is_duplicate = is_duplicate(shipment)
    shipment.id = current_id
    current_id += 1
    shipments.append(shipment)
    return {"shipment": shipment, "is_duplicate": shipment.is_duplicate}

@app.get("/shipments/duplicate-shipments")
def get_duplicate_shipments():
    return {"duplicate_shipments": [s for s in shipments if s.is_duplicate]}

@app.get("/scalar", include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Shipment API Scalar Reference",
    )
        

