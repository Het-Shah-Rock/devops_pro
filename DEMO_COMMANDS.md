# 🚀 QuickCart Enterprise — Full Demo Commands Guide
> Run every technology in this project end-to-end for demonstration.
> All commands are for **PowerShell** on Windows.
> Working directory: `C:\Users\shahh\Desktop\devops_project`

---

## ✅ PRE-CHECK: Verify All Tools Are Installed

```powershell
# Check Python
python --version

# Check Git
git --version

# Check Docker
docker --version

# Check kubectl
kubectl version --client
```

---

## 1️⃣ GIT & GITHUB — Version Control

```powershell
# See all commits made to this project
git log --oneline -15

# See the current status of the repository
git status

# See what files exist in the project
git ls-files

# Push any new changes to GitHub
git add .
git commit -m "Demo: Showing git in action"
git push
```

> **What to show:** The GitHub repo at https://github.com/Het-Shah-Rock/devops_pro.git with all branches, commits, and files like `Jenkinsfile`, `Dockerfile`, `k8s/`, etc.

---

## 2️⃣ PYTHON & STREAMLIT — The Application

```powershell
# Initialize the database (first time only)
python seed.py

# Run the full multi-page web application
python -m streamlit run app.py
```

> **App opens at:** http://localhost:8501
> **Pages to show:**
> - 🏪 Storefront (Hero banner, 37 products, categories)
> - 🛒 Cart (Add items, apply coupon code `SAVE20`, checkout)
> - ✅ Order Confirmation (Tracking timeline)
> - 🔥 Deals & Offers page
> - 🧾 Order History page
> - 👤 Profile page
> - 📊 Admin Dashboard (login as `admin`)
> - 🚀 DevOps Control Center (Full CI/CD visual demo)

---

## 3️⃣ SQLITE DATABASE — Inspect Data via CMD

```powershell
# Show all tables in the database
python -c "import sqlite3; c=sqlite3.connect('quickcart.db'); print(c.execute('SELECT name FROM sqlite_master WHERE type=\'table\'').fetchall())"

# View all 37 products
python -c "import sqlite3; c=sqlite3.connect('quickcart.db'); [print(row) for row in c.execute('SELECT id, name, price, stock, category FROM products')]"

# View all orders placed
python -c "import sqlite3; c=sqlite3.connect('quickcart.db'); [print(row) for row in c.execute('SELECT * FROM orders')]"

# View all coupons
python -c "import sqlite3; c=sqlite3.connect('quickcart.db'); [print(row) for row in c.execute('SELECT code, discount_pct, min_order FROM coupons')]"
```

---

## 4️⃣ PYTEST — Automated Unit Testing

```powershell
# Run all 6 unit tests (should all PASS)
python -m pytest tests/ -v

# Run tests with coverage report (for SonarQube)
python -m pytest tests/ --cov=. --cov-report=xml:coverage.xml --junitxml=test-results.xml -v
```

> **Expected output:** `6 passed in 0.65s`

---

## 5️⃣ DOCKER — Containerization

```powershell
# Build the Docker image manually (multi-stage build)
docker build -t devops-quickcart:latest .

# See the built image details
docker images | Select-String "quickcart"

# Run the app as a Docker container
docker run -d -p 8080:8501 --name quickcart-demo devops-quickcart:latest

# Check the running container
docker ps

# See container logs
docker logs quickcart-demo

# Stop and remove the demo container
docker stop quickcart-demo
docker rm quickcart-demo
```

> **App runs at:** http://localhost:8080 (Docker version)

---

## 6️⃣ DOCKER COMPOSE — Multi-Service Orchestration

```powershell
# Build and start all services defined in docker-compose.yml
docker-compose up --build -d

# See running services
docker-compose ps

# See live logs from the app container
docker-compose logs -f

# Stop all services
docker-compose down
```

> **App runs at:** http://localhost:8080 (Docker Compose version)

---

## 7️⃣ JENKINS — CI/CD Pipeline

```powershell
# Start the Jenkins server (if not already running)
docker start jenkins_server

# Check Jenkins is running
docker ps | Select-String "jenkins"
```

> **Jenkins Dashboard:** http://localhost:8081
> **Steps to show:**
> 1. Login (username: `het`)
> 2. Click `QuickCart-DevOps-Pipeline`
> 3. Click `Build Now`
> 4. Click on build `#` → `Console Output`
> 5. Show pipeline stages: Checkout → Lint → Security → Test → Docker Build → K8s Deploy → SUCCESS

---

## 8️⃣ KUBERNETES — Container Orchestration (Manifests)

```powershell
# Show all K8s config files
Get-ChildItem k8s\

# View the Deployment config (2 replicas, liveness probes, resource limits)
Get-Content k8s\deployment.yaml

# View the Auto-Scaler config (scales 2 to 10 pods on CPU load)
Get-Content k8s\hpa.yaml

# View the Persistent Volume (saves database across pod restarts)
Get-Content k8s\pv-pvc.yaml

# View the ConfigMap (environment variable injection)
Get-Content k8s\configmap.yaml

# View the Secret (secure credentials injection)
Get-Content k8s\secret.yaml

# View the Ingress (hostname-based routing)
Get-Content k8s\ingress.yaml

# --- If Kubernetes cluster is enabled in Docker Desktop ---
# Apply all manifests to the cluster
kubectl apply -f k8s\pv-pvc.yaml
kubectl apply -f k8s\configmap.yaml
kubectl apply -f k8s\secret.yaml
kubectl apply -f k8s\deployment.yaml
kubectl apply -f k8s\service.yaml

# Check pod status
kubectl get pods

# Check all resources
kubectl get all

# See the autoscaler
kubectl get hpa
```

---

## 9️⃣ SONARQUBE — Code Quality & Security Analysis

```powershell
# Start the SonarQube server (if not already running)
docker start sonarqube-server

# Check it is running
docker ps | Select-String "sonar"

# Wait ~60 seconds then check status (should show "UP")
curl.exe -s http://localhost:9000/api/system/status

# Run the full code quality scan against your project
docker run --rm --name sonar-scanner `
    -v "${PWD}:/usr/src" `
    --add-host=host.docker.internal:host-gateway `
    sonarsource/sonar-scanner-cli `
    "-Dsonar.projectKey=quickcart-enterprise" `
    "-Dsonar.projectName=QuickCart Enterprise" `
    "-Dsonar.projectVersion=1.0" `
    "-Dsonar.sources=." `
    "-Dsonar.inclusions=app.py,database.py,seed.py" `
    "-Dsonar.exclusions=**/__pycache__/**,quickcart.db" `
    "-Dsonar.host.url=http://host.docker.internal:9000" `
    "-Dsonar.token=squ_692e3e4ba441c5711bc310b5902ee708c4dedb9f"
```

> **SonarQube Dashboard:** http://localhost:9000
> **Login:** `admin` / `QuickCart@DevOps2026`
> **Project:** QuickCart Enterprise (shows Bugs, Code Smells, Security Hotspots, Coverage)

---

## 🔁 FULL DEMO — Start Everything at Once

Run these commands in order for a complete live demonstration:

```powershell
# STEP 1: Start Jenkins
docker start jenkins_server

# STEP 2: Start SonarQube
docker start sonarqube-server

# STEP 3: Start the App via Docker Compose
docker-compose up --build -d

# STEP 4: Run the Streamlit App directly (for live coding demo)
python -m streamlit run app.py

# STEP 5: Run Tests
python -m pytest tests/ -v

# STEP 6: Check all running Docker containers
docker ps
```

### 🌐 All Active URLs After Full Start:

| Service | URL | Credentials |
|---|---|---|
| **Streamlit App** | http://localhost:8501 | `admin` / `admin` |
| **Docker App** | http://localhost:8080 | — |
| **Jenkins** | http://localhost:8081 | `het` / your password |
| **SonarQube** | http://localhost:9000 | `admin` / `QuickCart@DevOps2026` |
| **GitHub Repo** | https://github.com/Het-Shah-Rock/devops_pro | — |

---

## 📁 Project File Structure (For Report)

```
devops_project/
├── app.py                     # Main Storefront (Streamlit)
├── database.py                # SQLite schema & connection
├── seed.py                    # 37 products + 4 coupons seeder
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Multi-stage Docker build
├── docker-compose.yml         # Local orchestration
├── Jenkinsfile                # CI/CD pipeline definition
├── sonar-project.properties   # SonarQube config
├── run_sonar.bat              # One-click SonarQube scanner
├── trigger_jenkins.py         # Jenkins API automation script
├── Makefile                   # Developer shortcuts
├── pages/
│   ├── 0_DevOps_Control_Center.py  # CI/CD visual dashboard
│   ├── 1_Cart.py                   # Shopping cart + checkout
│   ├── 2_Order_Confirmation.py     # Post-order tracking
│   ├── 3_Deals_and_Offers.py       # Deals page
│   ├── 4_Order_History.py          # Past orders + reorder
│   ├── 5_Profile.py                # User profile management
│   └── 6_Admin_Dashboard.py        # Admin analytics panel
├── k8s/
│   ├── deployment.yaml        # 2 replicas, resource limits
│   ├── service.yaml           # Expose app on port 80
│   ├── ingress.yaml           # Domain routing (quickcart.local)
│   ├── hpa.yaml               # Auto-scale 2-10 pods
│   ├── pv-pvc.yaml            # Persistent database storage
│   ├── configmap.yaml         # Environment variable injection
│   └── secret.yaml            # Secure credentials injection
├── tests/
│   └── test_database.py       # 6 automated unit tests
└── .github/
    └── workflows/
        └── ci-cd.yml          # GitHub Actions pipeline
```
