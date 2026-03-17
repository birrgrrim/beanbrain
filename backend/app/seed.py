from sqlalchemy.orm import Session

from .models import BasketSize, BrewMethod, Descriptor, Equipment, Taster

DESCRIPTORS = {
    "Fruity": [
        "Berry", "Blueberry", "Strawberry", "Raspberry", "Blackberry",
        "Citrus", "Lemon", "Orange", "Grapefruit", "Lime",
        "Stone Fruit", "Peach", "Apricot", "Plum", "Cherry",
        "Tropical", "Mango", "Pineapple", "Passionfruit",
        "Apple", "Grape", "Dried Fruit", "Raisin",
    ],
    "Sweet": [
        "Chocolate", "Dark Chocolate", "Milk Chocolate", "Cocoa",
        "Caramel", "Brown Sugar", "Honey", "Maple Syrup", "Molasses",
        "Vanilla", "Toffee", "Butterscotch", "Cookies",
    ],
    "Nutty": [
        "Almond", "Hazelnut", "Walnut", "Peanut", "Cashew",
    ],
    "Spicy": [
        "Cinnamon", "Clove", "Nutmeg", "Cardamom", "Black Pepper", "Ginger",
    ],
    "Floral": [
        "Jasmine", "Rose", "Lavender", "Hibiscus", "Chamomile",
    ],
    "Herbal": [
        "Tea-like", "Mint", "Sage", "Basil", "Tobacco",
    ],
    "Roasted": [
        "Smoky", "Ashy", "Burnt", "Toasty", "Roasted Nuts",
    ],
    "Earthy": [
        "Earthy", "Woody", "Mushroom", "Cedar", "Leather",
    ],
    "Sour/Fermented": [
        "Winey", "Fermented", "Vinegar", "Sour",
    ],
    "Other": [
        "Buttery", "Creamy", "Syrupy", "Clean", "Bright", "Complex",
    ],
}

EQUIPMENT = [
    {"type": "grinder", "name": "Default Grinder", "model": None, "is_active": True},
    {"type": "machine", "name": "Default Machine", "model": None, "is_active": True},
]

BREW_METHODS = ["Espresso"]

BASKET_SIZES = [
    {"size_grams": 14, "label": "14g"},
    {"size_grams": 18, "label": "18g"},
    {"size_grams": 25, "label": "25g"},
]


def seed_database(db: Session) -> None:
    """Seed the database with initial data if tables are empty."""
    if db.query(Descriptor).first():
        return

    for category, names in DESCRIPTORS.items():
        for name in names:
            db.add(Descriptor(name=name, category=category))

    for eq in EQUIPMENT:
        db.add(Equipment(**eq))

    for method in BREW_METHODS:
        db.add(BrewMethod(name=method))

    for bs in BASKET_SIZES:
        db.add(BasketSize(**bs))

    db.commit()
