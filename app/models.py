from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# class Followers(db.Model):
#     follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

followers = db.Table('followers', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)

user_pokemon = db.Table('user_pokemon', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),
)

user_product = db.Table('user_products', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('prooduct_id', db.Integer, db.ForeignKey('product.id')),
)

# create our models based off our ERD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    post = db.relationship("Post", backref="author", lazy=True)
    followed = db.relationship("User", 
        primaryjoin = (followers.c.follower_id==id), 
        secondaryjoin = (followers.c.followed_id==id),
        secondary = followers,
        backref= db.backref('followers', lazy='dynamic'),
        lazy = 'dynamic'
    )
    team = db.relationship("Pokemon",
        secondary=user_pokemon,
        backref='trainers',
        lazy='dynamic'
        )
    cart = db.relationship("Product",
        secondary=user_product,
        backref='customers',
        lazy='dynamic'
        )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def follow(self, user):
        self.followed.append(user)
        db.session.commit()

    def unfollow(self, user):
        self.followed.remove(user)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }
    def saveToDB(self):
        db.session.commit()
    
    # get all the post that I am following plus my own
    def get_followed_posts(self):
        # all the posts I am following
        followed = Post.query.join(followers, (Post.user_id == followers.c.followed_id)).filter(followers.c.follower_id == self.id)

        # get all my posts
        mine = Post.query.filter_by(user_id = self.id)

        # put them all together
        all = followed.union(mine).order_by(Post.date_created.desc())
        return all

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    pokemon_type = db.Column(db.String)
    ability = db.Column(db.String)
    img_url = db.Column(db.String)
    hp = db.Column(db.String)
    attack = db.Column(db.String)
    defense = db.Column(db.String)

    def __init__(self, name, pokemon_type, ability, img_url, hp, attack, defense):
        self.name = name
        self. pokemon_type = pokemon_type
        self.ability = ability
        self.img_url = img_url
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def save(self):
        db.session.add(self)
        db.session.commit()
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    img_url = db.Column(db.String(300))
    caption = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, img_url, caption, user_id):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id
    
    def updatePostInfo(self, title, img_url, caption):
        self.title=title
        self.img_url=img_url
        self.caption=caption

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def saveUpdates(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'caption': self.caption,
            'img_url': self.img_url,
            'date_created': self.date_created,
            'user_id': self.user_id,
            'author': self.author.username, # username to get the name of author
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(5,2), nullable=False)
    img_url = db.Column(db.String(500))
    description = db.Column(db.Numeric(5,2))

    def __init__(self, price, name, description, img_url):
        self.name = name
        self.price = price
        self.img_url = img_url
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def remove(self):
        db.session.delete(self)
        db.session.commit()