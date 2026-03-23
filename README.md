# Portfolio Monitor & Auto-Warmer

Production-grade CI/CD pipeline with dual-platform triggers (GitHub/Azure DevOps) handling automated monthly "heartbeat" runs, real-time anomaly detection, and seamless ETL syncing.

## 🎯 Project Philosophy

Most modern cloud-native applications suffer from "Cold Start" latency on serverless platforms. This project demonstrates a **high-performance, low-footprint architecture** optimized for Google Cloud Run. By transitioning from Microsoft-hosted agents to a **Self-Hosted Windows Agent**, I bypassed environment concurrency limits while maintaining a production-grade CI/CD lifecycle.

## 🏗️ System Architecture

The framework orchestrates infrastructure health through five specialized layers:

1.  **Ingestion Layer:** Multi-channel ingestion supporting both **GitHub** and **Azure DevOps Repos**. Any `git push` to either origin triggers the automated workflow.
2.  **Validation Layer (The Gatekeeper):** A "Fail-Fast" pre-check stage that validates environment variables (e.g., `SLACK_TOKEN`) and performs syntax compilation before script execution.
3.  **Environment Sync:** Automated dependency management and Python 3.11 configuration with native UTF-8 support for cross-platform log compatibility.
4.  **Persistence Layer:** Secure management of sensitive API tokens and URLs using Azure DevOps Variable Groups (`Portfolio-Secrets`).
5.  **Audit & Alerting:** A Slack-integrated monitoring system that detects performance anomalies and pushes real-time status notifications.

## 🔄 The Pipelines

* **Continuous Integration (CI):** Configured to trigger automatically on every `git push` to the `main` branch. This ensures that any code changes are immediately validated and tested on the local agent.
* **Scheduled Maintenance:** A YAML-based `cron` schedule dispatches a "Heartbeat" run on the 1st of every month at midnight to ensure long-term environment stability.
* **Fail-Fast Validation:** Every run begins with a logic gate that ensures credentials are live and the Python code is syntactically sound, preventing "silent failures" in production.
* **Self-Hosted Execution:** Powered by a local Windows agent (**PANPAN**) to ensure zero-cost execution without cloud parallelism restrictions.

## 🛠️ Technical Stack

* **Repositories:** GitHub (Mirror) & Azure DevOps Repos (Primary)
* **Cloud Provider:** Google Cloud Platform (Cloud Run)
* **Orchestration:** Azure DevOps (Azure Pipelines)
* **Agent Infrastructure:** Self-Hosted Windows Agent (PowerShell/CMD)S
* **Automation:** Python 3.11 & YAML-based CI/CD
* **Monitoring:** Slack API (Webhooks), Requests, aiosmtplib

---

## 🚀 Installation & Setup

### Azure DevOps Configuration
1.  **Agent Setup:** Download and configure a self-hosted agent in the `MyLocalLaptop` pool.
2.  **Trigger Setup:** Ensure the `azure-pipelines.yml` includes the `trigger: [main]` block to enable CI from code pushes.
3.  **Variable Group:** Create a group named `Portfolio-Secrets` and map your `SLACK_TOKEN`.
4.  **Execution:** The pipeline handles Windows-specific dependency installation and UTF-8 environment setup automatically.

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
