#!/usr/bin/python
# -*- coding: latin-1 -*-
# $Id: xmppChat.py,v 1.2 2006/10/06 12:30:42 normanr Exp $

import sleekxmpp
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from time import sleep
import logging
import sys
import os
import select

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):

    reload(sys)
    sys.setdefaultencoding('utf8')

else:

    raw_input = input

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/tmp/xmppClient.log',
                    filemode='w')


# Function starting presence event
def session_start(event):

    chatbot.send_presence(pshow='xa' ,  ppriority="0")
    print('Session started')
    chatbot.get_roster()


# Function to manage (Handle) incoming user messages
def message(msg):

	if msg['type'] in ('chat', 'normal'):

		print(msg['body'])
		message = raw_input('Answer : ')
		msg.reply(str(message)).send()



if __name__ == '__main__':

	# Usage Instructions to execute (calling) the script :
    	if(len(sys.argv) < 3):

	    	print ' Chat Usage :' + ' xmppFacebookChat  userID   user_password   destJID '
	    	print 'All Parameters goes without string comas'
		sys.exit()

	jid = sys.argv[1]
	password = sys.argv[2]
	server = ("chat.facebook.com", 5222)
	dest = sys.argv[3] 

	chatbot = sleekxmpp.ClientXMPP(jid, password)
	chatbot.register_plugin(u'xep_0030')  # Service Discovery
	chatbot.register_plugin(u'xep_0045')  # Multi-User Chat
	chatbot.register_plugin(u'xep_0199')  # XMPP Ping
	chatbot.register_plugin(u'xep_0203')  # XMPP Delayed messages
	chatbot.add_event_handler('session_start', session_start)
	chatbot.add_event_handler('message', message)
	chatbot.auto_reconnect = True
	chatbot.connect(server)
	chatbot['feature_mechanisms'].unencrypted_plain = True
	chatbot.process()
	
	sleep(8)
	while (1):

		message = raw_input('Message to Send : ');
		chatbot.send_message(sys.argv[4], str(message), 'chat')
		sleep(1)