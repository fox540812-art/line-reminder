from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN", "")

@app.route("/", methods=["GET"])
def home():
    return "LINE Reminder Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    events = data.get("events", [])
    
    for event in events:
        if event.get("type") == "message" and event.get("source", {}).get("type") == "group":
            group_id = event["source"]["groupId"]
            reply_token = event["replyToken"]
            reply_message(reply_token, f"群組ID是：\n{group_id}\n\n請把這串ID複製起來告訴我。")
    
    return jsonify({"status": "ok"})

def reply_message(reply_token, text):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(url, headers=headers, json=data)

@app.route("/push", methods=["GET"])
def push():
    group_id = request.args.get("group_id")
    if not group_id:
        return "缺少 group_id 參數", 400
    
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "to": group_id,
        "messages": [{
            "type": "text",
            "text": "📢 早安～今天要做的事情是：\n\n1. 記得開會\n2. 記得寫進度\n3. 加油！"
        }]
    }
    requests.post(url, headers=headers, json=data)
    return "推播成功"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
