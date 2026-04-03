# Portfolio Monitor & Auto-Warmer

Production-grade CI/CD pipeline with triple-platform orchestration (GitHub Actions, Azure DevOps, and GitHub Repos) handling automated "heartbeat" runs, real-time anomaly detection, and seamless ETL syncing.

## 🎯 Project Philosophy

Most modern cloud-native applications suffer from "Cold Start" latency on serverless platforms. This project demonstrates a **high-performance, low-footprint architecture** optimized for Google Cloud Run.

## 🏗️ System Architecture

### **Architecture Diagram**

```mermaid
graph TD
    subgraph "Orchestration Layer"
        GH[GitHub Actions] -- cron/push --> Runner[Self-Hosted Windows Agent]
        ADO[Azure DevOps Pipelines] -- cron/push --> Runner
    end

    subgraph "Validation & Security"
        Runner --> Env[Python 3.12 / UTF-8 Environment]
        Secrets1[(Azure Variable Groups)] -.-> Runner
        Secrets2[(GitHub Secrets)] -.-> Runner
        Runner --> Gate{Fail-Fast Logic Gate}
    end

    subgraph "Execution & Delivery"
        Gate -- Success --> Warm[HTTP Warmer / Health Check]
        Warm -- Ping --> GCR[Google Cloud Run Portfolio]
        GCR -- Status 200 --> Notify[Slack API Notification]
        Gate -- Failure --> Alert[Real-time Error Alert]
        Alert --> Notify
    end

    style GCR fill:#4285F4,color:#fff
    style Notify fill:#4A154B,color:#fff
    style Gate fill:#f96,stroke:#333

The framework orchestrates infrastructure health through five specialized layers:

1. **Ingestion Layer:** Multi-channel ingestion supporting **GitHub**, **GitHub Actions**, and **Azure DevOps Repos**. Any `git push` to either origin triggers a parallel automated workflow.
2. **Validation Layer (The Gatekeeper):** A "Fail-Fast" pre-check stage that validates environment variables (e.g., `SLACK_TOKEN`) and performs syntax compilation before script execution.
3. **Environment Sync:** Automated dependency management and Python 3.12 configuration with native UTF-8 support for cross-platform log compatibility.
4. **Persistence Layer:** Secure management of sensitive API tokens using Azure DevOps Variable Groups (`Portfolio-Secrets`) and GitHub Actions Secrets.
5. **Audit & Alerting:** A Slack-integrated monitoring system that detects performance anomalies and pushes real-time status notifications.

## 🔄 The Pipelines

* **Continuous Integration (CI):** Configured to trigger automatically on every `git push` to the `main` branch. This ensures that any code changes are immediately validated and tested on the local agent.
* **Dual-Cloud Scheduling:** * **Azure Pipelines:** YAML-based `cron` schedule for a 07:00 AM EST "Morning Warm-up."
    * **GitHub Actions:** Redundant `cron` schedule to ensure high availability and environment stability even during platform outages.
* **Fail-Fast Validation:** Every run begins with a logic gate that ensures credentials are live and the Python code is syntactically sound, preventing "silent failures" in production.
* **Self-Hosted Execution:** Powered by a local Windows agent to ensure zero-cost execution without cloud parallelism or execution time restrictions.

## 🛠️ Technical Stack

* **Repositories:** GitHub (Mirror/CI) & Azure DevOps Repos (Primary/CI)
* **Cloud Provider:** Google Cloud Platform (Cloud Run)
* **Orchestration:** Azure Pipelines & GitHub Actions
* **Agent Infrastructure:** Self-Hosted Windows Agent (PowerShell/CMD)
* **Automation:** Python 3.12 & YAML-based CI/CD
* **Monitoring:** Slack API (Webhooks), Requests, aiosmtplib

---

## 🚀 Installation & Setup

### Platform Configuration
1. **Azure DevOps:** * Download and configure a self-hosted agent in the `MyLocalLaptop` pool.
    * Map your `SLACK_TOKEN` in a Variable Group named `Portfolio-Secrets`.
2. **GitHub Actions:**
    * Configure a local runner with the `self-hosted` tag.
    * Add your `SLACK_TOKEN` to **Settings > Secrets and variables > Actions**.

### Local Development & Testing
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run Validation & Monitor Manually
set PYTHONUTF8=1
python -m py_compile monitor_portfolio.py
python monitor_portfolio.py