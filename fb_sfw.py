from fb_msnger import FB_Messenger_Handler
import json
import os 

class FB_SFW():
    def __init__(self,fb_msg):
        self.fb_msg=fb_msg
        self.state='choose_user'
        self.current_user=''
    def command(self,cmd):
        if cmd=='':
            pass
        elif cmd[0]=='/':
            if cmd[1:]=='back':
                self.state='choose_user'
            elif cmd[1:]=='exit':
                self.state=='exit'


    def choose_user(self):
        username=input()
        self.fb_msg.get_user_msg(username)
        self.current_user=username
        self.state='user_chat'

    def refresh(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        self.fb_msg.get_user_msg(self.current_user)

    def send_msg(self,msg):
        if msg=='':
            self.refresh()
            return
        self.fb_msg.send_msg_to_user(self.current_user,msg)
        self.refresh()

    def run(self):
        first=True
        while True:
            if not first:
                cmd=input()
                self.command(cmd)
            first=False
            if self.state=='end':
                print('Bye~')
                break
            elif self.state=='choose_user':
                self.fb_msg.get_msg_list()
                self.choose_user()
            elif self.state=='user_chat':
                self.send_msg(cmd)
            elif self.state=='exit':
                break
if __name__=='__main__':
    with open('cookie.json' , 'r') as reader:
        json_cookie = json.loads(reader.read())
    cookie = json_cookie['cookie']
    facebook_id = json_cookie['facebook_id']
    fb_msg_handler=FB_Messenger_Handler(cookie=cookie,facebook_id=facebook_id)
    fbsfw=FB_SFW(fb_msg_handler)
    fbsfw.run()
