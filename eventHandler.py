import datetime
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

APP_PATH = "/etc/warmindforge"
DB_PATH = f"{APP_PATH}/events.db"
Engine = create_engine(f"sqlite:///{DB_PATH}")#, echo=True)
Session = sessionmaker(bind=Engine)
session = Session()
Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    date = Column(DateTime)
    event_type = Column(String(50))
    activity = Column(String(50))
    slot_0 = Column(String(50))
    slot_1 = Column(String(50))
    slot_2 = Column(String(50))
    slot_3 = Column(String(50))
    slot_4 = Column(String(50))
    slot_5 = Column(String(50))
    alt_1 = Column(String(50))
    alt_2 = Column(String(50))
    alt_3 = Column(String(50))
    suppress = Column(Integer)

def initdb():
    Base.metadata.bind = Engine
    Base.metadata.create_all(Engine)

class FireteamFunctions(object):
    """
    Class that handles Fireteams
    """

    def __init__(self):
        pass

    def expired_calendar_cleanup(self):
        # identify events older than 1 day and suppress them
        date_yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        all_events = session.query(Event).all()
        for event in all_events:
            eventDate = event.date
            if eventDate < date_yesterday:
                new_suppress = 1
            else:
                new_suppress = 0
            session.query(Event).filter_by(id = event.id).update({Event.suppress:1})

    def create_test_event(self):
        # UNUSED
        """

        """
        this_event_name = input("Name of event: ")
        date_entry = input('Enter a date in YYYY-MM-DD format: ')
        year, month, day = map(int, date_entry.split('-'))
        this_event_date = datetime.date(year, month, day)
        time_entry = input('Enter a time in 24 hour format (23:30): ')
        hour, minute = map(int, time_entry.split(':'))
        this_event_time = datetime.time(hour, minute)
        this_event_occurs = datetime.datetime(year, month, day, hour, minute)
        # print(this_event_occurs - datetime.datetime.now())
        # this_event_time = datetime.time.
        this_user = "N1N3 13"
        this_type = "raid"
        this_activity = "king's fall"
        entry = [this_event_name, this_event_occurs, this_type, this_activity, this_user]
        self.incursion_update(this_event_name, this_event_occurs, this_type, this_activity, this_user)
        # print(entry)
        # print(this_event_time)

    def incursion_event_help(self):
        # HELP
        msg = ('AI-HANDLER // COMMAND SYNTAX \n'
               ' THIS COMMAND SYNTAX: `!event help`\n'
               ' LIST INCURSIONS: `!event list` \n'
               ' SCHEDULE INCURSION: `!event add` \n'
               '     _EXAMPLE:_ `!event add Fraggle\'s VoG Hammer Fest|2016-9-18|19:30|raid|VoG` \n'
               '         *_note:_ the | character is a bar or pipe and is *mandatory* \n'
               '     _CREATE AN INCURSION:_ `!event add name of event|YYYY-M-D|hh:mm|type|destination` \n'
               '     _DATE/TIME:_ The date is YYY-M-D and Time is from the 24 hour clock in CST. \n'
               '     _TYPE:_ CoE, PoE, raid, crucible, strike, mission \n'
               '     _DESTINATION:_ example VoG, Reef, King\'s Fall \n'
               ' JOIN INCURSION FIRETEAM: `!event join #` << change # to the INCURSION ID to join the fireteam \n'
               ' JOIN INCURSION AS ALTERNATE: `!event alt-join #` << change # to the INCURSION ID to join the fireteam alternates\n'
               ' LEAVE INCURSION FIRETEAM: `!event leave #` << change # to the INCURSION ID to leave the fireteam  \n'
               ' LEAVE INCURSION AS ALTERNATE: `!event alt-leave #` << change # to the INCURSION ID to leave the fireteam alternates\n'
               ' DELETE INCURSION: `!event delete #` << Must be fireteam leader of the incursion.')
        return msg

    def incursion_create(self, this_author, this_event):
        this_event_id = None
        this_event_name = this_event[0]
        year, month, day = map(int, this_event[1].split('-'))
        hour, minute = map(int, this_event[2].split(':'))
        this_event_occurs = datetime.datetime(year, month, day, hour, minute)
        this_type = this_event[3]
        this_activity = this_event[4]
        slot1 = "OPEN"
        slot2 = "OPEN"
        slot3 = "OPEN"
        slot4 = "OPEN"
        slot5 = "OPEN"
        alt1 = "OPEN"
        alt2 = "OPEN"
        alt3 = "OPEN"
        # print(this_event)
        if this_event_occurs < datetime.datetime.now():
            msg = ('AI-HANDLER // {0.author.mention} // INCURSION OCCURS IN THE PAST')
            suppress = 1
        else:
            suppress = 0
        self.incursion_update(this_event_id, this_event_name, this_event_occurs, this_type,
                              this_activity, this_author, slot1, slot2, slot3, slot4, slot5,
                              alt1, alt2, alt3, suppress)
        db_event_row = self.incursion_lookup_by_name(this_event_name)
        # print("db_event_row: ", db_event_row)
        db_event_id = db_event_row.id
        msg = ('AI-HANDLER // {0.author.mention} // INCURSION ID ' + str(db_event_id) + ' \"' + str(
            this_event_name) + '\" SCHEDULED')
        return msg

    def incursion_delete(self, this_author, this_event_id):
        event = self.incursion_lookup_by_id(this_event_id)
        if this_author == event.slot_0:
            del_event = session.query(Event).filter_by(id=event.id).first()
            session.delete(event)
            session.commit()
            msg = f"AI-HANDLER // INCURSION EVENT ID {this_event_id} EXPUNGED"
        elif this_author == "":
            del_event = session.query(Event).filter_by(id=event.id).first()
            session.delete(event)
            session.commit()
            msg = 'AI-HANDLER // INCURSION EVENT EXPUNGED VIA OVERRIDE'
        else:
            msg = "AI-HANDLER // ONLY THE FIRETEAM LEADER MAY EXPUNGE AN INCURSION"
        return msg

    def incursion_list(self):
        events = self.incursion_query()
        # print(events)
        # print("len0", len(events[0]))

    def incursion_join_fireteam(self, this_author, this_event_id):
        # print('update calendar')
        event = self.incursion_lookup_by_id(this_event_id)
        guardians = {"slot_0":event.slot_0, "slot_1":event.slot_1, "slot_2":event.slot_2, "slot_3":event.slot_3, "slot_4":event.slot_4, "slot_5":event.slot_5}
        alts = {"alt_1":event.alt_1, "alt_2":event.alt_2, "alt_3":event.alt_3}
        if this_author in guardians.values() or this_author in alts.values():
            # print("exists")
            msg = 'AI-HANDLER // REQUESTING GUARDIAN ALREADY ASSIGNED TO FIRETEAM'
            return msg
        else:
            pass
        if "OPEN" not in guardians.values():
            # print('no open slots')
            # msg = 'AI-HANDLER // FIRETEAM CONTAINS MAXIMUM NUMBER OF GUARDIANS'
            if "OPEN" in alts.values():
                msg = 'AI-HANDLER // FIRETEAM CONTAINS MAXIMUM NUMBER OF GUARDIANS - ALTERNATE SLOTS OPEN'
            else:
                msg = 'AI-HANDLER // FIRETEAM CONTAINS MAXIMUM NUMBER OF GUARDIANS - ALL ALTERNATE SLOTS FILLED'
                # print(msg)
                return msg
        # FIND FIRST OPEN SLOT
        slot = ""
        for i in range(3,0,-1):
            if alts[f"alt_{i}"] != "OPEN":
                slot = f"alt_{i}"
        for i in range(5,-1,-1):
            if guardians[f"slot_{i}"] != "OPEN":
                slot = f"slot_{i}"

        if slot.starswith("alt"):
            msg = f'AI-HANDLER // GUARDIAN ASSIGNED TO FIRETEAM ALTERNATE FOR INCURSION {this_event_id}'
        elif slot.startswith("slot"):
            msg = f'AI-HANDLER // GUARDIAN ASSIGNED TO FIRETEAM FOR INCURSION {this_event_id}'

        session.query(Event).filter_by(id = event.id).update({getattr(event, slot):this_author})
        return msg

    def incursion_join_alternate(self, this_author, this_event_id):
        # print('update calendar')
        event = self.incursion_lookup_by_id(this_event_id)
        guardians = {"slot_0":event.slot_0, "slot_1":event.slot_1, "slot_2":event.slot_2, "slot_3":event.slot_3, "slot_4":event.slot_4, "slot_5":event.slot_5}
        alts = {"alt_1":event.alt_1, "alt_2":event.alt_2, "alt_3":event.alt_3}
        if this_author in guardians.values():
            # print("exists")
            msg = 'AI-HANDLER // REQUESTING GUARDIAN ALREADY ASSIGNED TO FIRETEAM'
            return msg
        elif this_author in alts.values():
            msg = 'AI-HANDLER // REQUESTING GUARDIAN ALREADY ASSIGNED TO FIRETEAM ALTERNATES'

        if "OPEN" not in alts.values():
            msg = 'AI-HANDLER // FIRETEAM CONTAINS MAXIMUM NUMBER OF GUARDIANS - ALL ALTERNATE SLOTS FILLED'
            return msg
        # FIND FIRST OPEN SLOT
        slot = ""
        for i in range(3,0,-1):
            if alts[f"alt_{i}"] != "OPEN":
                slot = f"alt_{i}"

        # We can just say the user is assigned, because we already know there is space.
        msg = f'AI-HANDLER // GUARDIAN ASSIGNED TO FIRETEAM ALTERNATE FOR INCURSION {this_event_id}'
        session.query(Event).filter_by(id = event.id).update({getattr(event, slot):this_author})
        return msg

    def incursion_leave_fireteam(self, this_author, this_event_id):
        """
        Leave the Fireteam Assigned to an Incursion
        :param self:
        :param this_author:
        :param this_event_id:
        :return:
        """
        event = self.incursion_lookup_by_id(this_event_id)
        guardians = {"slot_0":event.slot_0, "slot_1":event.slot_1, "slot_2":event.slot_2, "slot_3":event.slot_3, "slot_4":event.slot_4, "slot_5":event.slot_5}
        if this_author not in guardians.values():
            # print("exists")
            msg = 'AI-HANDLER // REQUESTING GUARDIAN NOT ASSIGNED TO FIRETEAM PRIMARIES'
            return msg

        for slot, guardian in guardians.items():
            if guardian == this_author:
                # print(slot)
                session.query(Event).filter_by(id = event.id).update({slot : "OPEN"})

        msg = f"AI-HANDLER // {this_author} REMOVED FROM FIRETEAM."
        modifiedGuardians = {"slot_0":event.slot_0, "slot_1":event.slot_1, "slot_2":event.slot_2, "slot_3":event.slot_3, "slot_4":event.slot_4, "slot_5":event.slot_5}
        
        shift_list = []
        for i in range(0,6):
            guardian = modifiedGuardians[f"slot_{i}"]
            if guardian != "OPEN":
                shift_list.append(guardian)

        if shift_list == []:
            msg = 'AI-HANDLER // NO GUARDIANS TO PROMOTE TO FIRETEAM LEADER. DELETING INCURSION.'
            self.incursion_delete("", this_event_id)
            return msg
        
        else:
            # Here we define a list of slots so that we can reshuffle the active guardians
            slots = ["slot_0", "slot_1", "slot_2", "slot_3", "slot_4", "slot_5"]
            # Now we trim the new active slot list down to size
            slots = slots[0:len(shift_list)-1]
            # Finally, iterate through the range and shuffle guardians down to the first active slots
            for i in range(len(slots)):
                if i == 0:
                    msg = f'AI-HANDLER // {shift_list[i]} PROMOTED TO FIRETEAM LEADER.'
                session.query(Event).filter_by(id = event.id).update({slots[i] : shift_list[i]})
        return msg

    def incursion_leave_alternate(self, this_author, this_event_id):
        event = self.incursion_lookup_by_id(this_event_id)
        guardians = {"alt_1":event.alt_1, "alt_2":event.alt_2, "alt_3":event.alt_3}
        if this_author not in guardians.values():
            msg = 'AI-HANDLER // REQUESTING GUARDIAN NOT ASSIGNED TO FIRETEAM ALTERNATES'
            return msg

        for slot, guardian in guardians:
            if guardian == this_author:
                session.query(Event).filter_by(id = event.id).update({slot : "OPEN"})

        msg = f"AI-HANDLER // {this_author} REMOVED FROM FIRETEAM ALTERNATES."
        modifiedGuardians = {"alt_1":event.alt_1, "alt_2":event.alt_2, "alt_3":event.alt_3}
        
        shift_list = []
        for i in range(1,4):
            guardian = modifiedGuardians[f"alt_{i}"]
            if guardian is not "OPEN":
                shift_list.append(guardian)

        if shift_list == []:
            msg = 'AI-HANDLER // NO GUARDIANS ASSIGNED AS FIRETEAM ALTERNATES.'
            return msg
        
        else:
            # Here we define a list of slots so that we can reshuffle the active guardians
            slots = ["alt_1", "alt_2", "alt_3"]
            # Now we trim the new active slot list down to size
            slots = slots[0:len(shift_list)-1]
            # Finally, iterate through the range and shuffle guardians down to the first active slots
            for i in range(len(slots)):
                session.query(Event).filter_by(id = event.id).update({slots[i] : shift_list[i]})
        return msg

    def incursion_update(self, this_event_id, this_event_name, this_event_occurs, this_type, this_activity, this_slot0,
                              this_slot1, this_slot2, this_slot3, this_slot4, this_slot5, this_alt1, this_alt2,
                              this_alt3, this_suppress):
        """
        Updates the calendar and returns the entry info
        :param self:
        :param eventDict:
        :param this_user:
        """
        eventDict = {'id':this_event_id, 'name':this_event_name, 'date':this_event_occurs, 'event_type':this_type, 'activity':this_activity, 'slot_0':this_slot0,
                     'slot_1':this_slot1, 'slot_2':this_slot2, 'slot_3':this_slot3, 'slot_4':this_slot4, 'slot_5':this_slot5, 'alt_1':this_alt1, 'alt_2':this_alt2, 'alt_3':this_alt3,
                     'suppress':this_suppress}
        # print('update calendar')
        if this_event_id is None:
            # print("id = none")
            new_event_record = Event(**eventDict)
            session.add(new_event_record)
            session.commit()
        else:
            # print("id is " + str(this_event_id))
            session.query(Event).filter_by(**eventDict).update({column: getattr(obj, column) for column in table.__table__.columns.keys()})

    def incursion_query(self, flag=-1):
        if flag == 1:
            query = session.query(Event).filter(Event.suppress != 0).all()
        elif flag == 0:
            query = session.query(Event).filter_by(suppress = 0).all()
        else:
            query = session.query(Event).filter(Event.suppress != -1).all()
        return query

    def incursion_lookup_by_id(self, event_id):
        query = session.query(Event).filter_by(id = event_id).first()
        return query

    def incursion_lookup_by_name(self, event_name):
        query = session.query(Event).filter_by(name = event_name).first()
        return query
