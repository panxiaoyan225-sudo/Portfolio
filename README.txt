# Portfolio Monitor & Auto-Warmer

An automated monitoring pipeline designed to solve the **"Cold Start"** latency issue on Google Cloud Run while providing real-time infrastructure alerts via Slack.

---

## 📋 Overview
This project serves a dual purpose:
1. **Cold Start Mitigation:** Periodically "pings" the Google Cloud Run hosted portfolio to ensure the container remains warm and responsive for visitors.
2. **Infrastructure Auditing:** Automatically checks the health of the live URL and logs performance metrics.
3. **Real-time Alerting:** Dispatches status reports to a dedicated Slack channel (`#portfolio`) using a custom Slack App (**Data Auditor**).

## 🛠️ Technical Stack
* **Language:** Python 3.x
* **Cloud Provider:** Google Cloud Platform (Cloud Run)
* **Automation:** Windows Task Scheduler + Batch Scripting
* **Communication:** Slack API (WebClient)
* **Environment Management:** Python Virtual Environments (venv)

---

## ⚙️ Architecture & Automation

### 1. The Local-to-Cloud Heartbeat
To maintain high availability without the cost of a "Minimum Instance" on Google Cloud, this project utilizes a local automation engine:
* **Batch Execution:** A Windows Batch file (`monitor.bat`) manages the environment activation and script execution.
* **Windows Task Scheduler:** Triggers the heartbeat at scheduled intervals. This ensures the Cloud Run instance never "scales to zero," providing a fast experience for stakeholders.

### 2. The Slack Integration
The system integrates with the Slack API to provide transparency into the pipeline's health.
* **Security Model:** Uses a "Need-to-Know" protocol where the Bot User must be explicitly invited to the `#portfolio` channel to grant it permission to post.
* **Automated Feedback:** Provides immediate visual confirmation (e.g., ✅ status) upon successful pings.



---

## 🚀 Installation & Setup

### Configuration
1. **Virtual Environment:**
   ```bash
   python -m venv venv
   call venv\Scripts\activate
   pip install -r requirements.txt