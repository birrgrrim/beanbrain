from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table, Boolean
from sqlalchemy.orm import relationship

from .database import Base

# Many-to-many: coffee <-> descriptor (roastery descriptors)
coffee_descriptor = Table(
    "coffee_descriptor",
    Base.metadata,
    Column("coffee_id", Integer, ForeignKey("coffees.id", ondelete="CASCADE"), primary_key=True),
    Column("descriptor_id", Integer, ForeignKey("descriptors.id"), primary_key=True),
)

# Many-to-many: tasting <-> descriptor (personal taste descriptors)
tasting_descriptor = Table(
    "tasting_descriptor",
    Base.metadata,
    Column("tasting_id", Integer, ForeignKey("tastings.id", ondelete="CASCADE"), primary_key=True),
    Column("descriptor_id", Integer, ForeignKey("descriptors.id"), primary_key=True),
)


class Coffee(Base):
    __tablename__ = "coffees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    roastery = Column(String, nullable=False)
    origin = Column(String, nullable=True)
    process = Column(String, nullable=True)
    roast_level = Column(String, nullable=True)
    roastery_url = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    roastery_descriptors = relationship("Descriptor", secondary=coffee_descriptor)
    tastings = relationship("Tasting", back_populates="coffee", cascade="all, delete-orphan")
    grinder_settings = relationship("GrinderSetting", back_populates="coffee", cascade="all, delete-orphan")


class Descriptor(Base):
    __tablename__ = "descriptors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)


class Tasting(Base):
    __tablename__ = "tastings"

    id = Column(Integer, primary_key=True, index=True)
    coffee_id = Column(Integer, ForeignKey("coffees.id", ondelete="CASCADE"), nullable=False)
    taster_name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)  # 1-10 (displayed as 5 stars with halves)
    comment = Column(String, nullable=True)
    tasted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    coffee = relationship("Coffee", back_populates="tastings")
    descriptors = relationship("Descriptor", secondary=tasting_descriptor)


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # "grinder" or "machine"
    name = Column(String, nullable=False)
    model = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    grinder_settings = relationship("GrinderSetting", back_populates="equipment")


class BrewMethod(Base):
    __tablename__ = "brew_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)


class GrinderSetting(Base):
    __tablename__ = "grinder_settings"

    id = Column(Integer, primary_key=True, index=True)
    coffee_id = Column(Integer, ForeignKey("coffees.id", ondelete="CASCADE"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    brew_method_id = Column(Integer, ForeignKey("brew_methods.id"), nullable=False)
    setting = Column(Float, nullable=False)
    notes = Column(String, nullable=True)

    coffee = relationship("Coffee", back_populates="grinder_settings")
    equipment = relationship("Equipment", back_populates="grinder_settings")
    brew_method = relationship("BrewMethod")
