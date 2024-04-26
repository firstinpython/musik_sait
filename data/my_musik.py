import datetime
import sqlalchemy
from .db_session import SqlalachemyBase

class Musiks_Like(SqlalachemyBase):
    __tablename__ = "musiks_like"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_musiks = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("musiks.name_musiks"))
    file_musiks = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("musiks.file_musiks"))
    like_musik = sqlalchemy.Column(sqlalchemy.Integer,default=0)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    photo_musiks = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("musiks.photo_musiks"))