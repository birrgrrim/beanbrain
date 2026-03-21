from datetime import datetime

from typing import Literal

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


# --- Origin ---

class OriginOut(BaseModel):
    id: int
    name_en: str
    name_uk: str
    flag: str | None = None

    model_config = {"from_attributes": True}


# --- Roastery ---

class RoasteryCreate(BaseModel):
    name: str
    website: str | None = None
    logo_url: str | None = None


class RoasteryUpdate(BaseModel):
    name: str | None = None
    website: str | None = None
    logo_url: str | None = None
    is_active: bool | None = None


class RoasteryOut(BaseModel):
    id: int
    name: str
    website: str | None = None
    logo_url: str | None = None
    is_active: bool

    model_config = {"from_attributes": True}


# --- Grinder ---

class GrinderCreate(BaseModel):
    name: str
    model: str | None = None
    kind: Literal["auto", "manual"] = "auto"
    is_default: bool = False
    range_min: float = 0
    range_max: float | None = None
    step: float = 1


class GrinderUpdate(BaseModel):
    name: str | None = None
    model: str | None = None
    kind: Literal["auto", "manual"] | None = None
    is_default: bool | None = None
    range_min: float | None = None
    range_max: float | None = None
    step: float | None = None


class GrinderOut(BaseModel):
    id: int
    name: str
    model: str | None = None
    kind: str
    is_default: bool
    range_min: float
    range_max: float | None = None
    step: float

    model_config = {"from_attributes": True}


# --- Brew Setup ---

class BrewSetupCreate(BaseModel):
    method_type: Literal["espresso", "pourover", "aeropress", "frenchpress", "moka", "cezve"]
    name: str
    basket_grams: int | None = None
    is_default: bool = False


class BrewSetupUpdate(BaseModel):
    name: str | None = None
    basket_grams: int | None = None
    is_default: bool | None = None


class BrewSetupOut(BaseModel):
    id: int
    method_type: str
    name: str
    basket_grams: int | None = None
    is_default: bool

    model_config = {"from_attributes": True}


# --- Brew Method Type (hardcoded, not DB) ---

class BrewMethodTypeOut(BaseModel):
    key: str
    icon: str
    has_basket: bool


# --- Grinder Setting ---

class GrinderSettingCreate(BaseModel):
    grinder_id: int
    brew_setup_id: int
    setting: float
    notes: str | None = None


class GrinderSettingOut(BaseModel):
    id: int
    coffee_id: int
    grinder_id: int
    brew_setup_id: int
    setting: float
    notes: str | None = None
    grinder: GrinderOut
    brew_setup: BrewSetupOut

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
    roastery_id: int
    origin_id: int | None = None
    process: str | None = None
    roast_level: str | None = None
    roastery_url: str | None = None
    image_url: str | None = None
    score: float | None = None
    sweetness: int | None = None
    acidity: int | None = None
    bitterness: int | None = None
    notes: str | None = None
    roaster_comment: dict[str, str] | None = None
    price: int | None = None
    price_wholesale: int | None = None
    in_stock: bool = False
    in_store: bool = True
    roastery_descriptor_ids: list[int] = []


class CoffeeUpdate(BaseModel):
    name: str | None = None
    roastery_id: int | None = None
    origin_id: int | None = None
    process: str | None = None
    roast_level: str | None = None
    roastery_url: str | None = None
    image_url: str | None = None
    score: float | None = None
    sweetness: int | None = None
    acidity: int | None = None
    bitterness: int | None = None
    notes: str | None = None
    roaster_comment: dict[str, str] | None = None
    price: int | None = None
    price_wholesale: int | None = None
    in_stock: bool | None = None
    in_store: bool | None = None
    roastery_descriptor_ids: list[int] | None = None


class CoffeeOut(BaseModel):
    id: int
    name: str
    roastery_id: int
    origin_id: int | None = None
    origin_ref: OriginOut | None = None
    roastery_ref: RoasteryOut
    process: str | None = None
    roast_level: str | None = None
    roastery_url: str | None = None
    image_url: str | None = None
    score: float | None = None
    sweetness: int | None = None
    acidity: int | None = None
    bitterness: int | None = None
    notes: str | None = None
    roaster_comment: dict[str, str] | None = None
    price: int | None = None
    price_wholesale: int | None = None
    in_stock: bool
    in_store: bool
    created_at: datetime
    updated_at: datetime | None = None
    fetched_at: datetime | None = None
    roastery_descriptors: list[DescriptorOut] = []
    reviews: list[ReviewOut] = []
    grinder_settings: list[GrinderSettingOut] = []

    model_config = {"from_attributes": True}


class CoffeeListOut(BaseModel):
    id: int
    name: str
    roastery_id: int
    origin_id: int | None = None
    origin_ref: OriginOut | None = None
    roastery_ref: RoasteryOut | None = None
    roast_level: str | None = None
    image_url: str | None = None
    price: int | None = None
    price_wholesale: int | None = None
    in_stock: bool
    in_store: bool
    created_at: datetime
    avg_rating: float | None = None
    person_rating: int | None = None
    default_grind: float | None = None
    default_grind_step: float = 1
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
    score: float | None = None
    sweetness: int | None = None
    acidity: int | None = None
    bitterness: int | None = None
    price: int | None = None
    price_wholesale: int | None = None
    flavor_descriptors: dict[str, list[str]] = {}
    name_i18n: dict[str, str] = {}
    roaster_comment: dict[str, str] = {}
