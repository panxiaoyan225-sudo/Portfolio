import requests
import os
import time

# 1. CONFIGURATION
PORTFOLIO_URL = "https://xiaoyan-pan-data-analytics-portfolio-170069322954.us-west1.run.app/"
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_CHANNEL = "#portfolio"

# 2. SLACK UTILITY
def send_slack_notification(message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "channel": SLACK_CHANNEL, 
        "text": message
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        if response_json.get("ok"):
            print("🚀 Slack notification sent successfully!")
        else:
            print(f"❌ Slack Error: {response_json.get('error')}")
    except Exception as e:
        print(f"❌ Failed to connect to Slack: {e}")

# 3. WARM-UP & MONITORING LOGIC
def monitor_and_warm_portfolio():
    try:
        # Pinging the site to wake up the Cloud Run instance
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