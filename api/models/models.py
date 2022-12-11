from datetime import datetime

from ..utils import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.Text(), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    is_staff = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="user_comment", lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}','{self.email}')"

    def save(self):
        db.session.add(self)
        db.session.commit()


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(200), nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    summary = db.Column(db.VARCHAR, nullable=False)
    # can create a foreign key; referencing the id variable in the User class, so that is why it is lowercase u
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    comments = db.relationship("Comment", backref="post_comment", lazy=True)

    def __repr__(self):
        return f"post('{self.title}','{self.created_at}')"

    def save(self):
        res = db.session.add(self)
        db.session.commit()
        return res


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    content = db.Column(db.VARCHAR, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Comment: {self.id} by {self.user_id} on the post with {self.post_id}>"
