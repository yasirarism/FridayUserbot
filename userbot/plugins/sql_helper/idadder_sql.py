from sqlalchemy import (
    Column,
    String,
    Integer
)
from . import (
    SESSION,
    BASE
)


class idadder(BASE):
    """ Table to store the id """
    __tablename__ = "idadders"
    chat_id = Column(String(14))

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)  # ensure string

    def __repr__(self):
        return "<User %s>" % self.chat_id


idadder.__table__.create(checkfirst=True)

def add_usersid_in_db(chat_id: int):
    id_user = usersid(str(chat_id))
    SESSION.add(id_user)
    SESSION.commit()

def get_all_users():
    stark = SESSION.query(usersid).all()
    SESSION.close()
    return stark
