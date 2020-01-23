import requests
from bs4 import BeautifulSoup
import json
class FB_Messenger_Handler():
    def __init__(self,cookie,facebook_id):
        self.url='https://m.facebook.com/'
        self.msnger_url='https://m.facebook.com/messages/?no_hist=1'

        self.login_headers={
            'authority': 'm.facebook.com',
            'method': 'POST',
            'scheme': 'https',
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',
            'cookie':cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        }
        self.session=requests.Session()
        self.session.headers.update(self.login_headers)
        self.facebook_id=facebook_id
    def get_msg_list(self):
        msg_req=self.session.get(self.msnger_url)
        if msg_req.status_code!=200:
            print('connection fail')
            print('status_code:'+str(msg_req.status_code))
            return
        msg_html=msg_req.text
        
        #get messenger data in <code>
        msg_soup = BeautifulSoup(msg_html, 'lxml')
        code=msg_soup.find('code',id='u_0_10')
        #analysis <code> data
        msg_soup=BeautifulSoup(code.string,'lxml')
        self.fb_dstg=msg_soup.find('input',{'name':'fb_dtsg'}).get('value')
        threadlist_rows=msg_soup.find('div',id='threadlist_rows')
        msg_threads=threadlist_rows.find_all(class_='_55wp _7om2 _5b6o _67ix _2ycx acw del_area async_del abb touchable _592p _25mv')
        self.msg_urls={} #{facebook_name:user_msg_url}
        self.user_id_dir={} # {facebook_name:facebook_id}
        msg_threads=threadlist_rows.find_all(class_='_55wp _7om2 _5b6o _67ix _2ycx acw del_area async_del abb touchable _592p _25mv')
        for msg_thread in msg_threads:
            msg_box=msg_thread.find('a')
            user_id_string=msg_thread.get('id')
            user_id_start=user_id_string.find('fbid_')
            user_id=user_id_string[user_id_start+5:]
            self.user_id_dir[msg_box.string]=user_id
            self.msg_urls[msg_box.string]=self.url+msg_box.get('href')
        print(self.user_id_dir)

    def get_user_msg(self,username):
        user_msg_req=self.session.get(self.msg_urls[username])
        if user_msg_req.status_code!=200:
            print('connection fail')
            print('status_code:'+str(user_msg_req.status_code))
            return
        user_msg_html=user_msg_req.text
        msg_soup=BeautifulSoup(user_msg_html, 'lxml')
        messageGroup=msg_soup.find('div',id='messageGroup')
        msg_blocks=messageGroup.find_all('div',class_='_z3m')
        for msg_block in msg_blocks:
            i=msg_block.find('i')
            if i != None:
                author=i.get('aria-label')
            else:
                author='me'
            print(author+':')
            msgs=msg_block.find_all('div',class_='_34ej')
            for msg in msgs:
                try:
                    if msg.string!=None:
                        print(msg.string)
                #to do:emoji analys (is in <span>
                except UnicodeEncodeError:
                    print("emoji")
                    emojis=msg.find_all('span',class_='_6qdm')
                    for emoji in emojis:
                        print(emoji.string)

    def send_msg_to_user(self,username,msg):
        self.msg_form_data={
            'tids': 'cid.c.%s:%s'%(self.facebook_id,self.user_id_dir[username]),
            'ids[%s]'%self.user_id_dir[username]: self.user_id_dir[username],
            'body': msg,
            'waterfall_source': 'message',
            'action_time': '1579787390203',
            'fb_dtsg': self.fb_dstg,
            'jazoest': '22178',
            '__dyn': '1KQEGiFoO13DzUjxC2GfGh28sBBgS5UqxKcwRxG9xu3Za363u2W1DxWUW0x8lxK4ohws82ywUx60GEeE2RwVwUwk9EdEnw9u1-wrEswvosw-wWwt8-0mWeKdwHwEU6i12wm8qwk888C0NE6C2Wq2a4U2IzUuxy0W8' ,
            '__req': 'dv',
            '__ajax__':' AYkRz9aV8yXy7KRuJioSm333Z47naWOE9uloTso3qNJEzR2GBBH-_aOtM_D0sTfFUtuvh1YFyXZmVHMBI-lHq8Jbs-6pYqX0dBTKrX8FXUjO8g',
            '__a':'AYkRz9aV8yXy7KRuJioSm333Z47naWOE9uloTso3qNJEzR2GBBH-_aOtM_D0sTfFUtuvh1YFyXZmVHMBI-lHq8Jbs-6pYqX0dBTKrX8FXUjO8g',
            '__user': self.facebook_id,
        }

        send_msg=self.session.post(self.url+'/messages/send/?icm=1&entrypoint=web%3Atrigger%3Athread_list_thread&refid=12',data=self.msg_form_data)
        if send_msg.status_code!=200:
            print('ERROR:send meesage fail!')
            return

if __name__=='__main__':
    with open('cookie.json' , 'r') as reader:
        json_cookie = json.loads(reader.read())
    cookie = json_cookie['cookie']
    facebook_id = json_cookie['facebook_id']
    fb_msger=FB_Messenger_Handler(cookie=cookie,facebook_id=facebook_id)
    fb_msger.get_msg_list()
    username=input()
    fb_msger.get_user_msg(username=username)
    fb_msger.send_msg_to_user(username=username,msg=input())
