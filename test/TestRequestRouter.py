import unittest
import requestrouter
from requestrouter import ActionDetail

    
class TestRESTRouter(unittest.TestCase):
    
    def testParameterValueAllowedOnlyAfterMessages(self):
        d = requestrouter.parseURL("/user/sandy/?parameter=value", "GET")
        self.assertEquals(d.action, ActionDetail.SHOW_INDEX)
        
    
    def testShowMainPageRoot(self):
        d = requestrouter.parseURL("/", "POST")    
        self.assertEquals(d.action, ActionDetail.SHOW_INDEX)
        
        d = requestrouter.parseURL("///", "POST")    
        self.assertEquals(d.action, ActionDetail.SHOW_INDEX)
        
        d = requestrouter.parseURL("//////", "POST")    
        self.assertEquals(d.action, ActionDetail.SHOW_INDEX)
    
    def testShowMainPageInvalidURL(self):
        d = requestrouter.parseURL("abc", "POST")    
        self.assertEquals(d.action, ActionDetail.SHOW_INDEX)
    
        d = requestrouter.parseURL("/user/abc/efg", "POST")    
        self.assertEquals(d.action, ActionDetail.SHOW_INDEX)
    
        d = requestrouter.parseURL("/user//message", "POST")    
        self.assertEquals(d.action, ActionDetail.SHOW_INDEX)
    
    def testShowMainPageStrangeCharacterInURL(self):
        d = requestrouter.parseURL("/users/&%sb#", "POST")    
        self.assertEquals(d.action, ActionDetail.SHOW_INDEX)
    
    def testShowUserInfo(self):
        d =requestrouter.parseURL("/users/sandy", "GET")
        self.assertEquals(d.action, ActionDetail.RETRIEVE)
        self.assertEquals(d.target, ActionDetail.USER)
        
        d =requestrouter.parseURL("/users/sandy/", "GET")
        self.assertEquals(d.action, ActionDetail.RETRIEVE)
        self.assertEquals(d.target, ActionDetail.USER)
   
    def testShowMessage(self):
        d =requestrouter.parseURL("/users/sandy/messages", "GET")
        self.assertEquals(d.action, ActionDetail.RETRIEVE)
        self.assertEquals(d.target, ActionDetail.MESSAGE)
        
        
        d =requestrouter.parseURL("/users/sandy/messages/abcdefg", "GET")
        self.assertEquals(d.action, ActionDetail.RETRIEVE)
        self.assertEquals(d.target, ActionDetail.MESSAGE)
        
    def testShowMessageAndParameters(self):
        d=requestrouter.parseURL("/users/sandy/messages?startindex=6&endindex=12", "GET")
        self.assertEquals(d.action, ActionDetail.RETRIEVE)
        self.assertEquals(d.target, ActionDetail.MESSAGE)
        
        self.assertEqual( d.parameters['startindex'],['6'])
        self.assertEqual( d.parameters['endindex'],['12'])
        self.assertEqual( d.parameters['receiver'],['sandy'])
        
        d=requestrouter.parseURL("/users/sandy/messages%3Fstartindex%3D1%26endindex%3D3", "GET")
        self.assertEquals(d.action, ActionDetail.RETRIEVE)
        self.assertEquals(d.target, ActionDetail.MESSAGE)
        self.assertEqual( d.parameters['startindex'],['1'])
        self.assertEqual( d.parameters['endindex'],['3'])
        
    def testCreateMessageAndParameters(self):
        d=requestrouter.parseURL("/users/sandy/messages?startindex=6&endindex=12", "POST", "textmsg=Hi%2C+nice+to+meet+you%21")
        self.assertEquals(d.action, ActionDetail.CREATE)
        self.assertEquals(d.target, ActionDetail.MESSAGE)
        self.assertEqual(d.parameters['textmsg'], ['Hi, nice to meet you!'])
    
    def testDeleteMessageWithParameters(self):
        d=requestrouter.parseURL("/users/sandy/messages/3", "DELETE")
        self.assertEquals(d.action, ActionDetail.DELETE)
        self.assertEquals(d.target, ActionDetail.MESSAGE)
        self.assertEqual(d.parameters['messageid'], ['3'])       
        
if __name__ == '__main__':
    unittest.main()        