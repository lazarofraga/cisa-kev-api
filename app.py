from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Vulnerability(BaseModel):
    cveID: str
    vendorProject: str
    product: str
    vulnerabilityName: str
    dateAdded: str
    shortDescription: str
    requiredAction: str
    dueDate: str
    notes: str = None  # Assuming 'notes' might be optional

def execute_query(query: str, parameters: tuple):
    with sqlite3.connect("kev_list.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()

def convert_to_vulnerability(vuln: tuple):
    keys = [
        "cveID", "vendorProject", "product", "vulnerabilityName",
        "dateAdded", "shortDescription", "requiredAction", "dueDate", "notes"
    ]
    return Vulnerability(**dict(zip(keys, vuln)))

def get_vulnerabilities(query: str, parameters: tuple):
    vulnerabilities = execute_query(query, parameters)
    return [convert_to_vulnerability(vuln) for vuln in vulnerabilities]

def get_vulnerability_by_cve_id(cve_id: str):
    vulnerabilities = get_vulnerabilities("SELECT * FROM vulnerabilities WHERE cveID = ?", (cve_id,))
    return vulnerabilities[0] if vulnerabilities else None

@app.get("/vulnerability/{cve_id}", response_model=Vulnerability)
def read_vulnerability(cve_id: str):
    vulnerability = get_vulnerability_by_cve_id(cve_id)
    if vulnerability is None:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    return vulnerability

@app.get("/search/{query}", response_model=list[Vulnerability])
def search_vulnerabilities(query: str):
    query_str = "SELECT * FROM vulnerabilities WHERE vulnerabilityName LIKE ?"
    return get_vulnerabilities(query_str, ('%' + query + '%',))
