# 🚀 Portfolio Monitor & Auto-Warmer

An automated monitoring and orchestration pipeline using **Azure DevOps** designed to eliminate **"Cold Start"** latency on Google Cloud Run while providing real-time infrastructure alerts via Slack.

---

## 📋 Overview
This project provides a "Single Source of Truth" for infrastructure health, serving a triple purpose:
1.  **Cold Start Mitigation:** Periodically "pings" the Google Cloud Run hosted portfolio to ensure the container remains warm and responsive for visitors.
2.  **Strategic Risk Mitigation:** Automatically validates project configurations and logic before execution to eliminate human error and environment drift.
3.  **Real-time Alerting:** Dispatches status reports and performance metrics to a dedicated Slack channel.

## 🛠️ Technical Stack
* **Language:** Python 3.9
* **Cloud Provider:** Google Cloud Platform (Cloud Run)
* **Orchestration:** **Azure DevOps (Azure Pipelines)**
* **Automation:** YAML-based CI/CD Pipelines
* **Testing:** Pytest (Logic & Config Validation)
* **Communication:** Slack API (WebClient/Webhooks)

---

## ⚙️ Architecture & Automation

### 1. Cloud-Native Orchestration (Azure Pipelines)
The project has migrated from local Windows Task Scheduling to a fully containerized **Azure DevOps** workflow. This ensures 100% environment consistency:
* **Scheduled Heartbeat:** Controlled via `cron` schedules within `azure-pipelines.yml`, keeping the Cloud Run instance active without manual intervention.
* **Automated Validation:** Includes a dedicated `Validate Logic & Config` stage using `pytest` to verify Slack Webhooks and ticker lists before the main monitor runs.
* **Secret Management:** Sensitive tokens are injected via Azure Pipeline environment variables (`SLACK_WEBHOOK_URL`), removing the risk of hardcoded credentials.

### 2. The Slack Integration
The system integrates with a custom Slack App to provide immediate transparency into the pipeline's health.
* **Automated Feedback:** Provides immediate visual confirmation (e.g., ✅ status) upon successful pings or failure alerts for immediate troubleshooting.
* **Error Trapping:** If the validation scripts detect a configuration error, the pipeline halts immediately and notifies the owner, preventing "silent failures."

---

## 🚀 Installation & Setup

### Azure DevOps Configuration
1.  **Pipeline Import:** Create a new pipeline in Azure DevOps pointing to this repository.
2.  **Variables:** Define the following secret variable in your **Azure Pipeline Library** or Variable Group:
    * `SLACK_WEBHOOK`: Your unique Slack Webhook URL.
3.  **Deployment:** The `azure-pipelines.yml` handles the environment setup (`Python 3.9`), dependency installation, and execution.

### Local Development & Testing
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Validation Suite
python -m pytest tests/test_config.py

# Run Monitor Manually
python monitor_portfolio