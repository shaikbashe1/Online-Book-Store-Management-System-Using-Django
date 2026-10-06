from django.shortcuts import render, redirect
from django.contrib import messages
from .firebase_client import db, bucket

class CategoryObj:
    def __init__(self, name):
        self.name = name
        self.id = name

class BookObj:
    def __init__(self, doc_id, data):
        self.id = doc_id
        self.title = data.get('title', '')
        self.author = data.get('author', '')
        self.price = float(data.get('price', 0.0))
        self.category = CategoryObj(data.get('category', 'Unknown'))
        self.description = data.get('description', '')
        self.image_url = data.get('image_url', '')
        self.stock = int(data.get('stock', 0))

def get_all_books():
    docs = db.collection('books').stream()
    return [BookObj(doc.id, doc.to_dict()) for doc in docs]

def home(request):
    books = get_all_books()[:4]
    return render(request, 'books/home.html', {'books': books})

def book_list(request):
    books = get_all_books()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, book_id):
    doc = db.collection('books').document(book_id).get()
    if not doc.exists: return redirect('home')
    book = BookObj(doc.id, doc.to_dict())
    return render(request, 'books/book_detail.html', {'book': book})

def category_books(request, category_id):
    docs = db.collection('books').where('category', '==', category_id).stream()
    books = [BookObj(doc.id, doc.to_dict()) for doc in docs]
    return render(request, 'books/book_list.html', {'books': books, 'current_category': CategoryObj(category_id)})

def search(request):
    query = request.GET.get('q', '').lower()
    books = []
    if query:
        for b in get_all_books():
            if query in b.title.lower() or query in b.author.lower() or query in b.category.name.lower():
                books.append(b)
    return render(request, 'books/search.html', {'books': books, 'query': query})

def get_cart(request):
    if 'cart' not in request.session: request.session['cart'] = {}
    return request.session['cart']

def add_to_cart(request, book_id):
    cart = get_cart(request)
    doc = db.collection('books').document(book_id).get()
    if not doc.exists: return redirect('cart')
    book = BookObj(doc.id, doc.to_dict())
    
    if book_id in cart:
        if cart[book_id]['quantity'] < book.stock:
            cart[book_id]['quantity'] += 1
            messages.success(request, f"Increased quantity of '{book.title}'.")
        else: messages.error(request, "Not enough stock.")
    elif book.stock > 0:
        cart[book_id] = {'title': book.title, 'price': float(book.price), 'quantity': 1}
        messages.success(request, f"'{book.title}' added to cart.")
    request.session.modified = True
    return redirect('cart')

def update_cart(request, book_id, action):
    cart = get_cart(request)
    doc = db.collection('books').document(book_id).get()
    if not doc.exists or book_id not in cart: return redirect('cart')
    book = BookObj(doc.id, doc.to_dict())
    
    if action == 'increase' and cart[book_id]['quantity'] < book.stock:
        cart[book_id]['quantity'] += 1
    elif action == 'decrease':
        if cart[book_id]['quantity'] > 1: cart[book_id]['quantity'] -= 1
        else: del cart[book_id]
    request.session.modified = True
    return redirect('cart')

def remove_from_cart(request, book_id):
    cart = get_cart(request)
    if book_id in cart:
        del cart[book_id]
        request.session.modified = True
    return redirect('cart')

def clear_cart(request):
    if 'cart' in request.session: del request.session['cart']
    return redirect('cart')

def cart(request):
    cart = get_cart(request)
    cart_items = []
    total = 0
    for b_id, item in cart.items():
        sub = float(item['price']) * item['quantity']
        total += sub
        cart_items.append({'book_id': b_id, 'title': item['title'], 'price': item['price'], 'quantity': item['quantity'], 'subtotal': sub})
    return render(request, 'books/cart.html', {'cart_items': cart_items, 'total': total})

def register_user(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        if db.collection('users').document(u).get().exists:
            messages.error(request, "Username taken.")
        else:
            db.collection('users').document(u).set({'username': u, 'password': p})
            messages.success(request, "Registration successful!")
            return redirect('login')
    return render(request, 'books/register.html')

def login_user(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        doc = db.collection('users').document(u).get()
        if doc.exists and doc.to_dict().get('password') == p:
            request.session['firebase_user'] = u
            messages.success(request, f"Welcome, {u}!")
            return redirect('home')
        messages.error(request, "Invalid credentials.")
    return render(request, 'books/login.html')

def logout_user(request):
    if 'firebase_user' in request.session: del request.session['firebase_user']
    messages.success(request, "Logged out.")
    return redirect('home')
