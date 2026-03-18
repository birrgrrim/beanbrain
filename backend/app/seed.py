from sqlalchemy.orm import Session

from .models import BrewSetup, Descriptor, Grinder, Taster

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


def seed_database(db: Session) -> None:
    """Seed the database with initial data if tables are empty."""
    if db.query(Descriptor).first():
        return

    for category, names in DESCRIPTORS.items():
        for name in names:
            db.add(Descriptor(name=name, category=category))

    db.add(Grinder(name="Default Grinder", is_default=True))
    db.add(BrewSetup(method_type="espresso", name="Espresso", is_default=True))

    db.commit()
