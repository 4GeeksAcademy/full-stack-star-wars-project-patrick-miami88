from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite_characters: Mapped[List["Character"]] = relationship(secondary="favorite_characters", back_populates="favorited_by")
    favorite_planets: Mapped[List["Planet"]] = relationship(secondary="favorite_planets", back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_characters": [character.serialize() for character in self.favorite_characters],
            "favorite_planets": [planet.serialize() for planet in self.favorite_planets]
            # do not serialize the password, its a security breach
        }
favorite_characters = Table(
    "favorite_characters",
    db.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("character_id", ForeignKey("character.id"))
)

favorite_planets = Table(
    "favorite_planets",
    db.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("planet_id", ForeignKey("planet.id"))
)

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(50), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    homeworld_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    homeworld: Mapped["Planet"] = relationship(back_populates="characters")
    favorited_by: Mapped[List["User"]] = relationship(back_populates="favorite_characters", secondary="favorite_characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "homeworld": self.homeworld.serialize()
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(500), nullable=False)
    terrain: Mapped[str] = mapped_column(String(200), nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    characters: Mapped[List["Character"]] = relationship(back_populates="homeworld")
    favorited_by: Mapped[List["User"]] = relationship(back_populates="favorite_planets", secondary="favorite_planets")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "characters": [character.name for character in self.characters]
        }
    