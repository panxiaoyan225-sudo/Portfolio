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

# 3. WARM-UP LOGIC (Now returns the status instead of messaging)
def monitor_and_warm_portfolio():
    try:
        # Pinging the site to wake up the Cloud Run instance
        response = requests.get(PORTFOLIO_URL, timeout=15)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Connection Error: {e}")
        return None

# 4. EXECUTION FLOW (The "Outside" logic)
if __name__ == "__main__":
    # Perform the warm-up
    status = monitor_and_warm_portfolio()
    
    # Decide on ONE message to send based on the result
    if status == 200:
        msg = f"✅ Portfolio is warm and live. (Status: {status})"
        print(msg)
        send_slack_notification(msg) # This now runs exactly ONCE per script execution
    elif status:
        msg = f"⚠️ *Portfolio Alert*: Site returned status {status}\nURL: {PORTFOLIO_URL}"
        send_slack_notification(msg)
    else:
        msg = "🚨 *CRITICAL*: Portfolio is DOWN or unreachable!"
        send_slack_notification(msg)