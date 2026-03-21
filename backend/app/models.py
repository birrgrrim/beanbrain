from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, JSON, String, Table, UniqueConstraint
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


# Hardcoded brew method types (not in DB)
BREW_METHOD_TYPES = {
    "espresso":    {"icon": "method-espresso.png",    "has_basket": True},
    "pourover":    {"icon": "method-pourover.png",    "has_basket": False},
    "aeropress":   {"icon": "method-aeropress.png",   "has_basket": False},
    "frenchpress": {"icon": "method-frenchpress.png", "has_basket": False},
    "moka":        {"icon": "method-moka.png",        "has_basket": False},
    "cezve":       {"icon": "method-cezve.png",       "has_basket": False},
}


class Origin(Base):
    __tablename__ = "origins"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String, nullable=False)
    name_uk = Column(String, nullable=False)
    flag = Column(String, nullable=True)  # emoji flag, null for regions


class Roastery(Base):
    __tablename__ = "roasteries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    website = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)


class Coffee(Base):
    __tablename__ = "coffees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    roastery_id = Column(Integer, ForeignKey("roasteries.id"), nullable=False)
    origin_id = Column(Integer, ForeignKey("origins.id"), nullable=True)
    process = Column(String, nullable=True)
    roast_level = Column(String, nullable=True)
    roastery_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    score = Column(Float, nullable=True)
    sweetness = Column(Integer, nullable=True)
    acidity = Column(Integer, nullable=True)
    bitterness = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    roaster_comment = Column(JSON, nullable=True)
    price = Column(Integer, nullable=True)  # retail price (whole UAH)
    price_wholesale = Column(Integer, nullable=True)  # bulk/discount price (whole UAH)
    in_stock = Column(Boolean, default=False)   # at home right now
    in_store = Column(Boolean, default=True)    # available at roastery
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, nullable=True)

    origin_ref = relationship("Origin")
    roastery_ref = relationship("Roastery")
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


class Grinder(Base):
    __tablename__ = "grinders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    model = Column(String, nullable=True)
    kind = Column(String, default="auto")  # "auto" or "manual"
    is_default = Column(Boolean, default=False)

    grinder_settings = relationship("GrinderSetting", back_populates="grinder")


class BrewSetup(Base):
    __tablename__ = "brew_setups"

    id = Column(Integer, primary_key=True, index=True)
    method_type = Column(String, nullable=False)  # key from BREW_METHOD_TYPES
    name = Column(String, nullable=False)  # user label, e.g. "Gaggia Classic 18g"
    basket_grams = Column(Integer, nullable=True)  # espresso only
    is_default = Column(Boolean, default=False)

    grinder_settings = relationship("GrinderSetting", back_populates="brew_setup")


class GrinderSetting(Base):
    __tablename__ = "grinder_settings"

    id = Column(Integer, primary_key=True, index=True)
    coffee_id = Column(Integer, ForeignKey("coffees.id", ondelete="CASCADE"), nullable=False)
    grinder_id = Column(Integer, ForeignKey("grinders.id"), nullable=False)
    brew_setup_id = Column(Integer, ForeignKey("brew_setups.id"), nullable=False)
    setting = Column(Float, nullable=False)
    notes = Column(String, nullable=True)

    coffee = relationship("Coffee", back_populates="grinder_settings")
    grinder = relationship("Grinder", back_populates="grinder_settings")
    brew_setup = relationship("BrewSetup", back_populates="grinder_settings")
