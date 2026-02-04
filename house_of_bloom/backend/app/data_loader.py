import csv
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
PLANTS_FILE = DATA_DIR / 'plants.csv'

SLUG_RE = re.compile(r'[^a-z0-9]+')


def slugify(value: str) -> str:
    value = (value or '').strip().lower()
    value = SLUG_RE.sub('-', value)
    return value.strip('-') or 'item'


def clean_price(value: str) -> str:
    if not value:
        return ''
    cleaned = ''.join(ch for ch in value.strip() if ch.isdigit() or ch in '.,')
    if ',' in cleaned and '.' not in cleaned:
        cleaned = cleaned.replace(',', '.')
    return cleaned


def load_plants() -> list[dict]:
    if not PLANTS_FILE.exists():
        return []

    plants = []
    with PLANTS_FILE.open(newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=1):
            handle = row.get('Handle') or ''
            title = row.get('Title') or ''
            product_category = row.get('Product Category') or ''
            category_name = product_category.split('>')[-1].strip() if product_category else row.get('Type', '').strip()
            price = clean_price(row.get('Variant Price', ''))
            inventory = row.get('Variant Inventory Qty')
            try:
                inventory_qty = int(inventory)
            except (TypeError, ValueError):
                inventory_qty = 0
            image = (row.get('Image Src') or row.get('Variant Image') or '').strip()

            tags = [tag.strip() for tag in (row.get('Tags') or '').split(',') if tag.strip()]

            category_slug = slugify(category_name)
            plant = {
                'id': idx,
                'slug': slugify(handle or title),
                'handle': handle,
                'name': title,
                'description': row.get('Body (HTML)', ''),
                'category': category_name,
                'category_id': category_slug,
                'type': row.get('Type', ''),
                'product_category': product_category,
                'tags': tags,
                'price': price,
                'inventory': inventory_qty,
                'image': image,
                'vendor': row.get('Vendor', ''),
                'status': row.get('Status', ''),
            }
            plants.append(plant)
    return plants


def build_categories(plants: list[dict]) -> list[dict]:
    categories: dict[str, dict] = {}
    for plant in plants:
        name = plant.get('category') or 'general'
        key = slugify(name)
        if key not in categories:
            categories[key] = {
                'id': key,
                'title': name,
                'description': f"{name} plants curated for House of Bloom.",
                'image': plant.get('image', ''),
                'product_count': 0,
            }
        categories[key]['product_count'] += 1
    return list(categories.values())


def load_catalog() -> tuple[list[dict], list[dict]]:
    plants = load_plants()
    categories = build_categories(plants)
    return plants, categories


PLANTS, CATEGORIES = load_catalog()
