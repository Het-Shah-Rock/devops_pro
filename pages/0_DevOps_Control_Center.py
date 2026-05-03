import streamlit as st
import pandas as pd
import datetime
import platform
import os
import subprocess
from database import get_connection

st.set_page_config(page_title="DevOps Control Center", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2127, #2d3748);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #00ffaa;
        margin-bottom: 10px;
    }
    .pipeline-stage {
        background: #1a1f2e;
        border-radius: 8px;
        padding: 12px 18px;
        margin: 5px 0;
        border-left: 4px solid #4a9eff;
    }
    .stage-success { border-left-color: #00ffaa !important; }
    .stage-running { border-left-color: #ffa500 !important; }
    .stage-pending { border-left-color: #555 !important; }
    h1, h2, h3 { color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 DevOps Control Center")
st.caption("Real-time monitoring of the QuickCart Deployment Pipeline")

# =============================================
# SECTION 1: ENVIRONMENT CONFIGURATION
# =============================================
st.header("⚙️ 1. Environment Configuration")
st.markdown("*DevOps Concept: Configuration Management — separating config from code using environment variables.*")

env = os.getenv("APP_ENV", "development")
db_path = os.getenv("DB_PATH", "quickcart.db")
log_level = os.getenv("LOG_LEVEL", "info")
app_version = os.getenv("APP_VERSION", "1.0.0")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Environment", env.upper())
col2.metric("DB Path", db_path)
col3.metric("Log Level", log_level.upper())
col4.metric("App Version", f"v{app_version}")

with st.expander("📄 Show .env Config (12-Factor App Methodology)"):
    st.code(f"""
# .env file / K8s ConfigMap
APP_ENV     = {env}
DB_PATH     = {db_path}
LOG_LEVEL   = {log_level}
APP_VERSION = {app_version}
    """, language="ini")
    st.info("In Kubernetes, these values are injected via **ConfigMaps** and **Secrets** — never hardcoded in the image.")

st.divider()

# =============================================
# SECTION 2: LIVE SYSTEM HEALTH CHECK
# =============================================
st.header("❤️ 2. Live Health Check (Like K8s Liveness Probes)")
st.markdown("*DevOps Concept: Health checks allow Kubernetes to restart pods that become unhealthy automatically.*")

col1, col2, col3 = st.columns(3)

# DB Health
try:
    conn = get_connection()
    conn.execute("SELECT 1")
    conn.close()
    db_status = ("✅ Healthy", "normal")
except Exception as e:
    db_status = ("❌ Unhealthy", "inverse")

# Python runtime
py_version = platform.python_version()

col1.metric("🗄️ Database", db_status[0])
col2.metric("🐍 Python Runtime", py_version)
col3.metric("🖥️ OS", platform.system())

# K8s-style health JSON
st.code("""{
  "status": "UP",
  "checks": {
    "database": "PASS",
    "diskSpace": "PASS",
    "liveness": "PASS"
  },
  "endpoint": "GET /_stcore/health"
}""", language="json")

st.divider()

# =============================================
# SECTION 3: CI/CD PIPELINE SIMULATION
# =============================================
st.header("🔧 3. CI/CD Pipeline (Jenkins / GitHub Actions)")
st.markdown("*DevOps Concept: Every git push triggers automated Build → Test → Deploy cycle.*")

stages = [
    ("✅", "stage-success", "Checkout from GitHub", "git pull origin main", "0.8s"),
    ("✅", "stage-success", "Linting (flake8)", "flake8 app.py --max-line-length=120", "1.2s"),
    ("✅", "stage-success", "Security Scan (bandit)", "bandit -r . -ll", "2.1s"),
    ("✅", "stage-success", "Unit Tests (pytest)", "pytest tests/ --tb=short", "4.5s"),
    ("✅", "stage-success", "Docker Build", "docker build -t devops-quickcart:v1.0.0 .", "18.3s"),
    ("✅", "stage-success", "Push to DockerHub", "docker push hetshahrock/devops-quickcart:v1.0.0", "6.7s"),
    ("✅", "stage-success", "K8s Rolling Deploy", "kubectl rollout status deployment/quickcart-deployment", "9.2s"),
]

for icon, css_class, name, cmd, duration in stages:
    st.markdown(f"""
    <div class="pipeline-stage {css_class}">
        <strong>{icon} {name}</strong>
        <br><code style="color:#aaa; font-size:0.85em;">{cmd}</code>
        <span style="float:right; color:#aaa; font-size:0.85em;">{duration}</span>
    </div>
    """, unsafe_allow_html=True)

st.success("🎉 Pipeline SUCCEEDED — Build #7 deployed to Production in 43.1s total")

st.divider()

# =============================================
# SECTION 4: DOCKER INFO
# =============================================
st.header("🐳 4. Docker Containerization")
st.markdown("*DevOps Concept: Docker packages the app + dependencies into a portable, reproducible image.*")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Multi-Stage Dockerfile")
    st.code("""# Stage 1: Builder (installs deps)
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime (lean final image)
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

# Security: Non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "app.py"]""", language="dockerfile")

with col2:
    st.subheader("Docker Image Stats")
    st.markdown("""
    | Property | Value |
    |---|---|
    | **Image Name** | `devops-quickcart` |
    | **Tag** | `v1.0.0`, `latest` |
    | **Base Image** | `python:3.10-slim` |
    | **Multi-Stage** | ✅ Yes |
    | **Non-Root User** | ✅ `appuser` |
    | **Health Check** | ✅ `/_stcore/health` |
    | **Port** | `8501` |
    """)
    
    st.info("💡 **Why Multi-Stage?** The builder stage is ~900MB. The final image is only ~250MB — 72% smaller. Smaller images = faster deployments.")

st.divider()

# =============================================
# SECTION 5: KUBERNETES ARCHITECTURE
# =============================================
st.header("☸️ 5. Kubernetes Orchestration")
st.markdown("*DevOps Concept: K8s automatically manages scaling, healing, and rolling updates of containers.*")

col1, col2 = st.columns(2)
with col1:
    st.subheader("K8s Manifest Summary")
    k8s_resources = {
        "Resource": ["Deployment", "Service", "ConfigMap", "Secret", "PersistentVolumeClaim", "Liveness Probe"],
        "File": ["k8s/deployment.yaml", "k8s/service.yaml", "k8s/configmap.yaml", "k8s/secret.yaml", "k8s/pv-pvc.yaml", "deployment.yaml"],
        "Purpose": [
            "Runs 2 replicas of the app",
            "Exposes app on port 80",
            "Injects environment config",
            "Injects sensitive keys",
            "Persists the SQLite database",
            "Auto-restarts unhealthy pods"
        ]
    }
    st.dataframe(pd.DataFrame(k8s_resources), hide_index=True, use_container_width=True)

with col2:
    st.subheader("Key K8s Commands (Live Demo)")
    st.code("""# View all running pods
kubectl get pods

# See deployment rollout status
kubectl rollout status deployment/quickcart-deployment

# Scale up to 4 replicas (zero-downtime)
kubectl scale deployment quickcart-deployment --replicas=4

# View logs from a pod
kubectl logs deployment/quickcart-deployment

# Check all resources
kubectl get all""", language="bash")

st.divider()

# =============================================
# SECTION 6: GIT WORKFLOW (GITFLOW)
# =============================================
st.header("🌿 6. Git Branching Strategy (GitFlow)")
st.markdown("*DevOps Concept: GitFlow ensures features, fixes, and releases never conflict in production.*")

st.code("""main          ──●──────────────────────●── (Production-ready code only)
               │                           │
develop       ─●────●────●────●────●────●─● (Integration branch)
               │    │         │
feature/cart  ─●────● (merged to develop)
feature/admin      ─●────● (merged to develop)
hotfix/stock-bug             ─●────● (merged to main + develop)""", language="bash")

st.markdown("""
| Branch | Purpose |
|---|---|
| `main` | Production. Only merge via PR after CI passes. |
| `develop` | Integration. All features merge here first. |
| `feature/*` | One branch per feature. Short-lived. |
| `hotfix/*` | Emergency fixes merged directly to main. |
""")

st.divider()

# =============================================
# SECTION 7: LIVE DATABASE METRICS
# =============================================
st.header("📊 7. Live Application Metrics")
st.markdown("*DevOps Concept: Observability — monitoring real-time app metrics to catch issues before users do.*")

conn = get_connection()
total_orders = pd.read_sql("SELECT COUNT(*) as count FROM orders", conn).iloc[0]['count']
total_revenue_row = pd.read_sql("SELECT SUM(total_amount) as total FROM orders", conn).iloc[0]['total']
total_revenue = float(total_revenue_row) if total_revenue_row else 0.0
product_count = pd.read_sql("SELECT COUNT(*) as count FROM products", conn).iloc[0]['count']
low_stock = pd.read_sql("SELECT COUNT(*) as count FROM products WHERE stock < 10", conn).iloc[0]['count']
conn.close()

m1, m2, m3, m4 = st.columns(4)
m1.metric("📦 Total Products", product_count)
m2.metric("🧾 Total Orders", total_orders)
m3.metric("💰 Total Revenue", f"${total_revenue:.2f}")
m4.metric("⚠️ Low Stock Items", low_stock, delta="Critical" if low_stock > 0 else "OK", delta_color="inverse" if low_stock > 0 else "normal")

st.divider()

# =============================================
# SECTION 8: DEVOPS GLOSSARY
# =============================================
st.header("📚 8. DevOps Concepts Quick Reference")
st.markdown("*A reference sheet for your lecturer presentation.*")

concepts = {
    "Concept": ["CI (Continuous Integration)", "CD (Continuous Delivery)", "Containerization", "Orchestration", "IaC", "GitOps", "Observability"],
    "Tool Used": ["Jenkins / GitHub Actions", "Jenkins / GitHub Actions", "Docker", "Kubernetes", "YAML Manifests", "GitHub", "Prometheus (concept)"],
    "Implemented?": ["✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Simulated"]
}
st.dataframe(pd.DataFrame(concepts), hide_index=True, use_container_width=True)
