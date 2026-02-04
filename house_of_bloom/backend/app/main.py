import json
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError
from sqlalchemy import delete, func, select

from app.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    oauth2_scheme,
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)
from app.db import Base, SessionLocal, engine, get_session
from app.data_loader import load_catalog
from app.models import BrowsingHistory, Category, Plant, User
from app.schemas import HistoryCreate, LoginRequest, Token, UserCreate, UserOut

app = FastAPI(title='House of Bloom API', version='0.1.0')

origins = [
    'http://localhost',
    'http://localhost:5173',
    'http://localhost:4173',
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

HERO = {
    'title': 'House of Bloom',
    'tagline': 'Curated plants for the modern home',
    'summary': 'Minimal silhouettes, refined textures, and plant care that feels personal.',
    'image': 'https://images.unsplash.com/photo-1493666438817-866a91353ca9?auto=format&fit=crop&w=1200&q=80',
    'badge': 'New season drop',
}

COLLECTIONS = [
    {
        'id': 'statement-greens',
        'title': 'Statement Greens',
        'description': 'Architectural plants for living rooms and lobbies.',
        'image': 'https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=900&q=80',
    },
    {
        'id': 'petite-corners',
        'title': 'Petite Corners',
        'description': 'Low-light companions for desks and shelves.',
        'image': 'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=900&q=80',
    },
    {
        'id': 'outdoor-reserve',
        'title': 'Outdoor Reserve',
        'description': 'Planters crafted for terraces and balconies.',
        'image': 'https://images.unsplash.com/photo-1470246973918-29a93221c455?auto=format&fit=crop&w=900&q=80',
    },
]

CARE_GUIDES = [
    {'title': 'Precise watering', 'detail': 'Light meters and gentle reminders keep you on track for every species.'},
    {'title': 'Artisan planters', 'detail': 'Ceramic, terracotta, and matte lacquer vessels from local makers.'},
    {'title': 'Delivery & setup', 'detail': 'Two-hour windows, gentle handling, and styling advice for your space.'},
]

TESTIMONIALS = [
    {
        'quote': 'House of Bloom feels like walking into a gallery. Every plant arrives wrapped with a care story.',
        'name': 'Yasmin, Mumbai',
    },
    {
        'quote': 'The care guides are the best part. No guesswork, just calm instructions.',
        'name': 'Kabir, Pune',
    },
]


def plant_to_dict(plant: Plant) -> dict:
    return {
        'id': plant.id,
        'slug': plant.slug,
        'handle': plant.handle,
        'name': plant.name,
        'description': plant.description,
        'category': plant.category.title if plant.category else plant.category_id,
        'category_id': plant.category_id,
        'type': plant.type,
        'product_category': plant.product_category,
        'tags': [tag for tag in (plant.tags or '').split(',') if tag],
        'price': plant.price,
        'inventory': plant.inventory,
        'image': plant.image,
        'vendor': plant.vendor,
        'status': plant.status,
        'light': None,
        'watering': None,
        'size': None,
    }


def category_to_dict(category: Category) -> dict:
    return {
        'id': category.id,
        'title': category.title,
        'description': category.description,
        'image': category.image,
        'product_count': category.product_count,
    }


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    try:
        payload = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    user_id = payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=401, detail='Invalid token payload')
    with SessionLocal.begin() as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=401, detail='User not found')
        return UserOut.from_orm(user)


def sync_catalog(plants: list[dict], categories: list[dict]) -> None:
    with SessionLocal.begin() as session:
        session.execute(delete(Plant))
        session.execute(delete(Category))

        for cat_data in categories:
            session.add(Category(**cat_data))

        for plant_data in plants:
            tags_serialized = ','.join(plant_data.get('tags', []))
            plant_record = Plant(
                id=plant_data['id'],
                slug=plant_data['slug'],
                handle=plant_data.get('handle'),
                name=plant_data.get('name'),
                description=plant_data.get('description'),
                category_id=plant_data.get('category_id'),
                type=plant_data.get('type'),
                product_category=plant_data.get('product_category'),
                tags=tags_serialized,
                price=plant_data.get('price') or '',
                inventory=plant_data.get('inventory', 0),
                image=plant_data.get('image', ''),
                vendor=plant_data.get('vendor'),
                status=plant_data.get('status'),
            )
            session.add(plant_record)


@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)
    plants, categories = load_catalog()
    sync_catalog(plants, categories)


@app.post('/api/auth/register', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate):
    with SessionLocal.begin() as session:
        existing = session.scalar(select(User).filter_by(email=payload.email))
        if existing:
            raise HTTPException(status_code=400, detail='Email already registered')
        user = User(email=payload.email, hashed_password=get_password_hash(payload.password))
        session.add(user)
        session.flush()
        return UserOut.from_orm(user)


@app.post('/api/auth/login', response_model=Token)
def login(payload: LoginRequest):
    with SessionLocal.begin() as session:
        user = session.scalar(select(User).filter_by(email=payload.email))
        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Invalid credentials')
    access_token = create_access_token({'user_id': user.id, 'email': user.email})
    return Token(access_token=access_token)


@app.get('/api/auth/me', response_model=UserOut)
def read_current_user(current_user: UserOut = Depends(get_current_user)):
    return current_user


@app.post('/api/history', status_code=status.HTTP_201_CREATED)
def record_history(payload: HistoryCreate, current_user: UserOut = Depends(get_current_user)) -> dict[str, Any]:
    with SessionLocal.begin() as session:
        history = BrowsingHistory(
            user_id=current_user.id,
            path=payload.path,
            referrer=payload.referrer,
            metadata=json.dumps(payload.metadata or {}),
        )
        session.add(history)
    return {'status': 'ok'}


@app.get('/api/hero')
def read_hero():
    return HERO


@app.get('/api/collections')
def read_collections():
    return COLLECTIONS


@app.get('/api/categories')
def read_categories():
    with get_session() as session:
        categories = session.scalars(select(Category)).all()
        return [category_to_dict(cat) for cat in categories]


@app.get('/api/products')
def read_products():
    with get_session() as session:
        plants = session.scalars(select(Plant)).all()
        return [plant_to_dict(p) for p in plants]


@app.get('/api/products/{product_id}')
def read_product(product_id: int):
    with get_session() as session:
        product = session.get(Plant, product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Product not found')
        return plant_to_dict(product)


@app.get('/api/search')
def search_products(q: str = ''):
    query = q.strip()
    if not query:
        return []

    like = f"%{query.lower()}%"
    with get_session() as session:
        stmt = select(Plant).where(
            func.lower(Plant.name).like(like)
            | func.lower(Plant.description).like(like)
            | func.lower(Plant.tags).like(like)
        )
        plants = session.scalars(stmt).all()
        return [plant_to_dict(p) for p in plants]


@app.get('/api/care-guides')
def read_care_guides():
    return CARE_GUIDES


@app.get('/api/testimonials')
def read_testimonials():
    return TESTIMONIALS


@app.get('/health')
def health_check():
    return {'status': 'ok'}
