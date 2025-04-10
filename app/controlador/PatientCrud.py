from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.patient import Patient
import json

collection = connect_to_mongodb("SamplePatientService", "patients")

def GetPatientById(patient_id: str):
    try:
        patient = collection.find_one({"_id": ObjectId(patient_id)})
        if patient:
            patient["_id"] = str(patient["_id"])
            return "success", patient
        return "notFound", None
    except Exception as e:
        return f"notFound", None



def WritePatient(patient_data):
    print("🟡 WritePatient llamada con:", patient_data)
    try:
        # Validar recurso FHIR
        patient = Patient(**patient_data)
        print("✅ Validación FHIR exitosa")

        # Insertar en MongoDB
        patient_dict = patient.dict()
        print("📦 Diccionario a insertar:", patient_dict)

        insert_result = patients_collection.insert_one(patient_dict)
        print("🟢 Insertado correctamente:", insert_result.inserted_id)

        return "success", str(insert_result.inserted_id)

    except Exception as e:
        print(f"❌ Error en WritePatient: {e}")
        return "error", None
    

def GetPatientByIdentifier(patientSystem, patientValue):
    try:
        print(f"🔍 Buscando en MongoDB con system={patientSystem}, value={patientValue}")  
        patient = collection.find_one({"identifier.system": patientSystem, "identifier.value": patientValue})  
        
        if patient:
            patient["_id"] = str(patient["_id"])
            print(f"✅ Paciente encontrado: {patient}")
            return "success", patient
        
        print("⚠ Paciente no encontrado")
        return "notFound", None
    except Exception as e:
        print(f"❌ Error: {str(e)}")  # <-- Log del error exacto
        return f"error:{str(e)}",None