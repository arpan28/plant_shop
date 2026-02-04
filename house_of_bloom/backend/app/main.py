from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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

PRODUCTS = [
    {
        'id': 1,
        'name': 'Fiddle Leaf Fig',
        'price': '₹3,900',
        'description': 'Bold, sculptural leaves that make the whole room feel calm.',
        'light': 'Bright indirect',
        'watering': 'Once a week',
        'size': 'Medium',
        'images': ['https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1000&q=80'],
    },
    {
        'id': 2,
        'name': 'Sansevieria Trifasciata',
        'price': '₹2,200',
        'description': 'Almost indestructible, with elegant vertical stripes.',
        'light': 'Filtered sun',
        'watering': 'Every 10 days',
        'size': 'Small',
        'images': ['https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1000&q=80'],
    },
    {
        'id': 3,
        'name': 'Monstera Deliciosa',
        'price': '₹3,600',
        'description': 'Iconic fenestrated leaves that play well with light.',
        'light': 'Bright indirect',
        'watering': 'Once a week',
        'size': 'Large',
        'images': ['https://images.unsplash.com/photo-1472214103451-9374bd1c798e?auto=format&fit=crop&w=1000&q=80'],
    },
    {
        'id': 4,
        'name': 'Pothos Marble Queen',
        'price': '₹1,800',
        'description': 'Trailing greenery with creamy variegation.',
        'light': 'Low to medium',
        'watering': 'Every 7–9 days',
        'size': 'Small',
        'images': ['https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1000&q=80'],
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

@app.get('/api/hero')
def read_hero():
    return HERO


@app.get('/api/collections')
def read_collections():
    return COLLECTIONS


@app.get('/api/products')
def read_products():
    return PRODUCTS


@app.get('/api/products/{product_id}')
def read_product(product_id: int):
    product = next((item for item in PRODUCTS if item['id'] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    return product


@app.get('/api/care-guides')
def read_care_guides():
    return CARE_GUIDES


@app.get('/api/testimonials')
def read_testimonials():
    return TESTIMONIALS
