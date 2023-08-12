from django.shortcuts import render

# Create your views here.


# In[] Import the third-party packages
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
    MessageTemplateAction, TemplateSendMessage, CarouselTemplate,
    CarouselColumn, URITemplateAction, ConfirmTemplate,
    ButtonsTemplate, LocationMessage, LocationSendMessage,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, URIAction, QuickReply, QuickReplyButton, MessageAction,
    SourceUser
)


import requests
import emoji


# In[] Link to the "Capstone_bot"
line_bot_api= LineBotApi("3NLAIbX8Cy0KVIThE8ZeBg/xRodllRwe9igIbp6g4cb+QHuBcKMco4chMhiMT41Z8DaYVeSkvVe1aW0EzlYFm/F74YKhf8PNrQ1KXuVdEkFGp2c5Ojj72FhpfY2UJdKVpSzICGsVQlglBsBDpyaeygdB04t89/1O/w1cDnyilFU=")   #在 line_developer取得  
handler= WebhookHandler("1b0d223a012c07f284648494782f59e5")          #在 line_developer取得


# In[] 機器人主程式
@csrf_exempt
def callback(request):
    if request.method == 'POST':
	# get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']
		
        # get request body as text
        body = request.body.decode('utf-8')
        
	# handle webhook body
        try:
            events = handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

        return HttpResponse()  

def waterdepth():
    with open("waterdepth.txt", mode="r") as f:
        r = f.readlines()
        return r[-1]    
    
# In[] 
def dsp_crawler():    
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
              }
    
    
    #-- 感測資料-水利署_淹水感測器
    url= 'https://sta.ci.taiwan.gov.tw/STA_WaterResource_v2/v1.0/Datastreams?$expand=Thing,Thing/Locations,Observations($orderby=phenomenonTime%20desc;$top=1)%20&$filter=Thing/properties/authority_type%20eq%20%27%E6%B0%B4%E5%88%A9%E7%BD%B2%27%20%20and%20substringof(%27Datastream_Category_type=%E6%B7%B9%E6%B0%B4%E6%84%9F%E6%B8%AC%E5%99%A8%27,Datastreams/description)%20and%20substringof(%27Datastream_Category=%E6%B7%B9%E6%B0%B4%E6%B7%B1%E5%BA%A6%27,Datastreams/description)%20&$count=true'
    

    r= requests.get(url, headers= headers, verify= False)
    data= r.json()
    value= data['value']
    
    for i in range(len(value)):
        
        properties= value[i]['Thing']['properties']
        authority= properties['authority']
        stationName= properties['stationName']
        
        #-- 目標觀測站
        if stationName == '田中八堡圳淹水監控站':
            
            Locations= value[i]['Thing']['Locations']
            lon= Locations[0]['location']['coordinates'][0]
            lat= Locations[0]['location']['coordinates'][1]
                
            Observations= value[i]['Observations']
                
            phenomenonTime= Observations[0]['phenomenonTime']
            phenomenonTime= phenomenonTime[0:10] + ' ' + phenomenonTime[11:16]
                
            waterDepth= Observations[0]['result']  #-- unit: cm
            if float(waterDepth) < 0: waterDepth= 0.0
            waterDepth= round(float(waterDepth), 1)
        
            msg =  ':ocean:' + authority + '\n' 
            msg += stationName + '的觀測水深為{:.1f}公分'.format( float(waterDepth) ) + '\n'
            msg += ':watch:' + '觀測時間: ' +  phenomenonTime
            msg= emoji.emojize(msg, use_aliases=True)        

            return msg


# In[]
#-- reply message
@handler.add(MessageEvent, message= TextMessage)
def message_text(event):
    if event.message.text == u"水深":
        #-- 取得觀測水深訊息
        message= int(waterdepth()[0:2])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text= message))
    
    elif event.message.text == u"雨量圖":
        url= "https://cwbopendata.s3.ap-northeast-1.amazonaws.com/DIV2/O-A0040-002.jpg"
        message = ImageSendMessage(original_content_url= url, preview_image_url= url)
        line_bot_api.reply_message(event.reply_token, message)
    
    else:
        profile = line_bot_api.get_profile(event.source.user_id)
        display_name= profile.display_name
        line_bot_api.reply_message(event.reply_token, \
                                   TextSendMessage(text= emoji.emojize(display_name + '您好:' + '\n' + \
                                                                       ':speech_balloon:'+'聊天機器人暫不支援您輸入的查詢，請您使用選單重新查詢，謝謝!', use_aliases=True)))
