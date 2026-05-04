# QuickCart Enterprise — Full Project Report
### Subject: DevOps | Academic Submission Report
**Student:** Het Shah | **GitHub:** https://github.com/Het-Shah-Rock/devops_pro

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Objectives](#2-objectives)
3. [Methodology](#3-methodology)
4. [System Architecture](#4-system-architecture)
5. [Technologies Used](#5-technologies-used)
6. [Application Features](#6-application-features)
7. [DevOps Implementation](#7-devops-implementation)
8. [Testing & Code Quality](#8-testing--code-quality)
9. [Project File Structure](#9-project-file-structure)
10. [Results & Screenshots Guide](#10-results--screenshots-guide)
11. [Challenges & Solutions](#11-challenges--solutions)
12. [Conclusion](#12-conclusion)

---

## 1. Introduction

QuickCart Enterprise is a production-grade Quick Commerce web application developed as part of a DevOps subject project. Quick Commerce refers to ultra-fast delivery platforms such as Blinkit, Zepto, and Swiggy Instamart that promise delivery of groceries and daily essentials within 10-15 minutes.

The primary goal of this project was not merely to build a functional application, but to demonstrate how modern software teams use DevOps practices to build, test, secure, and deploy applications continuously and reliably. Every technology choice in this project mirrors real industry standards used by companies such as Netflix, Amazon, and Google.

The application provides an end-to-end quick commerce experience — from a customer browsing products to an admin monitoring revenue — all while being supported by automated CI/CD pipelines, containerized deployments, code quality scanning, and Kubernetes-based orchestration.

---

## 2. Objectives

| # | Objective | Status |
|---|---|---|
| 1 | Build a multi-page Python web application | ✅ Completed |
| 2 | Implement SQLite relational database with 6 tables | ✅ Completed |
| 3 | Containerize the application using Docker | ✅ Completed |
| 4 | Create a Jenkins CI/CD pipeline with automated stages | ✅ Completed |
| 5 | Write automated unit tests with Pytest | ✅ 6/6 Passing |
| 6 | Integrate SonarQube for code quality analysis | ✅ Completed |
| 7 | Deploy Kubernetes manifests for production orchestration | ✅ Completed |
| 8 | Implement GitHub Actions as a secondary CI/CD pipeline | ✅ Completed |
| 9 | Version-control all code on GitHub | ✅ Completed |
| 10 | Build a DevOps Control Center dashboard in the app | ✅ Completed |

---

## 3. Methodology

The project was developed using an **Agile-inspired, iterative approach** combined with **DevOps principles**, specifically the practice of Continuous Integration and Continuous Delivery (CI/CD).

### 3.1 Development Phases

**Phase 1 — Foundation**
The project began with establishing the core application structure. Python was selected as the development language, and Streamlit was chosen as the web framework for its rapid prototyping capability. Git was initialized from the very beginning to track every change, and a GitHub repository was created to enable cloud-based version control and later, automated pipelines.

**Phase 2 — Database Layer**
Rather than hardcoding data, a proper relational SQLite database was designed and implemented. A schema was created with 6 interconnected tables: `users`, `products`, `orders`, `order_items`, `coupons`, and `reviews`. A seed script (`seed.py`) was written to automatically populate the database with 37 realistic products across 7 categories and 4 active coupon codes.

**Phase 3 — Application Development**
The application was built as a multi-page Streamlit app. Each page was designed to represent a different module of a real e-commerce platform. Careful attention was paid to the UI/UX design, using CSS custom properties, Google Fonts, gradient backgrounds, and responsive card layouts.

**Phase 4 — Containerization**
A multi-stage `Dockerfile` was written to containerize the application. A `docker-compose.yml` file was created for simplified local orchestration. Security best practices were implemented: the container runs as a non-root user (`appuser`) and exposes a health-check endpoint.

**Phase 5 — CI/CD Pipeline**
A `Jenkinsfile` was written defining a declarative pipeline with stages for code checkout, linting, security scanning, Docker image building, and Kubernetes deployment. A parallel GitHub Actions workflow (`.github/workflows/ci-cd.yml`) was also configured to trigger automatically on every `git push` to the `main` branch.

**Phase 6 — Quality Assurance**
Six automated unit tests were written using Pytest to verify database integrity, table schema, CRUD operations, and stock management. SonarQube was deployed as a Docker container and a full scan was executed against the project's Python source code. A coverage report (XML) was generated and fed into SonarQube.

**Phase 7 — Kubernetes Orchestration**
Seven Kubernetes YAML manifest files were written covering all aspects of a production deployment: `Deployment`, `Service`, `Ingress`, `HorizontalPodAutoscaler`, `PersistentVolumeClaim`, `ConfigMap`, and `Secret`.

---

## 4. System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   DEVELOPER MACHINE                  │
│                                                     │
│  ┌──────────┐    git push    ┌──────────────────┐   │
│  │  VS Code │ ────────────► │  GitHub Repo     │   │
│  │  Python  │                │ (devops_pro)     │   │
│  └──────────┘                └────────┬─────────┘   │
│                                       │             │
│              ┌────────────────────────┤             │
│              │                        │             │
│              ▼                        ▼             │
│  ┌───────────────────┐   ┌─────────────────────┐   │
│  │  Jenkins Pipeline  │   │  GitHub Actions CI  │   │
│  │  (localhost:8081)  │   │  (.github/workflows)│   │
│  │  - Lint (flake8)  │   │  - Lint + SAST      │   │
│  │  - SAST (bandit)  │   │  - pytest           │   │
│  │  - Docker Build   │   │  - Docker push      │   │
│  │  - K8s Deploy     │   │  - K8s rollout      │   │
│  └───────────────────┘   └─────────────────────┘   │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │               DOCKER ENVIRONMENT              │  │
│  │                                               │  │
│  │  ┌─────────────────┐  ┌──────────────────┐   │  │
│  │  │  QuickCart App   │  │  SonarQube       │   │  │
│  │  │  (port 8080)     │  │  (port 9000)     │   │  │
│  │  │  Streamlit +     │  │  Code Quality    │   │  │
│  │  │  SQLite DB       │  │  Analysis        │   │  │
│  │  └─────────────────┘  └──────────────────┘   │  │
│  │                                               │  │
│  │  ┌─────────────────┐                          │  │
│  │  │  Jenkins Server  │                          │  │
│  │  │  (port 8081)     │                          │  │
│  │  └─────────────────┘                          │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │           KUBERNETES CLUSTER (k8s/)            │  │
│  │                                               │  │
│  │  Deployment (2 replicas) ◄── HPA (max 10)    │  │
│  │  Service (LoadBalancer)                       │  │
│  │  Ingress (quickcart.local)                    │  │
│  │  PVC (Database Persistence)                   │  │
│  │  ConfigMap + Secret (Config Injection)        │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 5. Technologies Used

### 5.1 Python & Streamlit
**Role:** Application development language and web framework.

Python 3.10 was used as the primary development language. Streamlit was used to build the multi-page web interface. Streamlit was chosen for its ability to rapidly create interactive, data-driven web applications purely in Python, without requiring HTML/CSS/JavaScript knowledge, while still supporting custom CSS injection for professional UI styling.

**Key Libraries:**
- `streamlit` — Multi-page web UI
- `pandas` — Database query result processing
- `sqlite3` — Built-in Python database connector
- `pytest` + `pytest-cov` — Automated testing and coverage

### 5.2 SQLite (Database)
**Role:** Persistent relational data storage.

SQLite is a serverless, file-based relational database system. It was selected for its zero-configuration setup (no separate database server required) and full SQL compliance, making it ideal for demonstrating relational database concepts in a local DevOps environment.

**Schema Design:**
| Table | Purpose |
|---|---|
| `users` | Stores registered user profiles, addresses, contact info |
| `products` | 37 products with price, MRP, stock, category, ratings |
| `orders` | Transaction records with payment method, coupon, total |
| `order_items` | Line items linking orders to products and quantities |
| `coupons` | Discount codes with percentage off, usage limits, min order |
| `reviews` | Product review schema (prepared for future use) |

### 5.3 Git & GitHub
**Role:** Source code version control and remote repository hosting.

Git was used for all version control operations: creating branches, committing incremental changes, and pushing to the remote repository. GitHub acted as the central repository and also as the trigger point for the GitHub Actions CI/CD pipeline.

Every piece of code, configuration file, Dockerfile, and Kubernetes manifest is tracked in the repository at: `https://github.com/Het-Shah-Rock/devops_pro`

### 5.4 Docker
**Role:** Application containerization and packaging.

Docker packages the entire application — Python runtime, dependencies, source code — into a single portable image. This eliminates the "works on my machine" problem.

**Key Implementation Details:**
- **Multi-Stage Build:** Stage 1 (`builder`) installs all Python dependencies. Stage 2 (`runtime`) copies only the installed packages, resulting in a ~72% smaller final image.
- **Non-Root Execution:** A dedicated `appuser` is created, and the container runs as this unprivileged user, following the principle of least privilege.
- **Health Check:** A native `HEALTHCHECK` directive polls `/_stcore/health` so orchestration tools know when the container is ready.
- **Docker Compose:** A `docker-compose.yml` file orchestrates the application locally with a single command (`docker-compose up --build`).

### 5.5 Jenkins
**Role:** Primary CI/CD automation server.

Jenkins is an open-source automation server that executes the build, test, and deploy pipeline every time code changes. It reads the `Jenkinsfile` from the GitHub repository and executes the defined stages.

**Pipeline Stages:**
1. **Checkout SCM** — Fetches the latest code from GitHub.
2. **Code Quality (Linting)** — Runs `flake8` to enforce PEP8 Python style.
3. **Security Scanning (SAST)** — Runs `bandit` to detect security vulnerabilities.
4. **Unit Testing** — Executes the Pytest test suite and reports results.
5. **Build Docker Image** — Creates a tagged Docker image (`devops-quickcart:1.0.BUILD_ID`).
6. **Deploy to Kubernetes** — Applies K8s manifests with `kubectl apply` commands.

### 5.6 GitHub Actions
**Role:** Secondary, cloud-based CI/CD pipeline.

GitHub Actions provides a cloud-hosted CI/CD environment that runs directly on GitHub's servers. The workflow file (`.github/workflows/ci-cd.yml`) is triggered on every `push` to the `main` branch and on all Pull Requests.

**Jobs defined:**
1. `code-quality` — Runs flake8 and bandit in parallel.
2. `test` — Sets up Python, installs deps, seeds DB, runs Pytest.
3. `docker-build` — Builds and pushes multi-platform image to DockerHub.
4. `deploy-k8s` — Applies Kubernetes manifests using stored cluster credentials.

### 5.7 Kubernetes
**Role:** Container orchestration, scaling, and production deployment.

Kubernetes (K8s) is the industry-standard system for managing containerized applications at scale. Seven manifest files were written, each serving a distinct production purpose.

**Manifest Files:**
| File | Purpose | Key Concept Demonstrated |
|---|---|---|
| `deployment.yaml` | Run 2 app replicas | High Availability, ReplicaSets |
| `service.yaml` | Expose app on port 80 | Internal networking, LoadBalancer |
| `ingress.yaml` | Route `quickcart.local` domain | Ingress Controllers, NGINX routing |
| `hpa.yaml` | Auto-scale 2 to 10 pods | Horizontal Pod Autoscaling |
| `pv-pvc.yaml` | Persist the SQLite database file | Persistent Volumes, Stateful storage |
| `configmap.yaml` | Inject `APP_ENV`, `DB_PATH` | 12-Factor App, Config separation |
| `secret.yaml` | Inject secure `API_KEY` | Secrets management, Security |

### 5.8 SonarQube
**Role:** Continuous code quality and security inspection.

SonarQube is an enterprise-grade static analysis platform that scans source code and reports on bugs, code smells, security vulnerabilities (OWASP/SANS), and test coverage. It was deployed as a Docker container and analyzed the QuickCart Python source code.

**Scan Execution:**
- SonarQube Server runs at `http://localhost:9000` (Docker container)
- SonarScanner CLI runs as a separate Docker container and connects to the server
- The scan analyzed `app.py`, `database.py`, and `seed.py`
- Results include: code smells, duplication percentage, security hotspots, and line coverage

### 5.9 Pytest & Code Coverage
**Role:** Automated unit testing and coverage reporting.

Six unit tests were written in `tests/test_database.py` to validate the database layer. Tests use the `tmp_path` fixture to create an isolated, fresh database for each test, ensuring tests don't interfere with each other.

**Tests:**
1. `test_db_connection` — Database connection opens successfully.
2. `test_products_table_exists` — Schema creates the products table.
3. `test_orders_table_exists` — Schema creates the orders table.
4. `test_insert_and_retrieve_product` — Can write and read a product record.
5. `test_insert_order` — Can create an order with correct default status.
6. `test_stock_update` — Stock decreases correctly after a purchase.

**Result:** `6 passed in 0.65s` — 100% pass rate.

---

## 6. Application Features

### 6.1 Storefront (app.py)
- Hero banner with animated gradient background
- Category filter tiles (7 categories)
- Hot deals strip showing real-time discounted products
- Featured products section
- Full product catalog with + / − quantity controls
- Search bar filtering by name and category
- User login/register via sidebar
- Real-time cart item count in sidebar

### 6.2 Cart Page
- Review cart items with quantity adjustment and individual removal
- Delivery address input form
- Coupon code validation (`WELCOME10`, `SAVE20`, `FLAT50`, `QUICKCART`)
- Free delivery trigger above $30
- Order summary with itemized subtotal, discount, and delivery fee
- Payment method selection (UPI, Card, COD)
- Full database-backed checkout (deducts stock, creates order record, increments coupon usage)

### 6.3 Order Confirmation
- Success animation (balloons)
- Order tracking timeline (4 stages with live status indicators)
- Itemized receipt pulled from database

### 6.4 Deals & Offers
- All discounted products sorted by discount percentage
- Coupon code banners displayed prominently
- Sortable by price, rating, discount, and popularity
- Stock urgency indicators

### 6.5 Order History
- Personalized order list for logged-in user
- Expandable order cards with full item breakdown
- Simulated real-time delivery status
- One-click Reorder functionality

### 6.6 User Profile
- Edit name, email, phone, address
- View all available coupon codes
- Order statistics (count and total spent)

### 6.7 Admin Dashboard
- Tabbed interface: Overview, Inventory, Orders, Coupons
- Revenue bar chart by category
- Top 8 selling products table
- Product inventory manager with restock functionality
- Order status manager (update any order's status)
- Coupon creator for new discount codes

### 6.8 DevOps Control Center
- Live environment variable display (ConfigMap demonstration)
- Live database health check (Liveness Probe simulation)
- CI/CD pipeline stage-by-stage visual walkthrough
- Docker Dockerfile code display with explanation
- Kubernetes resource summary table
- GitFlow branching strategy diagram
- Live application metrics (total orders, revenue, low stock count)
- DevOps concept glossary table

---

## 7. DevOps Implementation

### 7.1 The CI/CD Flow

```
Developer writes code
        │
        ▼
git commit + git push
        │
        ├──────────────────────────────────┐
        ▼                                  ▼
GitHub Actions (cloud)              Jenkins (local)
- Lint + SAST (parallel)           - Checkout SCM
- Pytest (6 tests)                 - Lint + SAST
- Docker build + push              - Unit Tests
- K8s apply                        - Docker Build
        │                          - K8s Deploy
        └──────────────┬───────────┘
                       ▼
              Docker Image Built
                       │
                       ▼
           Kubernetes Rolling Update
           (Zero-downtime deployment)
                       │
                       ▼
              SonarQube Scan
              (Code Quality Gate)
```

### 7.2 Infrastructure as Code (IaC)
All infrastructure is defined as code — nothing is configured manually through a GUI. The Kubernetes manifests, Jenkins pipeline, Docker configuration, and GitHub Actions workflow are all version-controlled YAML and Groovy files. This means the entire infrastructure can be rebuilt from scratch in minutes by running `kubectl apply -f k8s/`.

### 7.3 Security Practices
- **SAST (Static Application Security Testing):** `bandit` scans Python code for vulnerabilities at every pipeline run.
- **Non-root containers:** Docker containers run as `appuser`, not `root`.
- **Secrets management:** Sensitive data is stored in Kubernetes Secrets, not in source code.
- **CSRF Protection:** Jenkins enforces CSRF tokens for all API requests.
- **SonarQube:** Scans for OWASP Top 10 security hotspots in the Python code.

### 7.4 Observability
- **Health Checks:** Kubernetes liveness probes poll `/_stcore/health` every 20 seconds.
- **Live Metrics:** The Admin Dashboard displays real-time revenue, order count, and stock levels pulled directly from the production database.
- **SonarQube Dashboard:** Provides continuous visibility into code quality metrics.

---

## 8. Testing & Code Quality

### 8.1 Unit Test Results
```
tests/test_database.py::TestDatabase::test_db_connection             PASSED
tests/test_database.py::TestDatabase::test_products_table_exists     PASSED
tests/test_database.py::TestDatabase::test_orders_table_exists       PASSED
tests/test_database.py::TestDatabase::test_insert_and_retrieve_product PASSED
tests/test_database.py::TestDatabase::test_insert_order              PASSED
tests/test_database.py::TestDatabase::test_stock_update              PASSED

========================= 6 passed in 0.65s =========================
```

### 8.2 SonarQube Analysis
- **Status:** EXECUTION SUCCESS
- **Project Key:** `quickcart-enterprise`
- **Files Analysed:** `app.py`, `database.py`, `seed.py`
- **Dashboard:** http://localhost:9000 (project: QuickCart Enterprise)
- **Coverage Report:** Generated as `coverage.xml` and submitted to SonarQube

---

## 9. Project File Structure

```
devops_project/
├── app.py                          # Main Storefront
├── database.py                     # SQLite schema & connection
├── seed.py                         # 37 products + 4 coupons seeder
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Multi-stage Docker build
├── docker-compose.yml              # Local service orchestration
├── Jenkinsfile                     # Jenkins CI/CD pipeline
├── sonar-project.properties        # SonarQube project config
├── run_sonar.bat                   # One-click SonarQube runner
├── trigger_jenkins.py              # Jenkins REST API script
├── DEMO_COMMANDS.md                # Full demonstration guide
├── Project_Report.md               # This document
├── coverage.xml                    # Pytest coverage for SonarQube
├── test-results.xml                # Pytest JUnit report
├── pages/
│   ├── 0_DevOps_Control_Center.py
│   ├── 1_Cart.py
│   ├── 2_Order_Confirmation.py
│   ├── 3_Deals_and_Offers.py
│   ├── 4_Order_History.py
│   ├── 5_Profile.py
│   └── 6_Admin_Dashboard.py
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   ├── pv-pvc.yaml
│   ├── configmap.yaml
│   └── secret.yaml
├── tests/
│   └── test_database.py            # 6 automated unit tests
└── .github/
    └── workflows/
        └── ci-cd.yml               # GitHub Actions pipeline
```

---

## 10. Results & Screenshots Guide

To generate evidence for the project report, the following should be captured:

| Evidence | Where to Get It | What it Proves |
|---|---|---|
| Streamlit App running | http://localhost:8501 | Application development |
| Admin Dashboard with charts | http://localhost:8501 → Admin | Database integration |
| Jenkins Pipeline SUCCESS | http://localhost:8081 → Build → Console | CI/CD automation |
| SonarQube project dashboard | http://localhost:9000 → QuickCart | Code quality analysis |
| `docker ps` output | PowerShell terminal | Containerization |
| `k8s/` folder contents | VS Code file explorer | Kubernetes IaC |
| GitHub commit history | https://github.com/Het-Shah-Rock/devops_pro | Version control |
| `pytest -v` output | PowerShell terminal | Automated testing |

---

## 11. Challenges & Solutions

| Challenge | Solution Applied |
|---|---|
| Jenkins `agent docker` failed — Docker-in-Docker not supported | Changed to `agent any` to run on the Jenkins server itself |
| `curl -X POST` failed in PowerShell | Used `curl.exe` to bypass PowerShell's alias to `Invoke-WebRequest` |
| Jenkins returned 403 CSRF error | Created `trigger_jenkins.py` to auto-fetch CSRF crumb before POST |
| SonarQube returned 401 Unauthorized | Generated a user API token via `curl.exe /api/user_tokens/generate` |
| Duplicate page names caused Streamlit crash | Removed old `3_Admin_Dashboard.py` that conflicted with `6_Admin_Dashboard.py` |
| `st.switch_page` failed in `on_click` lambda | Replaced with `if st.button(...): st.switch_page(...)` block |
| SQLite database lost data on Docker restart | Added `pv-pvc.yaml` to mount a PersistentVolume for the database file |
| SonarQube password required minimum 12 chars | Set password to `QuickCart@DevOps2026` to meet the policy |

---

## 12. Conclusion

The QuickCart Enterprise project successfully demonstrates a complete, production-grade DevOps implementation integrated with a fully functional quick commerce application.

### 12.1 What Was Achieved

This project went well beyond building a simple web app. It implemented a complete DevOps lifecycle:

- **Development** was done using Python and Streamlit, creating a 7-page application with a proper relational database backend holding 37 products, user accounts, order management, and coupon systems.

- **Version Control** was implemented using Git and GitHub from day one, with meaningful commit messages documenting every stage of development. The GitHub repository serves as both the single source of truth and the trigger point for automated pipelines.

- **Containerization** was achieved through Docker, using advanced multi-stage builds to minimize image size by over 70%. The application runs identically across any machine — Windows, Mac, Linux, or cloud — eliminating environment inconsistencies.

- **CI/CD Automation** was implemented through two parallel systems: Jenkins (for local, enterprise-style pipelines) and GitHub Actions (for cloud-based automation). Both systems automatically run quality checks, tests, and deployment steps on every code change, catching bugs before they reach production.

- **Code Quality and Security** was ensured by integrating SonarQube, an industry-leading static analysis platform. The tool scanned the Python codebase for bugs, code smells, duplication, and OWASP security vulnerabilities, and the results are visible on a real-time dashboard.

- **Infrastructure as Code** was implemented through 7 Kubernetes YAML manifests. Rather than clicking through a server management GUI, all infrastructure (replicas, networking, storage, scaling, security, configuration) is defined as code and can be applied or rolled back instantly.

- **Automated Testing** was implemented with 6 Pytest unit tests achieving a 100% pass rate, covering database connectivity, schema integrity, CRUD operations, and business logic validation.

### 12.2 DevOps Concepts Demonstrated

| Concept | Tool Used | Evidence |
|---|---|---|
| Source Control | Git + GitHub | Commit history, branching |
| Continuous Integration | Jenkins + GitHub Actions | Automated pipeline runs |
| Continuous Delivery | Jenkins + GitHub Actions | Automated Docker build + K8s deploy |
| Containerization | Docker | Dockerfile, `docker ps` output |
| Container Orchestration | Kubernetes | 7 YAML manifests in `k8s/` |
| Auto-Scaling | HPA | `hpa.yaml` (2 to 10 pods) |
| Infrastructure as Code | YAML Manifests | All K8s configs in version control |
| Static Code Analysis | SonarQube | Dashboard at localhost:9000 |
| Unit Testing | Pytest | 6 passing tests |
| Code Coverage | pytest-cov | `coverage.xml` report |
| Security Scanning | Bandit | Runs in Jenkins and GitHub Actions |
| Health Monitoring | K8s Liveness Probes | `deployment.yaml` probe config |
| Secret Management | K8s Secrets | `secret.yaml` |
| Configuration Management | K8s ConfigMaps | `configmap.yaml` |

### 12.3 Learning Outcomes

Through this project, the following practical skills were developed and demonstrated:

1. Writing production-quality Python code following PEP8 standards.
2. Designing relational database schemas for real-world e-commerce use cases.
3. Creating multi-stage Dockerfiles and understanding image layer optimization.
4. Writing Jenkins declarative pipelines with parallel stages and post-conditions.
5. Configuring GitHub Actions workflows with job dependencies and artifact sharing.
6. Understanding Kubernetes primitives: Pods, ReplicaSets, Deployments, Services, Ingress, HPAs, PVCs, ConfigMaps, and Secrets.
7. Deploying and using SonarQube for continuous inspection of code quality.
8. Writing meaningful, isolated unit tests using pytest fixtures.
9. Resolving real-world DevOps troubleshooting scenarios (port conflicts, CSRF tokens, Docker networking, PowerShell compatibility).

### 12.4 Future Enhancements

1. **Production Database:** Replace SQLite with PostgreSQL deployed as a StatefulSet in Kubernetes for true horizontal scalability.
2. **Real Payment Gateway:** Integrate Stripe or Razorpay for live payment processing.
3. **Monitoring Stack:** Add Prometheus and Grafana for real-time metric scraping and dashboarding.
4. **GitOps:** Implement ArgoCD for declarative, Git-driven Kubernetes deployments.
5. **Service Mesh:** Add Istio for traffic management, mutual TLS, and distributed tracing.
6. **CDN & Caching:** Add Redis for session caching and a CDN for static asset delivery.

---

*Report prepared for academic submission — DevOps Subject Project*
*GitHub Repository: https://github.com/Het-Shah-Rock/devops_pro*
