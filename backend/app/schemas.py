from datetime import datetime

from pydantic import BaseModel, Field


# --- Descriptor ---

class DescriptorOut(BaseModel):
    id: int
    name: str
    category: str

    model_config = {"from_attributes": True}


# --- Equipment ---

class EquipmentOut(BaseModel):
    id: int
    type: str
    name: str
    model: str | None = None
    is_active: bool

    model_config = {"from_attributes": True}


# --- Brew Method ---

class BrewMethodOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


# --- Grinder Setting ---

class GrinderSettingCreate(BaseModel):
    equipment_id: int
    brew_method_id: int
    setting: float
    notes: str | None = None


class GrinderSettingOut(BaseModel):
    id: int
    coffee_id: int
    equipment_id: int
    brew_method_id: int
    setting: float
    notes: str | None = None
    equipment: EquipmentOut
    brew_method: BrewMethodOut

    model_config = {"from_attributes": True}


# --- Tasting ---

class TastingCreate(BaseModel):
    taster_name: str
    rating: int = Field(ge=1, le=10)
    comment: str | None = None
    descriptor_ids: list[int] = []


class TastingOut(BaseModel):
    id: int
    coffee_id: int
    taster_name: str
    rating: int
    comment: str | None = None
    tasted_at: datetime
    descriptors: list[DescriptorOut] = []

    model_config = {"from_attributes": True}


# --- Coffee ---

class CoffeeCreate(BaseModel):
    name: str
    roastery: str
    origin: str | None = None
    process: str | None = None
    roast_level: str | None = None
    roastery_url: str | None = None
    notes: str | None = None
    roastery_descriptor_ids: list[int] = []


class CoffeeUpdate(BaseModel):
    name: str | None = None
    roastery: str | None = None
    origin: str | None = None
    process: str | None = None
    roast_level: str | None = None
    roastery_url: str | None = None
    notes: str | None = None
    roastery_descriptor_ids: list[int] | None = None


class CoffeeOut(BaseModel):
    id: int
    name: str
    roastery: str
    origin: str | None = None
    process: str | None = None
    roast_level: str | None = None
    roastery_url: str | None = None
    notes: str | None = None
    created_at: datetime
    roastery_descriptors: list[DescriptorOut] = []
    tastings: list[TastingOut] = []
    grinder_settings: list[GrinderSettingOut] = []

    model_config = {"from_attributes": True}


class CoffeeListOut(BaseModel):
    id: int
    name: str
    roastery: str
    origin: str | None = None
    roast_level: str | None = None
    created_at: datetime
    roastery_descriptors: list[DescriptorOut] = []

    model_config = {"from_attributes": True}
