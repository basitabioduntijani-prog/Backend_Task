from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Simple FastAPI CRUD App",
    version="1.0.0",
    description="A FastAPI project demonstrating Create, Read, Update (PUT/PATCH), and Delete operations."
)

# In-memory database (list of dictionaries)
data = [
    {"name": "Sam Larry", "age": 20, "track": "AI Developer"},
    {"name": "Bahubali", "age": 21, "track": "Backend Developer"},
    {"name": "John Doe", "age": 22, "track": "Frontend Developer"}
]

# Pydantic model for validation
class Item(BaseModel):
    name: str = Field(..., example="Perpetual")
    age: int = Field(..., example=25)
    track: str = Field(..., example="Fullstack Developer")

# -------------------------
# ROUTES
# -------------------------

# Root endpoint
@app.get("/", description="Welcome message route")
def root():
    return {"Message": "Welcome to my FastAPI Application"}

# GET all data
@app.get("/get-data", description="Fetch all user entries")
def get_data():
    return {"Data": data}

# POST - create new data
@app.post("/create-data", description="Add a new user entry")
def create_data(req: Item):
    new_entry = req.dict()
    data.append(new_entry)
    print("Data after creation:", data)
    return {"Message": "Data Added Successfully", "Data": data}

# PUT - update existing data by index (replace entire entry)
@app.put("/update-data/{item_id}", description="Replace an existing user entry by ID")
def update_data(item_id: int, req: Item):
    if item_id < 0 or item_id >= len(data):
        return {"Error": f"ID {item_id} not found. Valid range: 0 to {len(data) - 1}"}
    data[item_id] = req.dict()
    print("Data after full update:", data)
    return {"Message": "Data Updated Successfully", "Data": data}

# PATCH - partially update an entry
@app.patch("/patch-data/{item_id}", description="Partially update user entry by ID")
def patch_data(item_id: int, req: Item):
    if item_id < 0 or item_id >= len(data):
        return {"Error": f"ID {item_id} not found. Valid range: 0 to {len(data) - 1}"}
    existing_entry = data[item_id]
    update_fields = req.dict(exclude_unset=True)
    existing_entry.update(update_fields)
    print("Data after partial update:", data)
    return {"Message": "Data Partially Updated", "Data": data}

# DELETE - remove entry by ID
@app.delete("/delete-data/{item_id}", description="Delete user entry by ID")
def delete_data(item_id: int):
    if item_id < 0 or item_id >= len(data):
        return {"Error": f"ID {item_id} not found. Valid range: 0 to {len(data) - 1}"}
    deleted_entry = data.pop(item_id)
    print("Data after deletion:", data)
    return {"Message": "Data Deleted Successfully", "Deleted": deleted_entry, "Remaining": data}

# -------------------------
# APP RUNNER
# -------------------------
if __name__ == "__main__":
    host = os.getenv("host", "127.0.0.1")
    port = int(os.getenv("port", 8000))
    print(f"🚀 Server running on http://{host}:{port}")
    uvicorn.run("app:app", host=host, port=port, reload=True)
