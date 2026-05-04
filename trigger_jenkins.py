import urllib.request
import base64
import json
import sys

# === CONFIGURATION ===
JENKINS_URL = "http://localhost:8081"
JOB_NAME = "QuickCart-DevOps-Pipeline"  # Ensure this perfectly matches your Jenkins Job name
USER = "het"
PASS = "admin123"

# Encode credentials for Basic Auth
creds = f"{USER}:{PASS}".encode('utf-8')
auth_header = b"Basic " + base64.b64encode(creds)

print(f"[*] Connecting to Jenkins DevOps Server at {JENKINS_URL}...")

try:
    # STEP 1: Bypass Security by fetching a valid CSRF Crumb
    crumb_req = urllib.request.Request(f"{JENKINS_URL}/crumbIssuer/api/json")
    crumb_req.add_header("Authorization", auth_header)
    
    with urllib.request.urlopen(crumb_req) as response:
        crumb_data = json.loads(response.read().decode())
        crumb_field = crumb_data['crumbRequestField']
        crumb_value = crumb_data['crumb']
        print(f"[OK] Security Crumb obtained: {crumb_value[:8]}...")

    # STEP 2: Send the POST request to trigger the build, attaching the Crumb
    build_url = f"{JENKINS_URL}/job/{JOB_NAME}/build"
    build_req = urllib.request.Request(build_url, method="POST")
    build_req.add_header("Authorization", auth_header)
    build_req.add_header(crumb_field, crumb_value)

    with urllib.request.urlopen(build_req) as response:
        if response.getcode() == 201:
            print(f"[SUCCESS] PIPELINE TRIGGERED! Started automated build for '{JOB_NAME}'.")
            print("-> Go to http://localhost:8081 to watch the CI/CD pipeline run live!")
        else:
            print(f"[WARNING] Triggered, but got unexpected status code: {response.getcode()}")

except urllib.error.HTTPError as e:
    print(f"[ERROR] HTTP Error: {e.code} - {e.reason}")
    if e.code == 404:
        print(f"-> ERROR: Jenkins could not find a job named '{JOB_NAME}'. Did you name it something else?")
    elif e.code == 401:
        print("-> ERROR: Authentication failed. Is your password definitely 'admin123'?")
except Exception as e:
    print(f"[ERROR] Error communicating with Jenkins: {e}")
