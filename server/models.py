from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

# Initialize the SQLAlchemy object
db = SQLAlchemy()

# Define the Author model
class Author(db.Model):
    # Set the table name
    __tablename__ = 'authors'  
    
    # Define the primary key
    id = db.Column(db.Integer, primary_key=True)  
    
    # Author name, must be unique and not null
    name = db.Column(db.String, unique=True, nullable=False)  
    
    # Author phone number
    phone_number = db.Column(db.String)  
    
    # Creation timestamp
    created_at = db.Column(db.DateTime, server_default=db.func.now())  
    
    # Update timestamp
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())  

    # Validate the name field
    @validates('name')
    def validate_name(self, key, name):
        # Check if name is not empty
        if not name:
            raise ValueError("Author name cannot be empty.")
        
        # Check for existing name
        existing_author = Author.query.filter_by(name=name).first()
        
        # Raise an error if name is not unique
        if existing_author:
            raise ValueError("Author name must be unique.")
        
        return name

    # Validate the phone number field
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        # Check if phone number is exactly 10 digits
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        
        return phone_number

    # Define the string representation of the Author object
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

# Define the Post model
class Post(db.Model):
    # Set the table name
    __tablename__ = 'posts'  
    
    # Define the primary key
    id = db.Column(db.Integer, primary_key=True)  
    
    # Post title, must not be null
    title = db.Column(db.String, nullable=False)  
    
    # Post content
    content = db.Column(db.String)  
    
    # Post category
    category = db.Column(db.String)  
    
    # Post summary
    summary = db.Column(db.String)  
    
    # Creation timestamp
    created_at = db.Column(db.DateTime, server_default=db.func.now())  
    
    # Update timestamp
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())  

    # Validate the content field
    @validates('content')
    def validate_content(self, key, content):
        # Ensure content is at least 250 characters long
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        
        return content

    # Validate the summary field
    @validates('summary')
    def validate_summary(self, key, summary):
        # Ensure summary is no more than 250 characters long
        if len(summary) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters long.")
        
        return summary

    # Validate the category field
    @validates('category')
    def validate_category(self, key, category):
        # Ensure category is either 'Fiction' or 'Non-Fiction'
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'.")
        
        return category

    # Validate the title field
    @validates('title')
    def validate_title(self, key, title):
        # Ensure title contains one of the required clickbait phrases
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError(f"Post title must be sufficiently clickbait-y and contain one of the following: {', '.join(clickbait_phrases)}")
        
        return title

    # Define the string representation of the Post object
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
