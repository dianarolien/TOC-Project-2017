#coding=utf-8

import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '524201999:AAGla7TkBcoEHbPvsvezKptjHec9fzmFJTE'
WEBHOOK_URL = 'https://2b475f67.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
	'home',
	'novel',
	'biqukan',
	#'quanben',
	'write',
	'writing',
	'reading',
	'web'
    ],
    transitions=[
	{
	    'trigger': 'advance',
	    'source': 'home',
	    'dest': 'novel',
	    'conditions': 'is_going_to_novel'
	},
	{
	    'trigger': 'advance',
	    'source': [
		'novel',
		'biqukan',
	#	'quanben',
		'write',
		'writing',
		'reading',
		'web'
	    ],
	    'dest': 'home',
	    'conditions':'is_going_to_home'
	},
	{
	    'trigger': 'advance',
	    'source': 'novel',
	    'dest': 'biqukan',
	    'conditions': 'is_going_to_biqukan'
	},
	{
	    'trigger': 'advance',
	    'source': 'biqukan',
	    'dest': 'novel',
	    'conditions': 'is_back_to_novel'
	},
	{
	    'trigger': 'advance',
	    'source': 'novel',
	    'dest': 'home',
	    'conditions': 'is_back_to_home_novel'
	},
	{
	    'trigger': 'advance',
	    'source': 'web',
	    'dest': 'home',
	    'conditions': 'is_back_to_home_web'
	},
	{
	    'trigger': 'advance',
	    'source': 'home',
	    'dest': 'write',
	    'conditions': 'is_going_to_write'
	},
	{
	    'trigger': 'advance',
	    'source': 'write',
	    'dest': 'writing',
	    'conditions': 'is_going_to_writing'
	},
	{
	    'trigger': 'advance',
	    'source': 'write',
	    'dest': 'reading',
	    'conditions': 'is_going_to_reading'
	},
	{
	    'trigger': 'advance',
	    'source': 'write',
	    'dest': 'home',
	    'conditions': 'is_back_to_home_write'
	},
	{
	    'trigger': 'advance',
	    'source': 'writing',
	    'dest': 'write',
	    'conditions': 'is_back_to_write_writing'
	},
	{
	    'trigger': 'advance',
	    'source': 'reading',
	    'dest': 'write',
	    'conditions': 'is_back_to_write_reading'
	},
	{
	    'trigger': 'advance',
	    'source': 'home',
	    'dest': 'web',
	    'conditions': 'is_going_to_web'
	},
    ],
    initial='home',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
	status = bot.set_webhook(WEBHOOK_URL)
	if not status:
		print ('Webhook setup failed')
		sys.exit(1)
	else:
		print ('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
	update = telegram.Update.de_json(request.get_json(force=True), bot)
	text = update.message.text
	boolean = False
	
	if text != None:
		print (text)
		boolean = True
	if boolean:
		machine.advance(update,bot)
		if machine.state == 'home':
			start(update)

	return 'ok'

@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

def start(update):
    	update.message.reply_text("嗨,我是你的閱讀小幫手, Piggy.\nPiggy 我主要有三個功能:\n1.下載小說\n2.和別人一起寫小說\n3.推薦一些好用的相關網站\n\n輸入:\n/novel 開始下載小說\n/write 開始別人一起寫小說\n/web 相關網站\n/home 回到主選單\n/back 回到上一層目錄")
    
if __name__ == "__main__":	
    _set_webhook()
    machine.graph.draw('machine_state.png', prog ='dot')
    app.run()
