Det beh�vs installera :
sqlalchemy

Det har programmet utvecklas och testas med Python 2.7.10 version.

===============================

Man kan b�rja message server genom att starta:
>>Python messageserver.py
Default port �r 9090, men det kan man �ndra direkt p� messageserver.py.

Det finns n�gra data redan, i "message.db" (SQLite)

Det finns tre anv�ndare : sandy, lala99, karo90
och, n�gra "not-yet-seen" meddelande.
(Finns inget implementation for att skapa anv�ndare via REST)

===============================

curl Request Examples

1. skicka meddelande till 
POST:
om avs�ndare information saknas, d� sender=receiver.
curl -X POST -d "textmsg=Hi%2C+nice+to+meet+you%21" http://127.0.0.1:9090/users/sandy/messages

man kan inkluderar avs�ndare information i parameter : sender=lala90 t.ex.
curl -X POST -d "sender=lala99&textmsg=Hi%2C+nice+to+meet+you%21" http://127.0.0.1:9090/users/sandy/messages


2. h�mta nya meddelande till mottagaren:
GET:
retrieve not-yet-seen messages:
curl http://127.0.0.1:9090/users/sandy/messages
curl http://127.0.0.1:9090/users/lala99/messages

3. ta bort meddelande 

DELETE:

raderar meddelande med id nummer (primary key. 
(Dock, finns inget intern verifiering om meddelande tillh�r mottagare..just nu)

curl -X DELETE http://127.0.0.1:9090/users/sandy/messages/3

4. H�mta tidsordnade meddelande:
GET: startindex & endindex. (sorterar f�r alla meddelande, b�de redan l�st och inte l�st)

curl "http://127.0.0.1:9090/users/sandy/messages?startindex=1&endindex=3"
or encoded:
curl http://127.0.0.1:9090/users/sandy/messages%3Fstartindex%3D1%26endindex%3D3




