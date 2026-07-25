from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "bxjm9d9YZYklm1VFNSRQG0viXGRVzp+cG6Y7BxgS4+MacyKTLdPsX9LTSg6GUVhVJs/I/tX1SH4ha5qwn7BZCT7jR8mGhe4dlMW8ZENokEckTGhq3l+3AHJHkJg/o0K723lD0sXSmIwo+8Jbil8NigdB04t89/1O/w1cDnyilFU="

@app.route("/", methods=["GET"])
def home():
    return "LINE Reminder Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("=== 收到 webhook ===")
    print(data)
    
    events = data.get("events", [])
    
    for event in events:
        print("事件類型:", event.get("type"))
        print("來源:", event.get("source"))
        
        if event.get("type") == "message" and event.get("source", {}).get("type") == "group":
            group_id = event["source"]["groupId"]
            reply_token = event["replyToken"]
            print("準備回覆群組ID:", group_id)
            
            result = reply_message(reply_token, f"群組ID是：\n{group_id}\n\n請把這串ID複製起來告訴我。")
            print("回覆結果:", result)
    
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
    
    response = requests.post(url, headers=headers, json=data)
    print("LINE API 狀態碼:", response.status_code)
    print("LINE API 回應:", response.text)
    return response.status_code, response.text

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
    
    response = requests.post(url, headers=headers, json=data)
    print("推播狀態碼:", response.status_code)
    print("推播回應:", response.text)
    
    if response.status_code == 200:
        return "推播成功"
    else:
        return f"推播失敗: {response.text}", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
