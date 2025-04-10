from fastapi import FastAPI, HTTPException, Request
import uvicorn
import os
from app.controlador.PatientCrud import GetPatientById, WritePatient, GetPatientByIdentifier
from fastapi.middleware.cors import CORSMiddleware

# Crear la aplicación FastAPI
app = FastAPI()

# ✅ Configuración de CORS corregida
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hl7-fhir-ehr-diego-sordella.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to HL7 FHIR API"}

@app.get("/status")
async def check_status():
    return {"message": "API is running on hl7-fhir-ehr-diego-sordella.onrender.com"}

@app.get("/patient/{patient_id}", response_model=dict)
async def get_patient_by_id(patient_id: str):
    print(f"🔍 Buscando paciente con ID: {patient_id}")
    status, patient = GetPatientById(patient_id)
    
    if status == 'success':
        return patient
    elif status == 'notFound':
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")

@app.get("/patient", response_model=dict)
async def get_patient_by_identifier(system: str, value: str):
    print(f"🔍 Buscando paciente con System: {system}, ID: {value}")
    status, patient = GetPatientByIdentifier(system, value)
    
    if status == 'success':
        return patient
    elif status == 'notFound':
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")

@app.post("/patient", response_model=dict)
async def add_patient(request: Request):
    new_patient_dict = dict(await request.json())
    print(f"📝 Recibiendo nuevo paciente: {new_patient_dict}")
    
    status, patient_id = WritePatient(new_patient_dict)
    
    if status == 'success':
        return {"_id": patient_id}
    else:
        raise HTTPException(status_code=500, detail=f"Validating error: {status}")

# ✅ Esta línea corregida permite ejecutar localmente
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


