#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Sequence, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
import datetime
import logging
engine=create_engine('sqlite:///message.db')
Base = declarative_base()
Session=sessionmaker(bind=engine,expire_on_commit=False)

    
class User(Base):
    __tablename__= 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(60), unique=True)
    epost = Column(String(80), unique=True)
    tel = Column(String(20))
    def __repr__(self):
        return "<User(username='%s', epost='%s', password='%s')>" % (self.username, self.epost, self.tel)
        
    
class Message(Base):
    __tablename__='messages'
    id = Column(Integer, Sequence('msg_id_seq'), primary_key=True)
    
    text = Column(String(100))
    timestamp = Column(DateTime())
    viewed  = Column(Boolean, default = False)
                     
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    def __repr__(self):
        return "<Message(id='%s', text='%s', viewed='%s', timestamp='%s', receiver='%s', sender='%s')>" % (self.id, self.text, self.viewed, self.timestamp, self.receiver.username, self.sender.username)
        
     
def retrieveMessage(ruser, retrieveRange=None):
    session = Session()
    msgs= getMessage(ruser,  session, retrieveRange)
    session.commit()
    session.close()
    return msgs


def createMessage(sender, receiver, msgtxt):
    session = Session()
    msgs= addMessage(sender, receiver, msgtxt,session)    
    session.commit()
    session.close()
    return msgs

def deleteMessage(messageid):
    session = Session()
    resultMsg={}
    try:
        msg = session.query(Message).filter(Message.id==messageid).first()
        session.delete(msg)
        resultMsg["results"] = ["message {} is deleted".format(messageid)]
    except Exception as e:
        resultMsg["errorMsg"] = "error in delete with messageid = {}, detail={}".format(messageid, e)
            
    session.commit()
    session.close()
    return resultMsg
    

def getMessage(ruser, session, retriveRange=None):
    
    #retrive last non-read messages
    resultMsg={}
    resultMsg["results"]=[]
    resultMsg["errorMsg"]=""
    if retriveRange is None:
        try:
            print "retrieving for receiveUser={}".format(ruser)

            for m in session.query(Message).filter(User.id==Message.receiver_id).filter(User.username==ruser).filter(Message.viewed==False).all():                
                m.viewed = True
                resultMsg["results"].append(str(m))
                
        except Exception as e:
            resultMsg["errorMsg"] = "query exception {]}".format(e)
            
            
    else:
        (startRange, endRange) = retriveRange
        try :
            
            maxLimit = session.query(Message).filter(User.id==Message.receiver_id).filter(User.username==ruser).count()
            if not (0<startRange <=maxLimit and 0<endRange<=maxLimit):
                resultMsg["errorMsg"] = "index value out of range, should be between 1 and {}".format(maxLimit)
                return resultMsg
                         
            for m in session.query(Message).filter(User.id==Message.receiver_id).filter(User.username==ruser).order_by(Message.timestamp).limit(endRange-startRange+1).offset(startRange-1).all():
                
                m.viewed = True         
                resultMsg["results"].append(str(m))
                
        except Exception as e:
            resultMsg["errorMsg"] = "query exception {]}".format(e)    
    return resultMsg
    
def addMessage(sender, receiver, msgtxt, session ):
    resultMsg={}
    resultMsg["results"]=[]
    resultMsg["errorMsg"]=[]
    try:
        sender_user = session.query(User).filter_by(username=sender).one()        
    except:        
        resultMsg["errorMsg"] ="fail to retreive one sender id"
    
    try:
        receiver_user = session.query(User).filter_by(username=receiver).one()        
    except:        
        resultMsg["errorMsg"] ="fail to retreive one sender id"
    
    msg = Message(text=msgtxt, timestamp=datetime.datetime.now())
    msg.sender=sender_user
    msg.receiver=receiver_user
    session.add(msg)
    resultMsg["results"].append(str(msg))
    return resultMsg
    
def addUser(uname, emailaddr, telnr, session):
    
    try:
        if session.query(User).filter_by(username=uname).count() > 0 :
            raise Exception("username already exist")
        if session.query(User).filter_by(epost=emailaddr).count() > 0 :
            raise Exception("epost already exist")
    except:
        print "fail to create user"
        
    user = User(username=uname, epost=emailaddr, tel=telnr)    
    session.add(user)        
   

def initDBTable():
    Base.metadata.create_all(engine)


def main():
    initDBTable()
    session = Session()
 
    addUser("lala99", "laura.korin@email.com", "98465837", session)
    addUser("sandy", "sandy.paros@yahoo.com", "7459574", session)
    addUser("karo90", "karol.ner@gmail.com", "98465837", session)
    session.commit()
    
    addMessage("lala99", "sandy", "hello, what\'s up?", session)
    addMessage("sandy", "lala99", "hello, Fine!", session)
    addMessage("lala99", "sandy", "shall we meet today?", session)
    addMessage("lala99", "sandy", "Thi is my message 1", session)
    addMessage("lala99", "sandy", "Thi is my message 2", session)
    addMessage("lala99", "sandy", "Thi is my message 3", session)
    addMessage("lala99", "sandy", "Thi is my message 4", session)
    addMessage("sandy", "lala99", "Yes!", session)
    addMessage("karo90", "sandy", "Nice to meet you", session)
    session.commit()
    session.close()
    
if __name__ == "__main__":
    main()
