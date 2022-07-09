import requests
import json
 
def post_message(token, channel, text, attachments=None):
    attachments = json.dumps(attachments)
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel, "text": text, "attachments":attachments}
    )
    print(response)

markdown_text = '''
*반갑습니다 휴먼.*
'''

attach_dict = {
    'color' : '#ff0000',
    'author_name' : 'INVESTAR',
    'author_link' : 'github.com/investar',
    'title' : '오늘의 증시 KOSPI',
    'title_link' : 'http://finance.naver.com/sise/sise_index.nhn?code=KOSPI',
    'text' : '2.326.13 △11.89 (+0.51%)',
    'image_url' : 'https://ssl.pstatic.net/imgstock/chart3/day/KOSPI.png'
    }

attach_list = [attach_dict]

 
myToken = "*****************************"
 
post_message(myToken,"#stock_info",text=markdown_text,
             attachments=attach_list)
