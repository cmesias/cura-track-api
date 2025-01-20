from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Initialize Supabase client
SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pydantic model for FacilityAdmin
class FacilityAdmin(BaseModel):
    name: str
    age: int
    condition: str

@app.post("/facility_admins/")
async def create_facility_admin(facility_admin: FacilityAdmin):
    response = supabase.table('facility_admins').insert({
        'name': facility_admin.name,
        'age': facility_admin.age,
        'condition': facility_admin.condition
    }).execute()
    
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Error creating facility_admin record")

    return {"message": "FacilityAdmin record created successfully"}

@app.get("/facility_admins/")
async def get_facility_admins():
    response = supabase.table('facility_admins').select("*").execute()
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error fetching facility_admins")

    return response.data
