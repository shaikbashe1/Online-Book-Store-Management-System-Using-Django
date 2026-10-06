import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_book_store.settings")
django.setup()

from django.contrib.auth.models import User
from books.models import Category, Book

# 1. Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin / admin123")

# 2. Create Categories
categories = ['Programming', 'Database', 'Artificial Intelligence', 'Fiction', 'Mathematics', 'Computer Science']
cat_objects = {}
for cat_name in categories:
    cat, created = Category.objects.get_or_create(name=cat_name)
    cat_objects[cat_name] = cat
print("Categories created.")

# 3. Create Books
books_data = [
    {
        'title': 'Python Crash Course',
        'author': 'Eric Matthes',
        'price': 29.99,
        'category': 'Programming',
        'description': 'A hands-on, project-based introduction to programming.',
        'stock': 15
    },
    {
        'title': 'Designing Data-Intensive Applications',
        'author': 'Martin Kleppmann',
        'price': 35.50,
        'category': 'Database',
        'description': 'The big ideas behind reliable, scalable, and maintainable systems.',
        'stock': 8
    },
    {
        'title': 'Artificial Intelligence: A Modern Approach',
        'author': 'Stuart Russell',
        'price': 79.99,
        'category': 'Artificial Intelligence',
        'description': 'The standard textbook on artificial intelligence.',
        'stock': 5
    },
    {
        'title': 'Clean Code',
        'author': 'Robert C. Martin',
        'price': 42.00,
        'category': 'Computer Science',
        'description': 'A Handbook of Agile Software Craftsmanship.',
        'stock': 20
    },
    {
        'title': "The Hitchhiker's Guide to the Galaxy",
        'author': 'Douglas Adams',
        'price': 12.99,
        'category': 'Fiction',
        'description': 'Seconds before the Earth is demolished to make way for a galactic freeway.',
        'stock': 50
    },
]

for book_data in books_data:
    category = cat_objects[book_data.pop('category')]
    book, created = Book.objects.get_or_create(title=book_data['title'], category=category, defaults=book_data)
    if created:
        print(f"Created book: {book.title}")

print("Database populated successfully!")
