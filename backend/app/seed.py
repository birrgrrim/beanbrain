from sqlalchemy.orm import Session

from .models import Descriptor, Origin

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

# (name_en, name_uk, flag)  — flag is None for regions
ORIGINS = [
    # Africa
    ("Ethiopia", "Ефіопія", "🇪🇹"),
    ("Kenya", "Кенія", "🇰🇪"),
    ("Tanzania", "Танзанія", "🇹🇿"),
    ("Rwanda", "Руанда", "🇷🇼"),
    ("Burundi", "Бурунді", "🇧🇮"),
    ("Uganda", "Уганда", "🇺🇬"),
    ("DR Congo", "ДР Конго", "🇨🇩"),
    # Central & South America
    ("Colombia", "Колумбія", "🇨🇴"),
    ("Brazil", "Бразилія", "🇧🇷"),
    ("Peru", "Перу", "🇵🇪"),
    ("Bolivia", "Болівія", "🇧🇴"),
    ("Ecuador", "Еквадор", "🇪🇨"),
    ("Costa Rica", "Коста-Ріка", "🇨🇷"),
    ("Guatemala", "Гватемала", "🇬🇹"),
    ("Honduras", "Гондурас", "🇭🇳"),
    ("El Salvador", "Сальвадор", "🇸🇻"),
    ("Nicaragua", "Нікарагуа", "🇳🇮"),
    ("Panama", "Панама", "🇵🇦"),
    ("Mexico", "Мексика", "🇲🇽"),
    ("Jamaica", "Ямайка", "🇯🇲"),
    # Asia & Pacific
    ("Indonesia", "Індонезія", "🇮🇩"),
    ("Vietnam", "В'єтнам", "🇻🇳"),
    ("India", "Індія", "🇮🇳"),
    ("Myanmar", "М'янма", "🇲🇲"),
    ("Thailand", "Таїланд", "🇹🇭"),
    ("China", "Китай", "🇨🇳"),
    ("Papua New Guinea", "Папуа Нова Гвінея", "🇵🇬"),
    ("Philippines", "Філіппіни", "🇵🇭"),
    # Middle East
    ("Yemen", "Ємен", "🇾🇪"),
    # Regions (flag = parent country's flag)
    ("Bali", "Балі", "🇮🇩"),
    ("Sumatra", "Суматра", "🇮🇩"),
    ("Java", "Ява", "🇮🇩"),
    ("Sulawesi", "Сулавесі", "🇮🇩"),
    ("Hawaii", "Гаваї", "🇺🇸"),
    ("Yunnan", "Юньнань", "🇨🇳"),
    # Unknown
    ("Unknown", "Невідомо", "🌍"),
]


def seed_database(db: Session) -> None:
    """Seed the database with initial data if tables are empty."""
    if db.query(Descriptor).first():
        return

    for category, names in DESCRIPTORS.items():
        for name in names:
            db.add(Descriptor(name=name, category=category))


    for name_en, name_uk, flag in ORIGINS:
        db.add(Origin(name_en=name_en, name_uk=name_uk, flag=flag))

    db.commit()


def seed_origins(db: Session) -> None:
    """Seed origins — adds missing ones, updates flags on existing."""
    existing = {o.name_en: o for o in db.query(Origin).all()}
    changed = False
    for name_en, name_uk, flag in ORIGINS:
        if name_en in existing:
            o = existing[name_en]
            if o.flag != flag or o.name_uk != name_uk:
                o.flag = flag
                o.name_uk = name_uk
                changed = True
        else:
            db.add(Origin(name_en=name_en, name_uk=name_uk, flag=flag))
            changed = True
    if changed:
        db.commit()
