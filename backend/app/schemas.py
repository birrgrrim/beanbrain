from datetime import datetime

from pydantic import BaseModel, Field


# --- Descriptor ---

class DescriptorOut(BaseModel):
    id: int
    name: str
    category: str

    model_config = {"from_attributes": True}


# --- Taster ---

class TasterCreate(BaseModel):
    name: str


class TasterOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


# --- Equipment ---

class EquipmentCreate(BaseModel):
    type: str
    name: str
    model: str | None = None
    is_default: bool = False


class EquipmentUpdate(BaseModel):
    name: str | None = None
    model: str | None = None
    is_default: bool | None = None


class EquipmentOut(BaseModel):
    id: int
    type: str
    name: str
    model: str | None = None
    is_active: bool
    is_default: bool

    model_config = {"from_attributes": True}


# --- Brew Method ---

class BrewMethodCreate(BaseModel):
    name: str
    is_default: bool = False


class BrewMethodOut(BaseModel):
    id: int
    name: str
    is_default: bool

    model_config = {"from_attributes": True}


# --- Basket Size ---

class BasketSizeCreate(BaseModel):
    size_grams: int
    label: str
    is_default: bool = False


class BasketSizeOut(BaseModel):
    id: int
    size_grams: int
    label: str
    is_default: bool

    model_config = {"from_attributes": True}


# --- Grinder Setting ---

class GrinderSettingCreate(BaseModel):
    equipment_id: int
    brew_method_id: int
    basket_size_id: int | None = None
    setting: float
    notes: str | None = None


class GrinderSettingOut(BaseModel):
    id: int
    coffee_id: int
    equipment_id: int
    brew_method_id: int
    basket_size_id: int | None = None
    setting: float
    notes: str | None = None
    equipment: EquipmentOut
    brew_method: BrewMethodOut
    basket_size: BasketSizeOut | None = None

    model_config = {"from_attributes": True}


# --- Review ---

class ReviewUpsert(BaseModel):
    taster_id: int
    rating: int = Field(ge=1, le=10)
    comment: str | None = None
    descriptor_ids: list[int] = []


class ReviewOut(BaseModel):
    id: int
    coffee_id: int
    taster_id: int
    taster: TasterOut
    rating: int
    comment: str | None = None
    updated_at: datetime
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
    image_url: str | None = None
    score: int | None = None
    sweetness: str | None = None
    acidity: str | None = None
    bitterness: str | None = None
    notes: str | None = None
    is_available: bool = True
    roastery_descriptor_ids: list[int] = []


class CoffeeUpdate(BaseModel):
    name: str | None = None
    roastery: str | None = None
    origin: str | None = None
    process: str | None = None
    roast_level: str | None = None
    roastery_url: str | None = None
    image_url: str | None = None
    score: int | None = None
    sweetness: str | None = None
    acidity: str | None = None
    bitterness: str | None = None
    notes: str | None = None
    is_available: bool | None = None
    roastery_descriptor_ids: list[int] | None = None


class CoffeeOut(BaseModel):
    id: int
    name: str
    roastery: str
    origin: str | None = None
    process: str | None = None
    roast_level: str | None = None
    roastery_url: str | None = None
    image_url: str | None = None
    score: int | None = None
    sweetness: str | None = None
    acidity: str | None = None
    bitterness: str | None = None
    notes: str | None = None
    is_available: bool
    created_at: datetime
    roastery_descriptors: list[DescriptorOut] = []
    reviews: list[ReviewOut] = []
    grinder_settings: list[GrinderSettingOut] = []

    model_config = {"from_attributes": True}


class CoffeeListOut(BaseModel):
    id: int
    name: str
    roastery: str
    origin: str | None = None
    roast_level: str | None = None
    image_url: str | None = None
    is_available: bool
    created_at: datetime
    avg_rating: float | None = None
    person_rating: int | None = None
    default_grind: float | None = None
    roastery_descriptors: list[DescriptorOut] = []

    model_config = {"from_attributes": True}


# --- Scrape ---

class ScrapeResult(BaseModel):
    name: str
    roastery: str
    origin: str | None = None
    process: str | None = None
    roast_level: str | None = None
    roastery_url: str
    image_url: str | None = None
    score: int | None = None
    sweetness: str | None = None
    acidity: str | None = None
    bitterness: str | None = None
    flavor_descriptors: dict[str, list[str]] = {}
    name_i18n: dict[str, str] = {}
