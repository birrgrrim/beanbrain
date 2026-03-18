from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base

# Many-to-many: coffee <-> descriptor (roastery descriptors)
coffee_descriptor = Table(
    "coffee_descriptor",
    Base.metadata,
    Column("coffee_id", Integer, ForeignKey("coffees.id", ondelete="CASCADE"), primary_key=True),
    Column("descriptor_id", Integer, ForeignKey("descriptors.id"), primary_key=True),
)

# Many-to-many: review <-> descriptor (personal taste descriptors)
review_descriptor = Table(
    "review_descriptor",
    Base.metadata,
    Column("review_id", Integer, ForeignKey("reviews.id", ondelete="CASCADE"), primary_key=True),
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
    image_url = Column(String, nullable=True)
    score = Column(Integer, nullable=True)
    sweetness = Column(Integer, nullable=True)
    acidity = Column(Integer, nullable=True)
    bitterness = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    roastery_descriptors = relationship("Descriptor", secondary=coffee_descriptor)
    reviews = relationship("Review", back_populates="coffee", cascade="all, delete-orphan")
    grinder_settings = relationship("GrinderSetting", back_populates="coffee", cascade="all, delete-orphan")


class Descriptor(Base):
    __tablename__ = "descriptors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)


class Taster(Base):
    __tablename__ = "tasters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("coffee_id", "taster_id", name="uq_review_coffee_taster"),
    )

    id = Column(Integer, primary_key=True, index=True)
    coffee_id = Column(Integer, ForeignKey("coffees.id", ondelete="CASCADE"), nullable=False)
    taster_id = Column(Integer, ForeignKey("tasters.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-10 (displayed as 5 stars with halves)
    comment = Column(String, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    coffee = relationship("Coffee", back_populates="reviews")
    taster = relationship("Taster")
    descriptors = relationship("Descriptor", secondary=review_descriptor)


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # "grinder" or "machine"
    name = Column(String, nullable=False)
    model = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)

    grinder_settings = relationship("GrinderSetting", back_populates="equipment")


class BrewMethod(Base):
    __tablename__ = "brew_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    is_default = Column(Boolean, default=False)


class BasketSize(Base):
    __tablename__ = "basket_sizes"

    id = Column(Integer, primary_key=True, index=True)
    size_grams = Column(Integer, nullable=False, unique=True)
    label = Column(String, nullable=False)
    is_default = Column(Boolean, default=False)


class GrinderSetting(Base):
    __tablename__ = "grinder_settings"

    id = Column(Integer, primary_key=True, index=True)
    coffee_id = Column(Integer, ForeignKey("coffees.id", ondelete="CASCADE"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    brew_method_id = Column(Integer, ForeignKey("brew_methods.id"), nullable=False)
    basket_size_id = Column(Integer, ForeignKey("basket_sizes.id"), nullable=True)
    setting = Column(Float, nullable=False)
    notes = Column(String, nullable=True)

    coffee = relationship("Coffee", back_populates="grinder_settings")
    equipment = relationship("Equipment", back_populates="grinder_settings")
    brew_method = relationship("BrewMethod")
    basket_size = relationship("BasketSize")
