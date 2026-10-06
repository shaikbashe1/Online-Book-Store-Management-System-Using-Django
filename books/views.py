from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Book, Category

def home(request):
    books = Book.objects.all()[:4] # Display top 4 books
    return render(request, 'books/home.html', {'books': books})

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

def category_books(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(category=category)
    return render(request, 'books/book_list.html', {'books': books, 'current_category': category})

def search(request):
    query = request.GET.get('q')
    books = []
    if query:
        books = Book.objects.filter(title__icontains=query) | \
                Book.objects.filter(author__icontains=query) | \
                Book.objects.filter(category__name__icontains=query)
        books = books.distinct()
    return render(request, 'books/search.html', {'books': books, 'query': query})

# --- Shopping Cart Logic ---

def get_cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']

def add_to_cart(request, book_id):
    cart = get_cart(request)
    book = get_object_or_404(Book, id=book_id)
    str_id = str(book_id)
    
    if str_id in cart:
        if cart[str_id]['quantity'] < book.stock:
            cart[str_id]['quantity'] += 1
            messages.success(request, f"Increased quantity of '{book.title}' in your cart.")
        else:
            messages.error(request, f"Sorry, only {book.stock} units of '{book.title}' available in stock.")
    else:
        if book.stock > 0:
            cart[str_id] = {
                'title': book.title,
                'price': str(book.price),
                'quantity': 1,
            }
            messages.success(request, f"'{book.title}' added to your cart.")
        else:
            messages.error(request, f"Sorry, '{book.title}' is out of stock.")
    
    request.session.modified = True
    return redirect('cart')

def update_cart(request, book_id, action):
    cart = get_cart(request)
    str_id = str(book_id)
    book = get_object_or_404(Book, id=book_id)
    
    if str_id in cart:
        if action == 'increase':
            if cart[str_id]['quantity'] < book.stock:
                cart[str_id]['quantity'] += 1
            else:
                messages.error(request, f"Sorry, only {book.stock} units of '{book.title}' available in stock.")
        elif action == 'decrease':
            if cart[str_id]['quantity'] > 1:
                cart[str_id]['quantity'] -= 1
            else:
                del cart[str_id]
                messages.success(request, f"'{book.title}' removed from cart.")
        request.session.modified = True
    return redirect('cart')

def remove_from_cart(request, book_id):
    cart = get_cart(request)
    str_id = str(book_id)
    if str_id in cart:
        title = cart[str_id]['title']
        del cart[str_id]
        request.session.modified = True
        messages.success(request, f"'{title}' removed from cart.")
    return redirect('cart')

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
        messages.success(request, "Cart cleared successfully.")
    return redirect('cart')

def cart(request):
    cart = get_cart(request)
    cart_items = []
    total = 0
    for str_id, item in cart.items():
        subtotal = float(item['price']) * item['quantity']
        total += subtotal
        cart_items.append({
            'book_id': str_id,
            'title': item['title'],
            'price': float(item['price']),
            'quantity': item['quantity'],
            'subtotal': subtotal
        })
    return render(request, 'books/cart.html', {'cart_items': cart_items, 'total': total})


# --- Authentication Logic ---

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'books/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'books/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')
