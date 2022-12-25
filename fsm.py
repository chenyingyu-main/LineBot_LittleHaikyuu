import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from transitions.extensions import GraphMachine
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from utils import send_text_message
import message_template.message_template as message_template
import message_template.player_intro as player_intro
import web_crawler.wiki_crawler_soup as soup
import web_crawler.yt_crawler_selenium as sele

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

    def is_going_to_news_and_media(self, event):
        text = event.message.text
        return text.lower() == "時事收集與媒體"

    def is_going_to_position(self, event):
        text = event.message.text
        return text.lower() == "球員站位與介紹"

    def is_going_to_ws(self, event):
        text = event.message.text
        return text == "Wing Spiker"

    def is_going_to_mb(self, event):
        text = event.message.text
        return text == "Middle Blocker"
    
    def is_going_to_op(self, event):
        text = event.message.text
        return text == "Opposite"

    def is_going_to_s(self, event):
        text = event.message.text
        return text == "Setter"

    def is_going_to_l(self, event):
        text = event.message.text
        return text == "Libero"
    
    def is_going_to_rules(self, event):
        text = event.message.text
        return text.lower() == "比賽規則"

    def is_going_to_rotation(self, event):
        text = event.message.text
        return text.lower() == "輪轉規則"

    def is_going_to_volleyball_game(self, event):
        text = event.message.text
        return text.lower() == "排球比賽"

    def is_going_to_volleyball_world(self, event):
        text = event.message.text
        return text == "Volleyball World"

    def is_going_to_vleague(self, event):
        text = event.message.text
        return text == "V.LEAGUE"

    def is_going_to_hop(self, event):
        text = event.message.text
        return text == "HOP Sports"
    
    def is_going_to_media(self, event):
        text = event.message.text
        return text == "排球推薦帳號"

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
        audio_message = AudioSendMessage(
            original_content_url="https://od.lk/s/NzlfMzEwNDE4MjVf/TABATA%20%28FULL%20BODY%E2%80%94LEVEL%20BEGINNER%29.mp3",
            duration=259000
        )
        message_to_reply = FlexSendMessage("塔巴塔", message)
        mes = [message_to_reply, audio_message]
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, mes)

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
        reply_token = event.reply_token
        message = message_template.about_volley
        message_to_reply = FlexSendMessage("時事收集與媒體", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply) 

    def on_enter_news_and_media(self, event):
        print("I'm entering news_and_media 時事收集與媒體")  
        reply_token = event.reply_token
        message = message_template.news_and_media
        message_to_reply = FlexSendMessage("時事收集與媒體", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)
        # message of "排球比賽" and "排球推薦帳號"

    def on_enter_position(self, event):
        print("I'm entering position 站位")
        reply_token = event.reply_token
        imagemap = ImagemapSendMessage(
            base_url='https://i.imgur.com/wa9rgBv.jpg',
            alt_text='this is a image map of 小排球佔位',
            base_size=BaseSize(width=1040, height=1040),
            actions=[
                MessageImagemapAction(
                    text="Opposite",
                    area=ImagemapArea(x=160, y=185, height=220, width=220)
                ),
                MessageImagemapAction(
                    text="Middle Blocker",
                    area=ImagemapArea(x=405, y=185, height=220, width=220)
                ),
                MessageImagemapAction(
                    text="Wing Spiker",
                    area=ImagemapArea(x=655, y=185, height=220, width=220)
                ),
                MessageImagemapAction(
                    text="Wing Spiker",
                    area=ImagemapArea(x=160, y=495, height=220, width=220)
                ),
                MessageImagemapAction(
                    text="Middle Blocker",
                    area=ImagemapArea(x=405, y=495, height=220, width=220)
                ),
                MessageImagemapAction(
                    text="Setter",
                    area=ImagemapArea(x=655, y=495, height=220, width=220)
                ),
                MessageImagemapAction(
                    text="Libero",
                    area=ImagemapArea(x=655, y=795, height=220, width=220)
                )
            ]
        )
        text_message = TextSendMessage(text="\U0000203C請點選下方『圖片的位置』來了解該位置球員～\n\n例如：\n我想了解OP位，請點選左上方『澤村』的頭像方格")
        message_send = [text_message, imagemap]
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_send)
        
    def on_enter_ws(self, event):
        print("I'm entering Wing spiker")  
        reply_token = event.reply_token
        message = player_intro.WS
        message_to_reply = FlexSendMessage("WS", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_mb(self, event):
        print("I'm entering MIddle Blocker")  
        reply_token = event.reply_token
        message = player_intro.MB
        message_to_reply = FlexSendMessage("MB", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_op(self, event):
        print("I'm entering OP")  
        reply_token = event.reply_token
        message = player_intro.OP
        message_to_reply = FlexSendMessage("OP", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_s(self, event):
        print("I'm entering setter")  
        reply_token = event.reply_token
        message = player_intro.S
        message_to_reply = FlexSendMessage("S", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_l(self, event):
        print("I'm entering libero")  
        reply_token = event.reply_token
        message = player_intro.L
        message_to_reply = FlexSendMessage("L", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)
    
    def on_enter_rules(self, event):
        # website scraping using beautifulsoup
        print("i am entering rules 比賽規則")
        reply_token = event.reply_token

        ## the rules[0] is th title
        foul_rules = soup.get_foul_rule()
        message1 = ''
        for i in range(len(foul_rules)):
            if i == 0:
                message1 += ('\U0001F3D0 ' + foul_rules[i] + ' \U0001F3D0\n\n')
            else:
                message1 += ('\U0001F31F ' + foul_rules[i] + '\n\n')
        
        change_rules = soup.change_and_timeout()
        message2 = ''
        for i in range(len(change_rules)):
            if i == 0:
                message2 += ('\U0001F3D0 ' + change_rules[i] + ' \U0001F3D0\n\n')
            else:
                message2 += ('\U0001F91D ' + change_rules[i] + '\n')

        score_rules = soup.score()
        message3 = ''
        for i in range(len(score_rules)):
            if i == 0:
                message3 += ('\U0001F3D0 ' + score_rules[i] + ' \U0001F3D0\n\n')
            else:
                message3 += ('\U0001F609 ' + score_rules[i] + '\n')

        quick_message = TextSendMessage(text="以上規則爬取自 維基百科，希望對使用者有幫助 \U0001F440\n\n 現在可以輸入『主選單』返回主選單 \n\n\U00002705 也可以直接使用快捷按鈕", 
                                        quick_reply=QuickReply(items=[
                                            QuickReplyButton(action=MessageAction(label="主選單", text="主選單"))
                                        ]))

        sendmessage = [TextSendMessage(text=message1), TextSendMessage(text=message2), TextSendMessage(text=message3), quick_message]
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, sendmessage)

    def on_enter_rotation(self, event):
        # sad, i cannot scrape this website by beautifulsoup :(
        # and it will take too long to use selenium...
        # i think i can only copy and paste
        # url = 'http://area.hcjh.tn.edu.tw/health/排球教學網站-資訊教學媒體競賽/1.htm'
        print("i am entering rotation 輪轉規則")
        reply_token = event.reply_token
        image_message = ImageSendMessage(
            original_content_url='https://images.squarespace-cdn.com/content/v1/5cd106404d871189e4392d5e/1598333863972-D05PLIFYVXIVRR2BP91O/1.png',
            preview_image_url='https://images.squarespace-cdn.com/content/v1/5cd106404d871189e4392d5e/1598333863972-D05PLIFYVXIVRR2BP91O/1.png'
        )
        message = '\U0001F3D0 位置 \U0001F3D0 \n\n' + '發球員的擊球瞬間，雙方球員必須在各自的場區內，按輪轉順序站位（發球員除外）。\n\n'
        message += '\U0001F914 場上球員的位置代號如下：\n靠近球網的三名是前排球員，各站在4號位（前排左）、3號位（前排中）和2號位（前排右）。\n另外三位是後排球員，各站在5號位（後排左）、6號位（後排中）和1號位（後排右）。\n\n'
        message += '\U0001F914 球員之間的位置關係為：\n每一後排球員的位置，必須比其同列的前排球員距離球網更遠。\n\n'
        message += '\n\U0001F3D0 輪轉 \U0001F3D0 \n\n整局比賽的輪轉順序、發球順序和球員位置，都依球隊的先發陣容決定和管制。\n發球隊獲得發球權時，該隊球員必須按順時鐘方向輪轉一個位置，2號位球員轉到1號位發球，1號位球員轉到6號位，餘此類推。\n'

        quick_message = TextSendMessage(text="以上規則擷取自 排球教學網站-資訊教學媒體競賽，希望對使用者有幫助 \U0001F440\n\n 現在可以輸入『主選單』返回主選單 \n\n\U00002705 也可以直接使用快捷按鈕", 
                                        quick_reply=QuickReply(items=[
                                            QuickReplyButton(action=MessageAction(label="主選單", text="主選單"))
                                        ]))
        messagesend = [image_message, TextSendMessage(message), quick_message]
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, messagesend)

    def on_enter_volleyball_game(self, event):
        print("i am entering volleyball game 排球比賽")
        print("I'm entering setter")  
        reply_token = event.reply_token
        message = message_template.game
        message_to_reply = FlexSendMessage("S", message)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_reply)
        

    def on_enter_volleyball_world(self, event):
        print("i am entering volleyball word")
        reply_token = event.reply_token

        keyword = 'volleyballworld'
        video_info = sele.get_youtube_video_links(keyword, 5)
        video_link = video_info[0]
        image_link = video_info[1]

        print(video_link)
        print(image_link)

        col = []
        for i in range(5):
            c = ImageCarouselColumn(
                image_url = image_link[i],
                action = URITemplateAction(
                    label = '點我觀看影片',
                    uri = video_link[i]
                )
            )
            col.append(c)

        line_bot_api = LineBotApi(channel_access_token)
        carousel_message = TemplateSendMessage(
            alt_text = 'Carousel template',
            template = ImageCarouselTemplate(columns = col)
        )

        quick_message = TextSendMessage(text="以上影片爬取自 " + keyword + "官方 YouTube ，希望對使用者有幫助 \U0001F440\n\n 現在可以輸入『主選單』返回主選單或者『排球比賽』觀看其他賽事 \n\n\U00002705 也可以直接使用快捷按鈕", 
                                        quick_reply=QuickReply(items=[
                                            QuickReplyButton(action=MessageAction(label="主選單", text="主選單")),
                                            QuickReplyButton(action=MessageAction(label="排球比賽", text="排球比賽"))
                                        ]))
        message_to_send = [carousel_message, quick_message]
        line_bot_api.reply_message(reply_token, message_to_send)

    def on_enter_vleague(self, event):
        print("i am entering V 聯盟")
        reply_token = event.reply_token

        keyword = 'VLEAGUEOfficialChannel'
        video_info = sele.get_youtube_video_links(keyword, 5)
        video_link = video_info[0]
        image_link = video_info[1]

        print(video_link)
        print(image_link)

        col = []
        for i in range(5):
            c = ImageCarouselColumn(
                image_url = image_link[i],
                action = URITemplateAction(
                    label = '點我觀看影片',
                    uri = video_link[i]
                )
            )
            col.append(c)

        line_bot_api = LineBotApi(channel_access_token)
        carousel_message = TemplateSendMessage(
            alt_text = 'Carousel template',
            template = ImageCarouselTemplate(columns = col)
        )

        quick_message = TextSendMessage(text="以上影片爬取自 " + keyword + "官方 YouTube ，希望對使用者有幫助 \U0001F440\n\n 現在可以輸入『主選單』返回主選單或者『排球比賽』觀看其他賽事 \n\n\U00002705 也可以直接使用快捷按鈕", 
                                        quick_reply=QuickReply(items=[
                                            QuickReplyButton(action=MessageAction(label="主選單", text="主選單")),
                                            QuickReplyButton(action=MessageAction(label="排球比賽", text="排球比賽"))
                                        ]))
        message_to_send = [carousel_message, quick_message]
        line_bot_api.reply_message(reply_token, message_to_send)

    def on_enter_hop(self, event):
        print("i am entering HOP")
        reply_token = event.reply_token

        keyword = 'HOPSports'
        video_info = sele.get_youtube_video_links(keyword, 5)
        video_link = video_info[0]
        image_link = video_info[1]

        print(video_link)
        print(image_link)

        col = []
        for i in range(5):
            c = ImageCarouselColumn(
                image_url = image_link[i],
                action = URITemplateAction(
                    label = '點我觀看影片',
                    uri = video_link[i]
                )
            )
            col.append(c)

        line_bot_api = LineBotApi(channel_access_token)
        carousel_message = TemplateSendMessage(
            alt_text = 'Carousel template',
            template = ImageCarouselTemplate(columns = col)
        )

        quick_message = TextSendMessage(text="以上影片爬取自 " + keyword + "官方 YouTube ，希望對使用者有幫助 \U0001F440\n\n 現在可以輸入『主選單』返回主選單或者『排球比賽』觀看其他賽事 \n\n\U00002705 也可以直接使用快捷按鈕", 
                                        quick_reply=QuickReply(items=[
                                            QuickReplyButton(action=MessageAction(label="主選單", text="主選單")),
                                            QuickReplyButton(action=MessageAction(label="排球比賽", text="排球比賽"))
                                        ]))
        message_to_send = [carousel_message, quick_message]
        line_bot_api.reply_message(reply_token, message_to_send)

    def on_enter_media(self, event):
        print("i am entering media")
        reply_token = event.reply_token
        message = message_template.media
        message_to_reply = FlexSendMessage("social media", message)
        quick_message = TextSendMessage(text="以上網址能連接去該社群網站，在此推薦給使用者 \U0000263A\n\n 現在可以輸入『主選單』返回主選單 \n\n\U00002705 也可以直接使用快捷按鈕", 
                                        quick_reply=QuickReply(items=[
                                            QuickReplyButton(action=MessageAction(label="主選單", text="主選單")),
                                        ]))
        message_to_send = [message_to_reply, quick_message]
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, message_to_send)