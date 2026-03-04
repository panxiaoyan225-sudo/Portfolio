import requests
import os
import time
import sys


def _add_pipeline_to_path() -> None:
    """Ensure the pipeline folder (with SLACK.py) is on sys.path."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pipeline_dir = os.path.join(base_dir, "pipeline", "pipeline_py")
    if pipeline_dir not in sys.path:
        sys.path.append(pipeline_dir)


_add_pipeline_to_path()
from SLACK import send_slack_notification

# 1. CONFIGURATION
PORTFOLIO_URL = "https://xiaoyan-pan-data-analytics-portfolio-170069322954.us-west1.run.app/"


# 3. WARM-UP & MONITORING LOGIC
def monitor_and_warm_portfolio():
    try:
        # Pinging the site to wake up the Cloud Run instance
        # Send an HTTP GET request to the portfolio URL with a 15-second timeout.
        # This checks if the site is reachable and responsive (used to "warm" the Cloud Run instance).
        response = requests.get(PORTFOLIO_URL, timeout=15)
        
        # Check if the HTTP response status code is 200, which means the portfolio site is successfully reachable and live
        if response.status_code == 200:
            print(f"✅ Portfolio is warm and live. (Status: {response.status_code})")
            msg=f"✅ Portfolio is warm and live. (Status: {response.status_code})"
            send_slack_notification(msg)
        else:
            # Alert Slack if the site returns a 404, 500, or 403
            msg = f"⚠️ *Portfolio Alert*: Site returned status `{response.status_code}`\nURL: {PORTFOLIO_URL}"
            send_slack_notification(msg)
            
    except requests.exceptions.RequestException as e:
        # Alert Slack if the site is completely unreachable
        msg = f"🚨 *CRITICAL*: Portfolio is DOWN or unreachable!\nError: `{str(e)}`"
        send_slack_notification(msg)

if __name__ == "__main__":
    monitor_and_warm_portfolio()