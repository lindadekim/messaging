Det behövs installera :
sqlalchemy

Det har programmet utvecklas och testas med Python 2.7.10 version.

===============================

Man kan börja message server genom att starta:
>>Python messageserver.py
Default port är 9090, men det kan man ändra direkt på messageserver.py.

Det finns några data redan, i "message.db" (SQLite)

Det finns tre användare : sandy, lala99, karo90
och, några "not-yet-seen" meddelande.
(Finns inget implementation for att skapa användare via REST)

===============================

curl Request Examples

1. skicka meddelande till 
POST:
om avsändare information saknas, då sender=receiver.
curl -X POST -d "textmsg=Hi%2C+nice+to+meet+you%21" http://127.0.0.1:9090/users/sandy/messages

man kan inkluderar avsändare information i parameter : sender=lala90 t.ex.
curl -X POST -d "sender=lala99&textmsg=Hi%2C+nice+to+meet+you%21" http://127.0.0.1:9090/users/sandy/messages


2. hämta nya meddelande till mottagaren:
GET:
retrieve not-yet-seen messages:
curl http://127.0.0.1:9090/users/sandy/messages
curl http://127.0.0.1:9090/users/lala99/messages

3. ta bort meddelande 

DELETE:

raderar meddelande med id nummer (primary key. 
(Dock, finns inget intern verifiering om meddelande tillhör mottagare..just nu)

curl -X DELETE http://127.0.0.1:9090/users/sandy/messages/3

4. Hämta tidsordnade meddelande:
GET: startindex & endindex. (sorterar för alla meddelande, både redan läst och inte läst)

curl "http://127.0.0.1:9090/users/sandy/messages?startindex=1&endindex=3"
or encoded:
curl http://127.0.0.1:9090/users/sandy/messages%3Fstartindex%3D1%26endindex%3D3




