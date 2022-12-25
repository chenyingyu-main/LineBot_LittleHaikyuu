import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "menu",
        "about_volley", "position", "ws", "mb", "op", "s", "l", "rules", "rotation",
        "training_and_cooldown", "physical_training", "cool_down", "tabata", "training_list", "intro_cool", "start_cool",
        "news_and_media", "volleyball_game", "volleyball_world", "vleague", "hop", "media"
    ],
    transitions=[
        # from user to menu
        {
            "trigger": "advance", "source": "user", "dest": "menu", "conditions": "is_going_to_menu",
        },
        # menu to my three main functions
        {
            "trigger": "advance", "source": "menu", "dest": "about_volley", "conditions": "is_going_to_about_volley",
        },
        {
            "trigger": "advance", "source": "menu", "dest": "training_and_cooldown", "conditions": "is_going_to_training_and_cooldown",
        },
        {
            "trigger": "advance", "source": "menu", "dest": "news_and_media", "conditions": "is_going_to_news_and_media",
        },
        # (關於排球) about volley
        {
            "trigger": "advance", "source": "about_volley", "dest": "position", "conditions": "is_going_to_position",
        },
        {
            "trigger": "advance", "source": "position", "dest": "ws", "conditions": "is_going_to_ws",
        },
        {
            "trigger": "advance", "source": "ws", "dest": "menu", "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance", "source": "ws", "dest": "position", "conditions": "is_going_to_position",
        },
        {
            "trigger": "advance", "source": "position", "dest": "mb", "conditions": "is_going_to_mb",
        },
        {
            "trigger": "advance", "source": "mb", "dest": "menu", "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance", "source": "mb", "dest": "position", "conditions": "is_going_to_position",
        },
        {
            "trigger": "advance", "source": "position", "dest": "op", "conditions": "is_going_to_op",
        },
        {
            "trigger": "advance", "source": "op", "dest": "menu", "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance", "source": "op", "dest": "position", "conditions": "is_going_to_position",
        },
        {
            "trigger": "advance", "source": "position", "dest": "s", "conditions": "is_going_to_s",
        },
        {
            "trigger": "advance", "source": "s", "dest": "menu", "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance", "source": "s", "dest": "position", "conditions": "is_going_to_position",
        },
        {
            "trigger": "advance", "source": "position", "dest": "l", "conditions": "is_going_to_l",
        },
        {
            "trigger": "advance", "source": "l", "dest": "menu", "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance", "source": "l", "dest": "position", "conditions": "is_going_to_position",
        },
        {
            "trigger": "advance", "source": "about_volley", "dest": "rules", "conditions": "is_going_to_rules",
        },
        {
            "trigger": "advance", "source": "rules", "dest": "menu", "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance", "source": "about_volley", "dest": "rotation", "conditions": "is_going_to_rotation",
        },
        {
            "trigger": "advance", "source": "rotation", "dest": "menu", "conditions": "is_going_to_menu",
        },
        # (體能與收操) training and cooldown
        {
            "trigger": "advance", "source": "training_and_cooldown", "dest": "physical_training", "conditions": "is_going_to_physical_training",
        },
        {
            "trigger": "advance", "source": "training_and_cooldown", "dest": "cool_down", "conditions": "is_going_to_cool_down",
        },
        {
            "trigger": "advance", "source": "physical_training", "dest": "tabata", "conditions": "is_going_to_tabata",
        },
        {
            "trigger": "advance", "source": "tabata", "dest": "menu", "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance", "source": "physical_training", "dest": "training_list", "conditions": "is_going_to_training_list",
        },
        {
            "trigger": "advance", "source": "training_list", "dest": "menu", "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance", "source": "cool_down", "dest": "intro_cool", "conditions": "is_going_to_intro_cool",
        },
        {
            "trigger": "advance", "source": "cool_down", "dest": "start_cool", "conditions": "is_going_to_start_cool",
        },
        {
            "trigger": "advance", "source": "intro_cool", "dest": "start_cool", "conditions": "is_going_to_start_cool",
        },
        {
            "trigger": "advance", "source": "start_cool", "dest": "menu", "conditions": "is_going_to_menu",
        },
        # (體能與收操) training and cooldown
        {
            "trigger": "advance", "source": "news_and_media", "dest": "volleyball_game", "conditions": "is_going_to_volleyball_game",
        },
        {
            "trigger": "advance", "source": "volleyball_game", "dest": "volleyball_world", "conditions": "is_going_to_volleyball_world",
        },
        {
            "trigger": "advance", "source": "volleyball_world", "dest": "menu", "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance", "source": "volleyball_world", "dest": "volleyball_game", "conditions": "is_going_to_volleyball_game",
        },
        {
            "trigger": "advance", "source": "volleyball_game", "dest": "vleague", "conditions": "is_going_to_vleague",
        },
        {
            "trigger": "advance", "source": "vleague", "dest": "menu", "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance", "source": "vleague", "dest": "volleyball_game", "conditions": "is_going_to_volleyball_game",
        },
        {
            "trigger": "advance", "source": "volleyball_game", "dest": "hop", "conditions": "is_going_to_hop",
        },
        {
            "trigger": "advance", "source": "hop", "dest": "menu", "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance", "source": "hop", "dest": "volleyball_game", "conditions": "is_going_to_volleyball_game",
        },
        {
            "trigger": "advance", "source": "news_and_media", "dest": "media", "conditions": "is_going_to_media",
        },
        {
            "trigger": "advance", "source": "media", "dest": "menu", "conditions": "is_going_to_menu",
        },
        # go_back
        {
            "trigger": "go_back", "source": ["training_and_cooldown"], "dest": "menu"
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

'''
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"
'''

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if machine.state == 'menu' and event.message.text.lower() == '主選單':
                send_text_message(event.reply_token, "您已經在主選單了")
            else:
                send_text_message(event.reply_token, "請依照按鈕指示進行操作")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
