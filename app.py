from flask import Flask, request
from Everest-Capital-Event-Microservice.Database.py import Event

event = Event()
app = Flask(__name__)


# works

@app.route("/create-event", methods=["POST"])
def create():
   
    res = request.json
    EventName = res['EventName']
    EventDate = res['EventDate']
    EventTime= res['EventTime']
    EventLocation = res['EventLocation']
    UserName = res['UserName']
    EventDescription = res['EventDescription'] 
    VirtualPerson = res['VirtualPerson']

    created = event.put(EventName=EventName, EventDate=EventDate, EventTime=EventTime,
                                EventLocation=EventLocation,UserName=UserName, EventDescription=EventDescription,
                                VirtualPerson=VirtualPerson, RSVP=[])
    return created


# works 
@app.route("/event-delete", methods=["POST"])
def delete():
    res = request.json
    EventName = res['EventName']

    deleted = event.delete(EventName=EventName)
    return deleted


# works
@app.route("/event-update", methods=["POST"])
def update():
    
    res = request.json
    EventName = res['EventName']
    New_EventDate = res['New_EventDate']
    New_EventTime= res['New_EventTime']
    New_EventLocation = res['New_EventLocation']
   
    New_EventDescription = res['New_EventDescription'] 
    New_VirtualPerson = res['New_VirtualPerson']
    updated = event.update_event(EventName=EventName, New_EventDate=New_EventDate, New_EventTime=New_EventTime,
                                New_EventLocation=New_EventLocation, New_EventDescription=New_EventDescription,
                                New_VirtualPerson=New_VirtualPerson


    return updated


@app.route("/event-view", methods=["GET"])
def view_event():
    res = event.view()
    return res


@app.route("/event-rsvp", methods=["POST"])
def rsvp():
    res = request.json
    EventName = res['EventName']
    UserName = res["UserName"]

    rsvp = event.rsvp(UserName=UserName, EventName=EventName)
    return rsvp


@app.route('/history', methods=["POST"])
def history():
    req = request.json
    username = req['UserName']
    res = event.getAllUserEvent(username)
    return res

#######
@app.route('/userRSVP', methods=['POST'])
def userRSVP():
    req = request.json
    username = req['UserName']
    res = event.getUserRvsp(username)
    return res

@app.route('/cancelRSVP', methods=['POST'])
def cancelReservation():
    req = request.json
    username = req['UserName']
    eventname = req['EventName']
    res = event.cancelRsvp(username, eventname)
    return res


@app.route('/', methods=['GET'])
def TEST():
    return "DOCKER WORKING FINE"

if __name__ == '__main__':
    app.run(debug=True)