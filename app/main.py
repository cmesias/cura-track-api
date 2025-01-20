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

# Pydantic model for Patients
class Patients(BaseModel):
    date_of_birth: str
    email: str
    employement_status: str
    first_name: str
    last_name: str
    role: str
    uid: str
    username: str

@app.post("/patients/")
async def create_patient(patient: Patients):
    response = supabase.table('patients').insert({
        'date_of_birth': patient.date_of_birth,
        'email': patient.email,
        'employement_status': patient.employement_status,
        'first_name': patient.first_name,
        'last_name': patient.last_name,
        'role': patient.role,
        'uid': patient.uid,
        'username': patient.username
    }).execute()
    
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Error creating patient record")

    return {"message": "Patients record created successfully"}

@app.get("/patients/")
async def get_patients():
    response = supabase.table('patients').select("*").execute()
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error fetching patients")

    return response.data
