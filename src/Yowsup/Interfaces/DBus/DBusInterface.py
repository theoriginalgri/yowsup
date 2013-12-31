'''
Copyright (c) <2012> Tarek Galal <tare2.galal@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR 
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import dbus.service
import inspect

from ...Interfaces.Interface import SignalInterfaceBase, MethodInterfaceBase
from ...connectionmanager import YowsupConnectionManager

DBUS_SERVICE = "com.yowsup"

class DBusInitInterface(dbus.service.Object):

	DBUS_INTERFACE = "com.yowsup.initializer"

	def __init__(self):
		self.busName = dbus.service.BusName(DBUS_SERVICE, bus=dbus.SessionBus())
		dbus.service.Object.__init__(self,self.busName, '/com/yowsup')
		
		self.connections = {}
		
		super(DBusInitInterface, self).__init__()
		
	@dbus.service.method(DBUS_INTERFACE)
	def init(self, username):
		man = YowsupConnectionManager()
		man.setInterfaces(DBusSignalInterface(self.busName, username), DBusMethodInterface(self.busName, username))
		self.connections[username] = man
		
		return username
		

class DBusSignalInterface(SignalInterfaceBase, dbus.service.Object):

	DBUS_INTERFACE = "com.yowsup.signals"
	
	def __init__(self, busName, connectionId):
		self.connectionId = connectionId
		self.busName = busName
		dbus.service.Object.__init__(self, self.busName, '/com/yowsup/%s/signals'%connectionId)

		super(DBusSignalInterface,self).__init__();

		self._attachDbusSignalsToSignals()


	@dbus.service.method(DBUS_INTERFACE)
	def getSignals(self):
		return self.signals
	
	def _attachDbusSignalsToSignals(self):
		for s in self.signals:
			try:
				currBusSig = getattr(self, s)
				self.registerListener(s, currBusSig)
				print("Registered %s on Dbus " % s)
			except AttributeError:
				print("Skipping %s" %s)

	## Signals ##
	
	
	@dbus.service.signal(DBUS_INTERFACE)
	def auth_success(self, username):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def auth_fail(self, username, reason):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def presence_updated(self, jid, lastSeen):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def presence_available(self, jid):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def presence_unavailable(self, jid):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def message_received(self, msgId, jid, content, timestamp, wantsReceipt, pushName, isBroadcast):
		pass
#--------------------------------------------------------------------------- Groups
	@dbus.service.signal(DBUS_INTERFACE)
	def group_messageReceived(self, msgId, jid, author, content, timestamp, wantsReceipt):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_gotInfo(self, jid, owner, subject, subjectOwner, subjectT, creation):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_setSubjectSuccess(self, jid):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_subjectReceived(self, msgId, fromAttribute, author, newSubject, timestamp, receiptRequested):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_addParticipantsSuccess(self, jid, jids):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_removeParticipantsSuccess(self, jid, jids):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_createSuccess(self, jid):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_createFail(self, errorCode):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_endSuccess(self, jid):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_gotPicture(self, jid, pictureId, filepath):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_infoError(self, errorCode):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_gotParticipants(self,jid, jids):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_setPictureSuccess(self, jid, pictureId):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_setPictureError(self, jid, errorCode):
		pass
	
#------------------------------------------------------------------------------ 
	
	@dbus.service.signal(DBUS_INTERFACE)
	def profile_setStatusSuccess(self, jid, messageId):
		pass
	
	
	@dbus.service.signal(DBUS_INTERFACE)
	def profile_setPictureSuccess(self, pictureId):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def profile_setPictureError(self, errorCode):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def status_dirty(self):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def receipt_messageSent(self, jid, msgId):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def receipt_messageDelivered(self, jid, msgId):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def receipt_visible(self, jid, msgId):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def contact_gotProfilePictureId(self, jid, pictureId):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def contact_typing(self, jid):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def contact_paused(self, jid):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def contact_gotProfilePicture(self, jid, pictureId, filename):
		pass


	@dbus.service.signal(DBUS_INTERFACE)
	def notification_contactProfilePictureUpdated(self, jid, timestamp, messageId, pictureId, wantsReceipt = True):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def notification_contactProfilePictureRemoved(self, jid, timestamp, messageId, wantsReceipt = True):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def notification_groupParticipantAdded(self, gJid, jid, author, timestamp, messageId, wantsReceipt = True):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def notification_groupParticipantRemoved(self, gjid, jid, author, timestamp, messageId, wantsReceipt = True):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def notification_groupPictureUpdated(self, jid, author, timestamp, messageId, pictureId, wantsReceipt = True):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def notification_groupPictureRemoved(self, jid, author, timestamp, messageId, wantsReceipt = True):
		pass


	@dbus.service.signal(DBUS_INTERFACE)
	def image_received(self, messageId, jid, preview, url, size, wantsReceipt, isBroadcast):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def video_received(self, messageId, jid, preview, url, size, wantsReceipt, isBroadcast):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def audio_received(self, messageId, jid, url, size, wantsReceipt, isBroadcast):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def location_received(self, messageId, jid, name, preview, latitude, longitude, isBroadcast):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def vcard_received(self, messageId, jid, name, data, isBroadcast):
		pass


	@dbus.service.signal(DBUS_INTERFACE)
	def group_imageReceived(self, messageId, jid, author, preview, url, size, wantsReceipt):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_videoReceived(self, messageId, jid, author, preview, url, size, wantsReceipt):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_audioReceived(self, messageId, jid, author, url, size, wantsReceipt):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_locationReceived(self, messageId, jid, author, name, preview, latitude, longitude, wantsReceipt):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_vcardReceived(self, messageId, jid, author, name, data, wantsReceipt):
		pass
	
	
	@dbus.service.signal(DBUS_INTERFACE)
	def message_error(self, messageId, jid, errorCode):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def disconnected(self, reason):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def ping(self, pingId):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def pong(self):
		pass


class DBusMethodInterface(MethodInterfaceBase, dbus.service.Object):
	DBUS_INTERFACE = 'com.yowsup.methods'

	def __init__(self, busName, connectionId):
		self.connectionId = connectionId
		super(DBusMethodInterface,self).__init__();

		dbus.service.Object.__init__(self, busName, '/com/yowsup/%s/methods'%connectionId)

		self._checkMethods()

	def _checkMethods(self):
		for method in self.methods:
			try:
				getattr(self, method)
			except AttributeError:
				print "Missing function %s" % method

	def interfaceMethod(self):
		frame = inspect.stack()[1]
		fnName = frame[3]
		args = frame[0].f_locals
		del args["self"]

		return self.call(fnName, args)

	@dbus.service.method(DBUS_INTERFACE)
	def getMethods(self):
		return self.methods
	
	@dbus.service.method(DBUS_INTERFACE)
	def getVersion(self):
		return self.interfaceMethod()
	
	@dbus.service.method(DBUS_INTERFACE)
	def auth_login(self, number, password):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def message_send(self, jid, message):
		return self.interfaceMethod()
	
	@dbus.service.method(DBUS_INTERFACE)
	def message_imageSend(self, jid, url, name, size, preview):
		return self.interfaceMethod()
	
	@dbus.service.method(DBUS_INTERFACE)
	def message_videoSend(self, jid, url, name, size, preview):
		return self.interfaceMethod()
	
	@dbus.service.method(DBUS_INTERFACE)
	def message_audioSend(self, jid, url, name, size):
		return self.interfaceMethod()
	
	@dbus.service.method(DBUS_INTERFACE)
	def message_locationSend(self, jid, latitude, longitude, preview): #@@TODO add name to location?
		return self.interfaceMethod()
	
	@dbus.service.method(DBUS_INTERFACE)
	def message_vcardSend(self, jid, data, name):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def message_ack(self, jid, msgId):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def notification_ack(self, jid, msgId):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def clientconfig_send(self):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def delivered_ack(self, jid, msgId):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def visible_ack(self, jid, msgId):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def ping(self):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def pong(self, pingId):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def typing_send(self, jid):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def typing_paused(self,jid):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def subject_ack(self, jid, msgId):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def group_getInfo(self,jid):
		return self.interfaceMethod()
	
	@dbus.service.method(DBUS_INTERFACE)
	def group_getPicture(self,jid):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def group_create(self, subject):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def group_addParticipants(self, jid, participants):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def group_removeParticipants(self, jid, participants):
		return self.interfaceMethod()
	
	@dbus.service.method(DBUS_INTERFACE)
	def group_setPicture(self, jid, filepath):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def group_end(self, jid):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def group_setSubject(self, jid, subject):
		return self.interfaceMethod()


	@dbus.service.method(DBUS_INTERFACE)
	def group_getGroups(self, gtype):
		return self.interfaceMethod()
	
	@dbus.service.method(DBUS_INTERFACE)
	def group_getParticipants(self, jid):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def presence_sendAvailable(self):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def presence_request(self, jid):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def presence_sendUnavailable(self):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def presence_sendAvailableForChat(self):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def presence_subscribe(self, jid):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def presence_unsubscribe(self, jid):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def contact_getProfilePicture(self, jid):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def picture_get(self,jid):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def picture_getIds(self,jids):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def profile_getPicture(self):
		return self.interfaceMethod()
	
	@dbus.service.method(DBUS_INTERFACE)
	def profile_setStatus(self, status):
		return self.interfaceMethod()
	
	@dbus.service.method(DBUS_INTERFACE)
	def profile_setPicture(self, filepath):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def ready(self):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def disconnect(self, reason):
		return self.interfaceMethod()

	def message_broadcast(self, message):
		return self.interfaceMethod()

	@dbus.service.method(DBUS_INTERFACE)
	def media_requestUpload(self,  b64Hash, t, size, b64OrigHash = None):
		return self.interfaceMethod()

