from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

# Define the base class for all models
Base = DeclarativeBase()

class datetime(Base):
    pass

class dewpoint(Base):
    pass

class humidity(Base):
    pass

class location(Base):
    pass

class precipitation(Base):
    pass

class temperature(Base):
    pass

class wind(Base):
    pass