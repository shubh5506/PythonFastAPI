from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

shipmentdata = [
    {"id": 1, "item": "Laptop", "quantity": 2},
    {"id": 2, "item": "Phone", "quantity": 5},
    {"id": 3, "item": "Tablet", "quantity": 3}, 
]

@app.get("/shipment")
async def get_shipment():
    return {"message": "Shipment details will be here.",
            "status": "This is a placeholder for shipment information."
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
    return {"message": "Shipment not found"}

@app.get("/scalar", include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Shipment API Scalar Reference",
    )
        