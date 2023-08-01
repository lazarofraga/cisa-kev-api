from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3


app = FastAPI()

# Define a Pydantic model for the response
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

def get_vulnerability_by_cve_id(cve_id: str):
    conn = sqlite3.connect("kev_list.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vulnerabilities WHERE cveID = ?", (cve_id,))
    vulnerability = cursor.fetchone()
    conn.close()

    # If found, return the data as an instance of the Vulnerability model
    if vulnerability:
        return Vulnerability(
            cveID=vulnerability[0],
            vendorProject=vulnerability[1],
            product=vulnerability[2],
            vulnerabilityName=vulnerability[3],
            dateAdded=vulnerability[4],
            shortDescription=vulnerability[5],
            requiredAction=vulnerability[6],
            dueDate=vulnerability[7],
            notes=vulnerability[8]
        )

@app.get("/vulnerability/{cve_id}", response_model=Vulnerability)
def read_vulnerability(cve_id: str):
    vulnerability = get_vulnerability_by_cve_id(cve_id)
    if vulnerability is None:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    return vulnerability


@app.get("/search/{query}", response_model=list[Vulnerability])
def search_vulnerabilities(query: str):
    conn = sqlite3.connect("kev_list.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vulnerabilities WHERE vulnerabilityName LIKE ?", ('%' + query + '%',))
    vulnerabilities = cursor.fetchall()
    conn.close()

    # Convert the raw vulnerabilities to instances of the Vulnerability model
    matching_vulnerabilities = [Vulnerability(
        cveID=vuln[0],
        vendorProject=vuln[1],
        product=vuln[2],
        vulnerabilityName=vuln[3],
        dateAdded=vuln[4],
        shortDescription=vuln[5],
        requiredAction=vuln[6],
        dueDate=vuln[7],
        notes=vuln[8]
    ) for vuln in vulnerabilities]

    return matching_vulnerabilities
