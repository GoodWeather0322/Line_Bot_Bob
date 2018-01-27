from flask import Flask, request, abort

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

line_bot_api = LineBotApi('8SkjJ6hELMBB5b2nKctz47GWyUEOKCLUgmYPNwN/9QYJNiSm8HNW3uWTiFYaBYwrRXm12YKciXkpdfGk27b3seeC/+d9DH4+JlRho1uVM2x100yRbclx1FInKEtNWy/bY4kgqtuhD3mYLmQL5i9ltgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7d092321365ffda93aa4867808e96e34')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()