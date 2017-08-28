import datetime
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

APP_PATH = "/etc/warmind_forge"
DB_PATH = f"{APP_PATH}/events.db"
Engine = create_engine(f"sqlite:///{DB_PATH}")#, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Events(Base):
    __tablename__ = 'events'
    id = Column(String(50), primary_key=True)
    event_name = Column(String(50))
    event_date = Column(DateTime)
    event_type = Column(String(50))
    event_activity = Column(String(50))
    slot_0 = Column(String(50))
    slot_1 = Column(String(50))
    slot_2 = Column(String(50))
    slot_3 = Column(String(50))
    slot_4 = Column(String(50))
    slot_5 = Column(String(50))
    alt_1 = Column(String(50))
    alt_2 = Column(String(50))
    alt_3 = Column(String(50))
    isPastEvent = Column(Boolean)

def initdb():
    Base.metadata.bind = Engine
    Base.metadata.create_all(engine)

def expired_calendar_cleanup():
    # identify events older than 1 day and suppress them
    date_yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    # print("date yesterday: ", date_yesterday)
    conn = sqlite3.connect(sqlite_warmind)
    c = conn.cursor()
    query = 'SELECT * FROM calendar'
    c.execute(query)
    out = c.fetchall()
    conn.close()
    print(out)
    for row in out:
        this_list = list(row)
        date_object = this_list[2]
        this_date = datetime.datetime.strptime(date_object, '%Y-%m-%d %H:%M:%S')
        # print("this date: ", this_date)
        if this_date < date_yesterday:
            # print("Less than")
            this_list[11] = 1
            # print(this_list)
            self.incursion_update(this_list[0], this_list[1], this_list[2], this_list[3], this_list[4],
                                    this_list[5], this_list[6], this_list[7], this_list[8], this_list[9],
                                    this_list[10], this_list[11], this_list[12], this_list[13], this_list[14])
        else:
            this_list[11] = 0
            # print(this_list)
            self.incursion_update(this_list[0], this_list[1], this_list[2], this_list[3], this_list[4],
                                    this_list[5], this_list[6], this_list[7], this_list[8], this_list[9],
                                    this_list[10], this_list[11], this_list[12], this_list[13], this_list[14])

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
            '         *_note:_ the | character is a bar or pipe. shift+backspace and is *mandatory* \n'
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
    print(this_event)
    if this_event_occurs < datetime.datetime.now():
        msg = ('AI-HANDLER // {0.author.mention} // INCURSION OCCURS IN THE PAST')
        suppress = 1
    else:
        suppress = 0
    self.incursion_update(this_event_id, this_event_name, this_event_occurs, this_type,
                            this_activity, this_author, slot1, slot2, slot3, slot4, slot5,
                            alt1, alt2, alt3, suppress)
    db_event_row = self.incursion_lookup_by_name(this_event_name)
    print("db_event_row: ", db_event_row)
    db_event_id = db_event_row[0]
    msg = ('AI-HANDLER // {0.author.mention} // INCURSION ID ' + str(db_event_id) + ' \"' + str(
        this_event_name) + '\" SCHEDULED')
    return msg

def incursion_delete(self, event_id):
    query = '''DELETE FROM calendar WHERE event_id=?'''
    conn = sqlite3.connect(sqlite_warmind)
    c = conn.cursor()
    c.execute(query, (event_id,))
    conn.commit()
    conn.close()
    pass

def incursion_list(self):
    events = self.incursion_query()
    # print(events)
    # print("len0", len(events[0]))
    pass

def incursion_join_fireteam(self, this_author, this_event_id):
    # print('update calendar')
    event_row = self.incursion_lookup_by_id(this_event_id)
    if this_author in event_row[5:10]:
        # print("exists")
        msg = 'AI-HANDLER // REQUESTING GUARDIAN ALREADY ASSIGNED TO FIRETEAM'
        return msg
    else:
        pass
    if "OPEN" not in event_row[5:10]:
        # print('no open slots')
        # msg = 'AI-HANDLER // FIRETEAM CONTAINS MAXIMUM NUMBER OF GUARDIANS'
        if "OPEN" in event_row[11:13]:
            msg = 'AI-HANDLER // FIRETEAM CONTAINS MAXIMUM NUMBER OF GUARDIANS - ALTERNATE SLOTS OPEN'
        else:
            msg = 'AI-HANDLER // FIRETEAM CONTAINS MAXIMUM NUMBER OF GUARDIANS - ALL ALTERNATE SLOTS FILLED'
            print(msg)
            return msg
    # FIND FIRST OPEN SLOT
    sentinel = 5
    for slot in event_row[5:13]:
        # print(sentinel)
        if slot != "OPEN":
            sentinel += 1
        else:
            break
    event_row_list = list(event_row)
    # print("SENTINEL: ", sentinel)
    if 5 <= sentinel <= 10:
        msg = 'AI-HANDLER // GUARDIAN ASSIGNED TO FIRETEAM FOR INCURSION ' + str(this_event_id)
    elif 11 <= sentinel <= 13:
        msg = 'AI-HANDLER // GUARDIAN ASSIGNED TO FIRETEAM ALTERNATE FOR INCURSION ' + str(this_event_id)
    event_row_list[sentinel] = this_author
    # print('final event row: ', event_row_list)
    this_event_id = event_row_list[0]
    this_event_name = event_row_list[1]
    this_event_occurs = event_row_list[2]
    this_type = event_row_list[3]
    this_activity = event_row_list[4]
    this_user = event_row_list[5]
    slot1 = event_row_list[6]
    slot2 = event_row_list[7]
    slot3 = event_row_list[8]
    slot4 = event_row_list[9]
    slot5 = event_row_list[10]
    alt1 = event_row_list[11]
    alt2 = event_row_list[12]
    alt3 = event_row_list[13]
    suppress = event_row_list[14]
    # print(this_event_id, this_event_name, this_event_occurs, this_type, this_activity, this_user, slot1, slot2, slot3, slot4, slot5, alt1, alt2, alt3, suppress)
    self.incursion_update(this_event_id, this_event_name, this_event_occurs, this_type, this_activity, this_user,
                            slot1, slot2, slot3, slot4, slot5, alt1, alt2, alt3, suppress)
    print(msg)
    return msg

def incursion_join_alternate(self, this_author, this_event_id):
    # print('update calendar')
    event_row = self.incursion_lookup_by_id(this_event_id)
    if this_author in event_row[5:10]:
        msg = 'AI-HANDLER // REQUESTING GUARDIAN ALREADY ASSIGNED TO FIRETEAM'
        print(msg)
        return msg
    elif this_author in event_row[11:14]:
        msg = 'AI-HANDLER // REQUESTING GUARDIAN ALREADY ASSIGNED TO FIRETEAM ALTERNATES'
        print(msg)
        return msg
    else:
        pass
    if "OPEN" not in event_row[11:14]:
        msg = 'AI-HANDLER // FIRETEAM CONTAINS MAXIMUM NUMBER OF GUARDIANS - ALL ALTERNATE SLOTS FILLED'
        print(msg)
        return msg
    # FIND FIRST OPEN SLOT
    sentinel = 11
    for slot in event_row[11:13]:
        print(sentinel)
        if slot != "OPEN":
            sentinel += 1
        else:
            break
    event_row_list = list(event_row)
    print("SENTINEL: ", sentinel)
    if 5 <= sentinel <= 10:
        msg = 'AI-HANDLER // GUARDIAN ASSIGNED TO FIRETEAM FOR INCURSION ' + str(this_event_id)
    elif 11 <= sentinel <= 13:
        msg = 'AI-HANDLER // GUARDIAN ASSIGNED TO FIRETEAM ALTERNATE FOR INCURSION ' + str(this_event_id)
    event_row_list[sentinel] = this_author
    # print('final event row: ', event_row_list)
    this_event_id = event_row_list[0]
    this_event_name = event_row_list[1]
    this_event_occurs = event_row_list[2]
    this_type = event_row_list[3]
    this_activity = event_row_list[4]
    this_user = event_row_list[5]
    slot1 = event_row_list[6]
    slot2 = event_row_list[7]
    slot3 = event_row_list[8]
    slot4 = event_row_list[9]
    slot5 = event_row_list[10]
    alt1 = event_row_list[11]
    alt2 = event_row_list[12]
    alt3 = event_row_list[13]
    suppress = event_row_list[14]
    # print(this_event_id, this_event_name, this_event_occurs, this_type, this_activity, this_user, slot1, slot2, slot3, slot4, slot5, alt1, alt2, alt3, suppress)
    self.incursion_update(this_event_id, this_event_name, this_event_occurs, this_type, this_activity, this_user,
                            slot1, slot2, slot3, slot4, slot5, alt1, alt2, alt3, suppress)
    print(msg)
    return msg

def incursion_leave_fireteam(self, this_author, this_event_id):
    """
    Leave the Fireteam Assigned to an Incursion
    :param self:
    :param this_author:
    :param this_event_id:
    :return:
    """
    event_row = self.incursion_lookup_by_id(this_event_id)
    if this_author not in event_row:
        msg = 'AI-HANDLER // REQUESTING GUARDIAN NOT ASSIGNED TO FIRETEAM'
        return
    else:
        pass
    open_slot = 0
    lowest_populated_slot = 0
    event_row_list = list(event_row)
    open_indices = [i for i, x in enumerate(event_row_list[5:11]) if x == "OPEN"]
    used_indices = [i for i, x in enumerate(event_row_list[5:11]) if x != "OPEN"]
    quitter = event_row_list.index(this_author)
    msg = "AI-HANDLER // ERROR"
    if len(used_indices) <= 1:
        msg = 'AI-HANDLER // NO GUARDIANS TO PROMOTE TO FIRETEAM LEADER. DELETING INCURSION.'
        self.incursion_delete(this_event_id)
        return msg
    if min(used_indices) == 0:
        index_user = used_indices.index(min(used_indices)) + 1
    else:
        index_user = min(used_indices)
    new_fireteam_leader = int(index_user) + 5
    for each in used_indices:
        if quitter == 5 and each == 0:
            # print("New Fire Team Leader: ", event_row_list[new_fireteam_leader])
            event_row_list[5] = event_row_list[new_fireteam_leader]
            event_row_list[new_fireteam_leader] = "OPEN"
            msg = 'AI-HANDLER // ' + event_row_list[5] + ' PROMOTED TO FIRETEAM LEADER.'
            # print(msg)
    open_indices = [i for i, x in enumerate(event_row_list[5:11]) if x == "OPEN"]
    used_indices = [i for i, x in enumerate(event_row_list[5:11]) if x != "OPEN"]
    print(event_row_list)
    for each in used_indices:
        if each == quitter and quitter != 5:
            event_row_list[quitter] = "OPEN"
            msg = 'AI-HANDLER // ' + this_author + ' REMOVED FROM FIRETEAM.'
            # print(msg)
        else:
            pass
    used_indices = [i for i, x in enumerate(event_row_list[5:11]) if x != "OPEN"]
    print(event_row_list)
    for each in used_indices:
        open_indices = [i for i, x in enumerate(event_row_list[5:11]) if x == "OPEN"]
        if open_indices != None and each != 0:
            event_row_list[(open_indices[0]) + 5] = event_row_list[each + 5]
            event_row_list[each + 5] = "OPEN"
    this_event_id = event_row_list[0]
    this_event_name = event_row_list[1]
    this_event_occurs = event_row_list[2]
    this_type = event_row_list[3]
    this_activity = event_row_list[4]
    this_slot0 = event_row_list[5]
    this_slot1 = event_row_list[6]
    this_slot2 = event_row_list[7]
    this_slot3 = event_row_list[8]
    this_slot4 = event_row_list[9]
    this_slot5 = event_row_list[10]
    this_alt1 = event_row_list[11]
    this_alt2 = event_row_list[12]
    this_alt3 = event_row_list[13]
    this_suppress = event_row_list[14]
    self.incursion_update(this_event_id, this_event_name, this_event_occurs, this_type, this_activity, this_slot0,
                            this_slot1, this_slot2, this_slot3, this_slot4, this_slot5, this_alt1, this_alt2,
                            this_alt3, this_suppress)
    return msg

def incursion_leave_alternate(self, this_author, this_event_id):
    event_row = self.incursion_lookup_by_id(this_event_id)
    if this_author not in event_row:
        msg = 'AI-HANDLER // REQUESTING GUARDIAN NOT ASSIGNED TO FIRETEAM'
        return
    else:
        pass
    event_row_list = list(event_row)
    open_indices = [i for i, x in enumerate(event_row_list[11:14]) if x == "OPEN"]
    used_indices = [i for i, x in enumerate(event_row_list[11:14]) if x != "OPEN"]
    quitter = event_row_list.index(this_author)
    msg = "AI-HANDLER // ERROR"
    if len(used_indices) < 1:
        msg = 'AI-HANDLER // NO GUARDIANS ARE ALTERNATES ON THIS INCURSION.'
        exit(0)
    event_row_list[quitter] = "OPEN"
    msg = 'AI-HANDLER // ' + this_author + ' REMOVED FROM INCURSION ALTERNATES.'
    used_indices = [i for i, x in enumerate(event_row_list[11:14]) if x != "OPEN"]
    for each in used_indices:
        open_indices = [i for i, x in enumerate(event_row_list[11:14]) if x == "OPEN"]
        if open_indices != None:
            this_each = each + 11
            this_index = open_indices[0] + 11
            event_row_list[this_index] = event_row_list[this_each]
            event_row_list[each + 11] = "OPEN"
    this_event_id = event_row_list[0]
    this_event_name = event_row_list[1]
    this_event_occurs = event_row_list[2]
    this_type = event_row_list[3]
    this_activity = event_row_list[4]
    this_slot0 = event_row_list[5]
    this_slot1 = event_row_list[6]
    this_slot2 = event_row_list[7]
    this_slot3 = event_row_list[8]
    this_slot4 = event_row_list[9]
    this_slot5 = event_row_list[10]
    this_alt1 = event_row_list[11]
    this_alt2 = event_row_list[12]
    this_alt3 = event_row_list[13]
    this_suppress = event_row_list[14]
    self.incursion_update(this_event_id, this_event_name, this_event_occurs, this_type, this_activity, this_slot0,
                            this_slot1, this_slot2, this_slot3, this_slot4, this_slot5, this_alt1, this_alt2,
                            this_alt3, this_suppress)
    return msg

def incursion_update(self, this_event_id, this_event_name, this_event_occurs, this_type, this_activity, this_user,
                        slot1, slot2, slot3, slot4, slot5, alt1, alt2, alt3, suppress):
    """
    Updates the calendar and returns the entry info
    :param self:
    :param this_event_id:
    :param this_event_name:
    :param this_event_occurs:
    :param this_type:
    :param this_activity:
    :param this_user:
    :param slot1:
    :param slot2:
    :param slot3:
    :param slot4:
    :param slot5:
    :param alt1:
    :param alt2:
    :param alt3:
    :param suppress:
    """
    print('update calendar')
    conn = sqlite3.connect(sqlite_warmind)
    if this_event_id is None:
        print("id = none")
        query = "INSERT INTO calendar (event_id, event_name, event_date, event_type, event_activity, slot0, slot1, slot2, slot3, slot4, slot5, alt1, alt2, alt3, suppress) VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        key = this_event_name, this_event_occurs, this_type, this_activity, this_user, slot1, slot2, slot3, slot4, slot5, alt1, alt2, alt3, suppress
        # print(key)
    else:
        print("id is " + str(this_event_id))
        query = "UPDATE calendar SET event_name=?, event_date=?, event_type=?, event_activity=?, slot0=?, slot1=?, slot2=?, slot3=?, slot4=?, slot5=?, alt1=?, alt2=?, alt3=?, suppress=? WHERE event_id=?"
        key = this_event_name, this_event_occurs, this_type, this_activity, this_user, slot1, slot2, slot3, slot4, slot5, alt1, alt2, alt3, suppress, this_event_id
        print(key)
    cur = conn.cursor()
    cur.execute(query, key)
    # print('update calendar: query executed')
    cur.close()
    conn.commit()
    conn.close()

def incursion_query(self, flag):
    conn = sqlite3.connect(sqlite_warmind)
    c = conn.cursor()
    if flag == 1:
        query = '''SELECT event_id, event_name, event_date, event_type, event_activity, slot0, slot1, slot2, slot3, slot4, slot5, alt1, alt2, alt3, suppress FROM calendar WHERE suppress IS NOT 0 '''
    elif flag == 0:
        query = '''SELECT event_id, event_name, event_date, event_type, event_activity, slot0, slot1, slot2, slot3, slot4, slot5, alt1, alt2, alt3, suppress FROM calendar WHERE suppress IS 0'''
    else:
        query = '''SELECT event_id, event_name, event_date, event_type, event_activity, slot0, slot1, slot2, slot3, slot4, slot5, alt1, alt2, alt3, suppress FROM calendar WHERE suppress IS NOT -1 '''
    c.execute(query)
    out = c.fetchall()
    conn.close()
    return out

def incursion_lookup_by_id(self, event_id):
    conn = sqlite3.connect(sqlite_warmind)
    c = conn.cursor()
    query = 'SELECT * FROM calendar WHERE event_id =' + event_id
    c.execute(query)
    out = c.fetchone()
    conn.close()
    return out

def incursion_lookup_by_name(self, event_name):
    conn = sqlite3.connect(sqlite_warmind)
    c = conn.cursor()
    query = 'SELECT * FROM calendar WHERE event_name =\"' + event_name + '\"'
    c.execute(query)
    out = c.fetchone()
    conn.close()
    return out
