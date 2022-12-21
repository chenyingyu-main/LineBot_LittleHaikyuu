import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from transitions.extensions import GraphMachine
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction
from utils import send_text_message
import message_template

channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # is going to
    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "主選單"

    def is_going_to_training_and_cooldown(self, event):
        text = event.message.text
        return text.lower() == "體能與收操"

    def is_going_to_physical_training(self, event):
        text = event.message.text
        return text.lower() == "球員體能訓練"

    def is_going_to_cool_down(self, event):
        text = event.message.text
        return text.lower() == "收操很重要"

    def is_going_to_tabata(self, event):
        text = event.message.text
        return text == "TABATA" or text == "tabata" or text == "Tabata" or text == "塔巴塔"
    
    def is_going_to_training_list(self, event):
        text = event.message.text
        return text == "排球體能菜單"

    def is_going_to_intro_cool(self, event):
        text = event.message.text
        return text == "收操小科普"

    def is_going_to_start_cool(self, event):
        text = event.message.text
        return text == "開始收操"
    
    def is_going_to_about_volley(self, event):
        text = event.message.text
        return text.lower() == "關於排球"

    # on state
    def on_enter_menu(self, event):
        print("I'm now in menu")

        reply_token = event.reply_token
        message = message_template.main_menu
        message_to_reply = FlexSendMessage("主選單", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_training_and_cooldown(self, event):
        print("I'm entering 體能與收操(training_and_cooldown)")

        reply_token = event.reply_token
        message = message_template.train_btn
        message_to_reply = FlexSendMessage("體能與收操_兩個按鈕", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_physical_training(self, event):
        print("I'm entering 體能(physical_training)")

        reply_token = event.reply_token
        quick_message = TextSendMessage(text="請於聊天室回覆『TABATA』(塔巴塔) 或 『排球體能菜單』，或使用以下快捷按鈕 \U0001F609", 
                                        quick_reply=QuickReply(items=[
                                            QuickReplyButton(action=MessageAction(label="TABATA", text="TABATA")),
                                            QuickReplyButton(action=MessageAction(label="排球體能菜單", text="排球體能菜單"))
                                        ]))
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, quick_message)

    def on_enter_cool_down(self, event):
        print("I'm entering 收操(cooldown)")

        reply_token = event.reply_token
        quick_message = TextSendMessage(text="關於收操⋯⋯ \n\n\U0001F632 還不是很瞭解的人，請在聊天室回覆『收操小科普』。\n\n\U0001F60E 如果已經充分理解的人，可以直接回覆『開始收操』進行收操呦！\n\n\n\U00002705 也可以直接使用快捷按鈕", 
                                        quick_reply=QuickReply(items=[
                                            QuickReplyButton(action=MessageAction(label="收操小科普", text="收操小科普")),
                                            QuickReplyButton(action=MessageAction(label="開始收操", text="開始收操"))
                                        ]))
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, quick_message)

    def on_enter_tabata(self, event):
        print("I'm entering 塔巴塔TABATA")

        reply_token = event.reply_token
        message = message_template.tabata
        message_to_reply = FlexSendMessage("塔巴塔", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_training_list(self, event):
        print("I'm entering 排球體能菜單 *3 list ")

        reply_token = event.reply_token
        message = message_template.training_3
        message_to_reply = FlexSendMessage("排球體能菜單", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_intro_cool(self, event):
        print("I'm entering 收操介紹 introl_cool ")

        reply_token = event.reply_token
        message = message_template.cool_intro
        message_to_reply = FlexSendMessage("收操介紹", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_start_cool(self, event):
        print("I'm entering 開始收操 start_cool")

        reply_token = event.reply_token
        message = message_template.do_cool_down
        message_to_reply = FlexSendMessage("開始收操", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_about_volley(self, event):
        print("I'm entering 關於排球  about volley")

        


