from flask import Flask, request, abort 
# 代表著從flask這個module中引入Flask, request, abort
# REF:https://github.com/twtrubiks/python-notes/tree/master/configparser_tutorial
# import configparser
# config = configparser.ConfigParser()
# config.read("config.ini")
import os
import sys
from dotenv import load_dotenv
load_dotenv()

# from secret_settings import *

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
# line_bot_api = LineBotApi(config['DEFAULT']['LINE_CHANNEL_ACCESS_TOKEN']) # 貼上你的line bot channel token
# handler = WebhookHandler(config['DEFAULT']['LINE_CHANNEL_SECRET'])
@app.route("/", methods=['GET'])
def hello_world():
		# 有人觸發了 / 這個路徑的時候就會呼叫此function並且執行
    return 'Hello World!'

# 此為 Webhook callback endpoint
@app.route("/callback", methods=['POST']) # 代表我們宣告了/callback這個路徑 只要有人訪問這個路徑系統就會進行處理
def callback():
    # get X-Line-Signature header value
    handler.handle(body, signature)

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print("Hello world")
        # print(f"\nFSM STATE: {machine.state}")
        # print(f"REQUEST BODY: \n{body}")
        # response = machine.advance(event)
        # if response == False:
        #     send_text_message(event.reply_token, "Not Entering any State")
    return 'OK'

# decorator 負責判斷 event 為 MessageEvent 實例，event.message 為 TextMessage 實例。所以此為處理 TextMessage 的 handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 決定要回傳什麼 Component 到 Channel
    # ref:https://github.com/line/line-bot-sdk-python#linebotapi
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
    # port = os.environ.get("PORT", 8000)
    # app.run(host="0.0.0.0", port=port, debug=True)