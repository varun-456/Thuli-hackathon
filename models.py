from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Initialize base for declarative models
Base = declarative_base()

# Define the Occasion model
class Occasion(Base):
    __tablename__ = 'occasion'
    occasion_id = Column(Integer, primary_key=True)
    occasion_name = Column(String)
    formality_level = Column(String)

    # Relationships
    outfits = relationship("Outfit", back_populates="occasion")
    accessories = relationship("Accessories", back_populates="occasion")

# Define the Outfit model
class Outfit(Base):
    __tablename__ = 'outfit'
    outfit_id = Column(Integer, primary_key=True)
    outfit_type = Column(String)
    occasion_id = Column(Integer, ForeignKey('occasion.occasion_id'))
    formality_level = Column(String)
    color_suggestions = Column(String)
    fabric_suggestions = Column(String)
    style = Column(String)
    gender = Column(String)

    # Relationships
    occasion = relationship("Occasion", back_populates="outfits")
    accessories = relationship("Accessories", back_populates="outfit")

# Define the Accessories model
class Accessories(Base):
    __tablename__ = 'accessories'
    accessory_id = Column(Integer, primary_key=True)
    outfit_id = Column(Integer, ForeignKey('outfit.outfit_id'))
    occasion_id = Column(Integer, ForeignKey('occasion.occasion_id'))
    accessories = Column(String)

    # Relationships
    outfit = relationship("Outfit", back_populates="accessories")
    occasion = relationship("Occasion", back_populates="accessories")
