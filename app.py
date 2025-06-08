from flask import Flask, render_template, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
from models import db, Book, Member, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# Book Endpoints
@app.route('/api/books', methods=['GET', 'POST'])
def manage_books():
    if request.method == 'GET':
        books = Book.query.all()
        return jsonify([{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'category': book.category,
            'status': book.status
        } for book in books])
    
    if request.method == 'POST':
        data = request.json
        new_book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            category=data['category']
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'message': 'Book added successfully'}), 201

@app.route('/api/books/<int:id>', methods=['PUT', 'DELETE'])
def book_detail(id):
    book = Book.query.get_or_404(id)
    
    if request.method == 'PUT':
        data = request.json
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.isbn = data.get('isbn', book.isbn)
        book.category = data.get('category', book.category)
        book.status = data.get('status', book.status)
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'})
    
    if request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})

# Member Endpoints
@app.route('/api/members', methods=['GET', 'POST'])
def manage_members():
    if request.method == 'GET':
        members = Member.query.all()
        return jsonify([{
            'id': member.id,
            'name': member.name,
            'email': member.email,
            'phone': member.phone,
            'member_type': member.member_type,
            'books_borrowed': member.books_borrowed
        } for member in members])
    
    if request.method == 'POST':
        data = request.json
        new_member = Member(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            member_type=data['member_type']
        )
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'message': 'Member added successfully'}), 201

@app.route('/api/members/<int:id>', methods=['PUT', 'DELETE'])
def member_detail(id):
    member = Member.query.get_or_404(id)
    
    if request.method == 'PUT':
        data = request.json
        member.name = data.get('name', member.name)
        member.email = data.get('email', member.email)
        member.phone = data.get('phone', member.phone)
        member.member_type = data.get('member_type', member.member_type)
        member.books_borrowed = data.get('books_borrowed', member.books_borrowed)
        db.session.commit()
        return jsonify({'message': 'Member updated successfully'})
    
    if request.method == 'DELETE':
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Member deleted successfully'})

# Authentication Endpoints
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(
        email=data['email'],
        password=data['password']
    ).first()
    
    if user:
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    new_user = User(
        fullname=data['fullname'],
        email=data['email'],
        password=data['password'],
        user_type=data['user_type']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Account created successfully'}), 201

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'})

# Statistics Endpoint
@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_books = Book.query.count()
    total_members = Member.query.count()
    return jsonify({
        'total_books': total_books,
        'total_members': total_members
    })

if __name__ == '__main__':
    app.run(debug=True)