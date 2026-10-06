from books.firebase_client import db
try:
    db.collection('books').document('1').set({
        'title': 'The Firebase Guide', 'author': 'Cloud Master', 'price': 19.99,
        'category': 'Programming', 'description': 'Learn Firebase easily.',
        'stock': 10, 'image_url': 'https://firebase.google.com/downloads/brand-guidelines/PNG/logo-logomark.png'
    })
    db.collection('categories').document('Programming').set({'name': 'Programming'})
except Exception as e:
    print(e)
