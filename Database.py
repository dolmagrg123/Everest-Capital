import boto3
from boto3.dynamodb.conditions import Attr, Key

class Event:
    def __init__(self):
        self.__Tablename__ = "Everest_Event"
        self.client = boto3.client('dynamodb')
        self.DB = boto3.resource('dynamodb')
        self.Primary_Column_Name = "eventName"
        self.Primary_key = "eventName"
        self.columns = ["EventDate", "EventTime","EventLocation","UserName", "EventDescription", "VirtualPerson", "RSVP" ]
        self.table = self.DB.Table(self.__Tablename__)

    def put(self, EventName,EventDate,EventTime, EventLocation,UserName, EventDescription,VirtualPerson,RSVP):

        # Since EventName is the primary key, cant have two events with same name
        if (self.check_event_exists(EventName)):
            # immediately return false
            return {
                "Result": False,
                "Error": "Event cannot be created",
                "Description": "Event name already exists",
                "EventName": None
            }

        response = self.table.put_item(
            Item={
                self.Primary_Column_Name: EventName,
                self.columns[0]: EventDate,
                self.columns[1]: EventTime,
                self.columns[2]: EventLocation,
                self.columns[3]: UserName,
                self.columns[4]: EventDescription,
                self.columns[5]: VirtualPerson,
                self.columns[6]:RSVP
            }
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return {
                "Result": True,
                "Error": None,
                "Description": "Event was created succesfully",
                "EventName": EventName

            }
        else:
            return  {
                "Result": False,
                "Error": "Database error",
                "Description": "Database error",
                "EventName": None
            }
    #to check the names of the event that exist
    def check_event_exists(self, EventName):
        response = self.table.scan(
            FilterExpression=Attr("eventName").eq(EventName)
        )
        if response["Items"]:
            # EventName already exists in database
            return True
        else:
            return False

    def update_event(self, EventName,New_EventDate,New_EventTime, New_EventLocation, New_EventDescription,New_VirtualPerson):

        response = self.table.scan(
            FilterExpression=Attr("eventName").eq(EventName)
        )
        if response["Items"]:

            res = self.table.update_item(
                Key={
                    'eventName': EventName,

                },
                UpdateExpression="set EventDate=:d, EventTime=:t, EventLocation=:l, EventDescription=:c, VirtualPerson=:p",
                ExpressionAttributeValues={
                    # ':n': New_BlogName,
                    ':d': New_EventDate,
                    ':t': New_EventTime,
                    ':l': New_EventLocation,
                    ':c': New_EventDescription,
                    ':p': New_VirtualPerson
                }
                # ReturnValues="UPDATED_NEW"

            )
            # return res
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return {
                    "Result": True,
                    "Error": None,
                    "Description": "Event was updated succesfully",

                    "EventName": None
                }
            else:
                return {
                    "Result": False,
                    "Error": "Database error",
                    "Description": "Database error",
                    "EventName": None
                }
        else:
            return {
                "Result": False,
                "Error": "Event not found",
                "Description": "Cannot be updated",
                "EventName": None
            }

    def delete(self, EventName):
        response = self.table.scan(
            FilterExpression=Attr("eventName").eq(EventName)
        )
        if response["Items"]:
            self.Primary_key = response["Items"][0]["eventName"]
            res = self.table.delete_item(
                Key={
                    self.Primary_Column_Name: self.Primary_key
                }
            )
            return {
                "Result": True,
                "Error": None,
                "Description": "Event was deleted"
            }
        else:
            return {
                "Result": False,
                "Error": "Event does not exists",
                "Description": "Error"
            }

    def view(self):
        res = self.table.scan()

        return {
            "Result": True,
            "Error": None,
            "Description": "All Event from database",
            "EventsDB": res['Items']
        }



    def rsvp(self, UserName, EventName):
        #print(User)
        response = self.table.scan(
            FilterExpression=Attr("eventName").eq(EventName)
        )

        if response["Items"]:

            if UserName in response['Items'][0]['RSVP']:
                return {
                    "Result": False,
                    "Error": "Database error",
                    "Description": "Cannot RSVP more than once"
                }

            res = self.table.update_item(
                Key={
                    'eventName': EventName,

                },

                UpdateExpression="set RSVP= list_append(RSVP, :s)",
                ExpressionAttributeValues={
                    ':s': [UserName]
                }
                #
            )
            # return res
            if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return {
                    "Result": True,
                    "Error": None,
                    "Description": "You Have RSVPd to this event"
                }
            else:
                return {
                    "Result": False,
                    "Error": "Database error",
                    "Description": "Database error"
                }
        else:
            return {
                "Result": False,
                "Error": "Event not found",
                "Description": "Cannot add rsvp"
            }

    def getAllUserEvent(self, username):
        response = self.table.scan()['Items']
        lst = []
        if len(response) > 0:
            for d in response:
                if d['UserName'] == username:
                    lst.append(d)
            return {
                "Result": True,
                "Error": None,
                "Description": "All events this user created",
                "EventsDB": lst
            }
        else:
            return {
                "Result": False,
                "Error": "No events for this user",
                "Description": "This user haven't post any event yet.",
                "EventsDB": lst
            }

    def getUserRvsp(self, username):
        # get current user's rvsp
        lst = []
        response = self.table.scan()['Items']
        for i in response:
            if username in i['RSVP']:
                lst.append(i)

        return {
            "Result": True,
            "Error": None,
            "Description": "All RSVP for this user",
            "RSVP": lst
        }
        #return response


    def cancelRsvp(self, UserName, Eventname):
        response = self.table.scan(
            FilterExpression=Attr("eventName").eq(Eventname)
        )
        try:
            idx = response['Items'][0]['RSVP'].index(UserName)
        except:
            return {
                "Result": False,
                "Error": "User not found",
                "Description": "User haven't make RSVP to this event yet"
            }

        if response["Items"]:
            statement = "REMOVE RSVP["+ str(idx)+ "]"

            res = self.table.update_item(
                Key={
                    'eventName': Eventname,

                },

                UpdateExpression=statement,

            )
            # return res
            if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return {
                    "Result": True,
                    "Error": None,
                    "Description": "RSVP was cancelled successfully"
                }
            else:
                return {
                    "Result": False,
                    "Error": "Database error",
                    "Description": "Database error"
                }
        else:
            return {
                "Result": False,
                "Error": "Event not found",
                "Description": "Cannot cancel rsvp because event not found"
            }


if __name__ == "__main__":
    event = Event()

    # for create new event
    # res = event.put(EventName="Women In Tech Vs Finance",EventDate="11/13/2020",EventTime="9:00AM", EventLocation="NYC",UserName="RAM", EventDescription="How are women impacting the finaces?",VirtualPerson="Virtual",RSVP=[])
    
    # for update event
    # res = event.update_event(EventName="Women In Finance",New_EventDate="11/13/2020",New_EventTime="9:00AM", New_EventLocation="NYC", New_EventDescription="Update :How are women impacting the finaces in Everest? ",New_VirtualPerson="Online")

    # for delete
    # res = event.delete("Women In Tech Vs Finance")

    # for view
    # res = event.view()

    #RSVp
    # res =event.rsvp("Ram", "Women In Tech Vs Finance")

    #get all usre event
    # res =event.getAllUserEvent("RAM")

    #get all user rsvp
    # res = event.getUserRvsp("Ram")

    #cancelRSVP
    res = event.cancelRsvp("Ram", "Women In Tech Vs Finance")

print (res)