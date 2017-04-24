#!/usr/bin/env python
import re
import urlparse
import urllib
import datahandler
import pprint
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler=logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def parseURL(inputpath, httpMethod, postParam=None):
    logger.debug("parseURL inputpath={} httpMethod={} postParam={}".format(inputpath, httpMethod, postParam))
    
    localpath=urllib.unquote(inputpath)
    
    queryToken= localpath.split('?')
    parameters={}
    if len(queryToken) ==2 :
        parameters.update(urlparse.parse_qs(queryToken[1]))
        localpath = queryToken[0]
    if httpMethod == "POST" and postParam:
        parameters.update(urlparse.parse_qs(postParam))
    
    tokens = filter(None, localpath.split('/'))
    logger.debug("slash parsed tokens={}".format(tokens))
    
    for token in tokens:
        if re.search(r"\W", token):
            return ActionDetail(ActionDetail.SHOW_INDEX)
        
    if len(tokens) <= 1 :
        return ActionDetail(ActionDetail.SHOW_INDEX)
    
    if len(tokens) == 2:
        if tokens[0].lower() == "users" and tokens[1]:
            parameters['receiver'] = [tokens[1]]
            return ActionDetail(ActionDetail.RETRIEVE, ActionDetail.USER, parameters)
        
    if len(tokens) >= 3:        
        if tokens[0].lower() =="users" and tokens[1] and tokens[2].lower()=="messages":
            parameters['receiver'] = [tokens[1]]
            if len(tokens) ==4:
                parameters['messageid'] = [tokens[3]]
            if httpMethod == "POST":
                return ActionDetail(ActionDetail.CREATE, ActionDetail.MESSAGE, parameters)
            elif httpMethod == "DELETE":
                return ActionDetail(ActionDetail.DELETE, ActionDetail.MESSAGE, parameters)
            else :
                return ActionDetail(ActionDetail.RETRIEVE, ActionDetail.MESSAGE, parameters)                
             
    return ActionDetail(ActionDetail.SHOW_INDEX)

    
class ActionDetail(object):
    #action
    SHOW_INDEX = 2
    SHOW_ERROR =3
    
    RETRIEVE = 4
    CREATE = 5
    UPDATE = 6
    DELETE = 7
    
    #target
    USER = 10
    MESSAGE = 11

    def __init__(self, action=-1, target=-1, parameters=None):
        self.action = action
        self.target=target
        self.parameters =parameters
    
    
    
    def showIndex(self):
        return {"redirectPage":"index.html", "results":["redirect to main page!"]}
    
    
    def executeDelete(self):
        if self.target == ActionDetail.MESSAGE:
            try:
                messageid = int(self.parameters["messageid"][0])                
                return datahandler.deleteMessage(messageid)
            except KeyError:
                pass
            except ValueError:
                pass
            return {"errorMsg":"problem in getting messageid, cannot perform DELETE"}
        
    def executeRetrieve(self):
        
        if self.target == ActionDetail.MESSAGE:
            try:
                startindex = int(self.parameters["startindex"][0])
                endindex = int(self.parameters["endindex"][0])
                return datahandler.retrieveMessage(self.parameters["receiver"][0], (startindex, endindex))
            except KeyError:
                pass
            except ValueError:
                pass
            return datahandler.retrieveMessage(self.parameters["receiver"][0])
        #if self.target == self.USER:            
            #retrieveUser can be called here
        
    
    def executeCreate(self):
        if self.target == ActionDetail.MESSAGE:
            receiver =self.parameters["receiver"][0]
            try :
                textmsg = self.parameters["textmsg"][0]
            except KeyError:
                resultMsg["errorMsg"]="no text msg found"
                return resultMsg
            try:
                sender = self.parameters["sender"][0]
            except KeyError:
                sender =receiver                                    
        return datahandler.createMessage(sender, receiver, textmsg)
        
    def execute(self):
        logger.debug("execute target={} action={}".format(self.target, self.action))
        logger.debug("execute parameters={}".format(self.parameters))
        if self.action == ActionDetail.RETRIEVE:
           return pprint.pformat(self.executeRetrieve())
        if self.action == ActionDetail.CREATE:
            return pprint.pformat(self.executeCreate())
        if self.action == ActionDetail.DELETE:
            return pprint.pformat(self.executeDelete())
        if self.action == ActionDetail.SHOW_INDEX:
            return pprint.pformat(self.showIndex())
    
    
    
