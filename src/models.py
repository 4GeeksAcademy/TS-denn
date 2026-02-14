from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Column, Table

db = SQLAlchemy()
# le he puesto comentarios a este codigo porque voy a volver en un futuro :)
favorite_table = Table(
    "favorites",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    favorites: Mapped[list["Character"]] = db.relationship(
        "Character",
        secondary=favorite_table,
        # relacion bideccional con character :') se llenan estas tablas.
        back_populates="favorites_by")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "favorites": self.favorites
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    quote: Mapped[str] = mapped_column(String(200), unique=True, nullable=True)
    
#relcion 1-n entre charater y location:
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))  # n
    location: Mapped["Location"] = relationship(back_populates="character_location")

#relacion many to many entre character y user:
    favorites_by: Mapped[list[User]] = db.relationship(
        "User",
        secondary=favorite_table,# relacion bideccional con user :')))))
        back_populates="favorites")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "quote": self.quote,
            "location_id": self.location.serialize() if self.location else None
        }


class Location(db.Model):  # una locacion puede tener varios personajes, pero un personaje solo puede estar en una locacion 1=locacion n=personajes
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=True)
    character_location: Mapped[list["Character"]] = relationship("Character", back_populates="location")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            #"character_location": self.character_location
        }
