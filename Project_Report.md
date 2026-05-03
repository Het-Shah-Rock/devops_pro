# Project Report: QuickCart - Enterprise Quick Commerce Platform

## 1. Project Overview

**QuickCart** is a comprehensive, enterprise-grade Quick Commerce application built to demonstrate a modern software development lifecycle (SDLC) and advanced DevOps practices. It simulates a 10-minute grocery delivery platform, similar to Blinkit or Zepto, featuring a multi-page web interface, a robust relational database backend, and a full suite of DevOps technologies for Continuous Integration, Continuous Deployment (CI/CD), containerization, and orchestration.

### 1.1 Objectives
*   **Application Development:** Build a functional, multi-page Python web application with user authentication, a product catalog, a shopping cart, order processing, and an admin dashboard.
*   **Database Integration:** Implement a persistent relational database (SQLite) to manage users, products, coupons, and orders.
*   **Containerization:** Package the application using Docker with multi-stage builds for security and efficiency.
*   **CI/CD Pipeline:** Automate testing, security scanning, and deployment using Jenkins and GitHub Actions.
*   **Orchestration:** Deploy the containerized application to Kubernetes (K8s) with high availability, auto-scaling, and persistent storage.
*   **Observability & DevOps Showcase:** Provide a dedicated "DevOps Control Center" within the app to visualize the underlying infrastructure and deployment health.

---

## 2. Technology Stack

### 2.1 Application Layer
*   **Language:** Python 3.10
*   **Frontend/Framework:** Streamlit (Multi-page architecture)
*   **Data Handling:** Pandas
*   **Database:** SQLite3

### 2.2 DevOps & Infrastructure Layer
*   **Version Control:** Git & GitHub
*   **Containerization:** Docker & Docker Compose
*   **CI/CD Automation:** Jenkins (Declarative Pipeline) & GitHub Actions
*   **Orchestration:** Kubernetes (Deployments, Services, ConfigMaps, Secrets, PVCs, Ingress, HPA)
*   **Testing & Security:** Pytest (Unit Testing), Flake8 (Linting), Bandit (SAST/Security Scanning)

---

## 3. Application Architecture

The application is structured using a modular, multi-page approach:

*   **`app.py` (Storefront):** The main landing page featuring a hero banner, category filters, a dynamic product grid, and hot deals.
*   **`pages/1_Cart.py`:** Manages the shopping cart, calculates totals, applies coupon codes, captures delivery addresses, and processes checkouts.
*   **`pages/2_Order_Confirmation.py`:** A post-checkout success page featuring an animated order tracking timeline and an itemized receipt.
*   **`pages/3_Deals_and_Offers.py`:** A dedicated section highlighting discounted products and active coupon codes.
*   **`pages/4_Order_History.py`:** Allows authenticated users to view past orders, track current status, and utilize a "Reorder" function.
*   **`pages/5_Profile.py`:** User profile management for updating contact and delivery details.
*   **`pages/6_Admin_Dashboard.py`:** A secure, tabbed interface for administrators to view revenue analytics, manage inventory (restock), update order statuses, and generate new coupons.
*   **`pages/0_DevOps_Control_Center.py`:** A unique, educational dashboard that visualizes the active CI/CD pipelines, Kubernetes resource health, environment variables, and live application metrics.

### 3.1 Database Schema (`database.py` & `seed.py`)
The SQLite database consists of interconnected tables:
1.  **`users`**: Stores user profiles and authentication details.
2.  **`products`**: A catalog of 37 seeded products with categories, stock levels, pricing, MRP, and ratings.
3.  **`orders` & `order_items`**: Tracks customer transactions, applied discounts, and specific items purchased to enable dynamic stock deduction.
4.  **`coupons`**: Manages discount codes, minimum order requirements, and usage limits.
5.  **`reviews`**: Schema prepared for product feedback.

---

## 4. DevOps Implementation

This project heavily emphasizes production-ready DevOps methodologies.

### 4.1 Containerization (Docker)
*   **Multi-Stage Build (`Dockerfile`):** The Dockerfile uses a `builder` stage to install dependencies and a minimal final stage to run the app. This reduces the image size by over 70%, improving deployment speed and reducing the attack surface.
*   **Security:** The application runs as a non-root user (`appuser`) inside the container.
*   **Health Checks:** A native `HEALTHCHECK` directive polls the `/_stcore/health` endpoint to ensure the container is functioning.
*   **Docker Compose (`docker-compose.yml`):** Facilitates local development by orchestrating the build and port mapping (`8080:8501`) with a single command (`docker-compose up`).

### 4.2 Continuous Integration & Continuous Deployment (CI/CD)
Two distinct pipelines were created to demonstrate flexibility:

1.  **Jenkins Pipeline (`Jenkinsfile`):**
    *   Utilizes a Docker Agent (`python:3.10-slim`) to run jobs in isolated environments.
    *   Executes parallel stages for Linting (`flake8`) and Static Application Security Testing (`bandit`).
    *   Builds and tags the Docker image, pushing it to DockerHub.
    *   Contains instructions for declarative Kubernetes rolling deployments.

2.  **GitHub Actions (`.github/workflows/ci-cd.yml`):**
    *   Triggered on `push` and `pull_request` to `main`.
    *   Runs Unit Tests using `pytest` against an in-memory test database, ensuring code integrity before deployment.
    *   Automatically builds multi-platform Docker images and pushes them to the container registry.
    *   Simulates the `kubectl apply` commands for production rollout.

### 4.3 Kubernetes Orchestration (`k8s/`)
The application is designed to run in a highly available Kubernetes cluster.

*   **Deployment (`deployment.yaml`):** Manages ReplicaSets (defaulting to 2 replicas) for high availability. Includes resource limits/requests and liveness probes.
*   **Service (`service.yaml`):** Exposes the deployment internally via a LoadBalancer/ClusterIP.
*   **Ingress (`ingress.yaml`):** Configures NGINX routing for the domain `quickcart.local` to handle external HTTP traffic.
*   **State Management (`pv-pvc.yaml`):** Defines a PersistentVolumeClaim so the SQLite database (`quickcart.db`) survives pod restarts and scaling events.
*   **Configuration Management (`configmap.yaml` & `secret.yaml`):** Demonstrates the "12-Factor App" methodology by injecting environment variables (`APP_ENV`, `DB_PATH`) and secure keys (`API_KEY`) into the pods rather than hardcoding them.
*   **Auto-scaling (`hpa.yaml`):** A HorizontalPodAutoscaler monitors CPU and memory utilization, automatically scaling the application from 2 up to 10 pods during traffic spikes.

### 4.4 Automated Testing
*   **Unit Tests (`tests/test_database.py`):** 6 automated tests verify database connection, schema creation, data insertion, order processing, and dynamic stock deduction.

---

## 5. Conclusion & Future Enhancements

The QuickCart project successfully integrates a feature-rich Python application with a modern DevOps pipeline. It serves as a comprehensive showcase of CI/CD, Infrastructure as Code (YAML), and container orchestration. 

**Potential Future Enhancements:**
1.  Migrating from SQLite to a distributed database like PostgreSQL or MongoDB for true horizontal scalability.
2.  Integrating a real payment gateway (e.g., Stripe or Razorpay).
3.  Adding Prometheus and Grafana for advanced metric scraping and dashboarding.
4.  Implementing ArgoCD for a true GitOps-based Kubernetes deployment strategy.
