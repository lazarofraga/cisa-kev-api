# CISA KEV Vulnerability API

This project fetches Known Exploited Vulnerabilities (KEV) data from the CISA website and serves it through a FastAPI application. The data is stored in an SQLite database.

## Project Structure
The project consists of two main Python scripts:

build_db.py - This script retrieves the KEV data from the CISA website and populates the SQLite database.
app.py - This script runs the FastAPI application, providing endpoints to fetch specific vulnerabilities by their CVE ID or search vulnerabilities by name.

## Getting Started

### Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
```

### Install the required Python libraries:

```bash
pip install fastapi uvicorn requests sqlite3
```
### Fetch the KEV data and populate the database:

```bash
python fetch_kev_data.py
```

### Start the app
```bash
uvicorn main:app --reload
```

 You can now interact with the API at http://localhost:8000.

### API Endpoints

`GET /vulnerability/{cve_id}` - Returns the vulnerability with the given CVE ID.


`GET /search/{query}` - Returns a list of vulnerabilities matching the given query string.

Replace <repository_url> and <repository_directory> with the appropriate URL and directory name for your project.