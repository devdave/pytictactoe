from sqlalchemy.orm.exc import NoResultFound
from stickstick.data import Board, Note

from sqlalchemy.sql import func
from stickstick.data import get_session, update_board_timestamp, datetime_to_milliseconds

import minjson as json

#document.execute('../libraries/stickstick/data/')

def handle_init(conversation):
    conversation.addMediaTypeByName('text/plain')
    conversation.addMediaTypeByName('application/json')

def handle_get(conversation):
    fresh = conversation.query['fresh'] == 'true'

    max_timestamp = None
    board_list = []
    session = get_session(application, fresh)
    try:
        try:
            boards = session.query(Board).all()
            for board in boards:
                board_list.append(board.id)
                timestamp = board.timestamp
                if max_timestamp is None or timestamp > max_timestamp:
                    max_timestamp = timestamp
        except NoResultFound:
            return None
    
        note_list = []
        try:
            notes = session.query(Note).all()
            for note in notes:
                note_list.append(note.to_dict())
        except NoResultFound:
            pass
    finally:
        session.close()

    if max_timestamp is not None:
        conversation.modificationTimestamp = datetime_to_milliseconds(max_timestamp)
    return json.write({'boards': board_list, 'notes': note_list})

def handle_get_info(conversation):
    session = get_session(application)
    try:
        max_timestamp = session.query(func.max(Board.timestamp)).scalar()
    finally:
        session.close()
    return datetime_to_milliseconds(max_timestamp)

def handle_put(conversation):
    # Note: You can only "consume" the entity once, so if we want it
    # as text, and want to refer to it more than once, we should keep
    # a reference to that text.
    
    text = conversation.entity.text
    note_dict = json.read(text)
    note = Note.create_from_dict(note_dict)
    
    session = get_session(application)
    try:
        session.add(note)
        update_board_timestamp(session, note)
        session.flush()
    finally:
        session.close()
    
    return handle_get(conversation)
