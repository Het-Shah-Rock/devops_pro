# 🎓 DevOps Project: Technology Explanation Guide
> **Purpose:** Use this document as your "cheat sheet" or presentation script when explaining your project to your lecturer. It covers **WHAT** each technology is, **WHY** you chose it for a DevOps project, and **WHAT** was tested.

---

## 🐍 1. Python & Streamlit (The Application Layer)
**What it is:** The programming language and web framework used to build the QuickCart interface.
**Why we used it:** 
*   **Rapid Prototyping:** Streamlit allows us to build a beautiful, multi-page, data-driven web app entirely in Python without needing a separate frontend team (HTML/CSS/JS).
*   **Focus on DevOps:** By keeping the app codebase clean and in one language, we could dedicate 80% of our project time to implementing the DevOps pipeline rather than struggling with UI bugs.
**What we tested:** We tested the application's ability to handle user sessions, calculate shopping cart totals, apply coupons, and route between 7 different pages flawlessly.

---

## 🗄️ 2. SQLite (The Database Layer)
**What it is:** A serverless, file-based relational database.
**Why we used it:** 
*   **Zero-Configuration:** It provides full SQL capabilities (foreign keys, JOINs) without needing a heavy, separate database server like MySQL or PostgreSQL to be managed locally.
*   **Persistence Demo:** It perfectly demonstrates why Kubernetes needs "Persistent Volumes". If the Docker container crashes, the `quickcart.db` file is saved, proving we understand stateful applications.
**What we tested:** We wrote Pytest scripts to test database connection, schema creation (tables like `products` and `orders`), data insertion, and dynamic stock deduction when an order is placed.

---

## 🐙 3. Git & GitHub (Version Control)
**What it is:** Git tracks code changes; GitHub hosts the code in the cloud.
**Why we used it:** 
*   **The Foundation of DevOps:** DevOps cannot exist without version control. It acts as our "Single Source of Truth."
*   **Pipeline Triggering:** GitHub is where our CI/CD pipeline starts. The moment code is pushed to the `main` branch, it triggers Jenkins and GitHub Actions automatically.
**What we tested:** We tested committing code, branching, pushing to remote repositories, and integrating GitHub Webhooks/Polling to trigger external pipelines.

---

## 🐳 4. Docker (Containerization)
**What it is:** A tool that packages the app, Python, and all dependencies into a single, portable "Image."
**Why we used it:** 
*   **Solves "It works on my machine":** By containerizing QuickCart, we guarantee it will run exactly the same way on the lecturer's computer, a Linux server, or AWS, because the environment is baked into the image.
*   **Multi-Stage Builds:** We used advanced Docker techniques to drastically reduce the image size and run the app as a non-root user (`appuser`) for enterprise-grade security.
**What we tested:** We tested building the image (`docker build`), running the container locally, exposing port 8080, and verifying the `HEALTHCHECK` endpoint (`/_stcore/health`).

---

## ⚙️ 5. Jenkins (Continuous Integration / Continuous Deployment)
**What it is:** An automation server that acts as the "robot" executing our DevOps pipeline.
**Why we used it:** 
*   **Eliminates Manual Work:** Without Jenkins, a developer has to manually run tests, manually build Docker images, and manually copy code to a server. Jenkins automates this entire flow.
*   **Industry Standard:** Jenkins is the most widely used CI/CD tool in the corporate world.
**What we tested:** We wrote a `Jenkinsfile` that successfully pulls code, runs security scans (`bandit`), runs unit tests, builds the Docker image, and simulates deploying to Kubernetes.

---

## 🛡️ 6. SonarQube & Pytest (Continuous Testing & Security)
**What it is:** Pytest runs our Python unit tests. SonarQube is an enterprise tool that scans the code for quality and security issues.
**Why we used it:** 
*   **Quality Gates:** In a real company, bad code should never reach production. We use Pytest to ensure the logic works, and SonarQube to catch hidden bugs, "code smells", or OWASP security vulnerabilities (like leaked passwords).
**What we tested:** 
*   **Pytest:** 6 automated tests achieving a 100% pass rate.
*   **SonarQube:** Scanned `app.py` and `database.py`, generating a full dashboard of metrics and proving we understand "Shift-Left Security" (finding bugs early in the pipeline).

---

## ☸️ 7. Kubernetes (Container Orchestration)
**What it is:** A system that manages, scales, and heals our Docker containers in production.
**Why we used it:** 
*   Docker is great for one laptop, but if 10,000 users visit QuickCart, one Docker container will crash. Kubernetes solves this.
*   **Infrastructure as Code (IaC):** We wrote 7 YAML files defining our entire server architecture as code, so it can be deployed anywhere instantly.
**What we tested / What you should show:**
*   **`deployment.yaml`**: Proves High Availability (runs 2 replicas of the app).
*   **`hpa.yaml`**: Proves Auto-scaling (scales from 2 to 10 servers if CPU spikes).
*   **`pv-pvc.yaml`**: Proves Data Persistence (saves the SQLite database if a server crashes).
*   **`secret.yaml`**: Proves Security (injects passwords securely instead of hardcoding them).

---

## 🎯 Summary Pitch for Your Lecturer
*"Sir/Ma'am, this project is not just a Python web app. It is a fully automated, production-ready DevOps pipeline. I wrote the application code, containerized it with Docker, secured and tested it using SonarQube and Pytest, automated the entire build process with Jenkins, and wrote the Infrastructure as Code to scale it infinitely on Kubernetes. It mirrors the exact software development lifecycle used by top tech companies."*
