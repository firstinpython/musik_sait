import datetime
import sqlalchemy
from .db_session import SqlalachemyBase
from .Like_musik import Musiks_Like

class User(SqlalachemyBase):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True, unique=True)
    hash_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    like_musik_id = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey("musiks_like.id"))
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)