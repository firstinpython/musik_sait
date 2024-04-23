import datetime
import sqlalchemy
from .db_session import SqlalachemyBase

class Musiks(SqlalachemyBase):
    __tablename__ = "musiks_like"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_musiks = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    file_musiks = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    like_musik = sqlalchemy.Column(sqlalchemy.Integer,default=0)