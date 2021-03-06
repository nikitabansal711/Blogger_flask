from app import db


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(2000), unique=True)
    user_name = db.Column(db.String(64), nullable=False, unique=True)
    user_email = db.Column(db.String(120), nullable=False)
    user_address = db.Column(db.String(200), nullable=False)
    user_mobile = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(2000), nullable=False)
    blogs = db.relationship('Blog', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.user_name)


class Blog(db.Model):
    __tablename__ = 'blog'
    blog_id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120), nullable=False)
    blog_type = db.Column(db.String(120), nullable=False)
    blog_desc = db.Column(db.Text(), nullable=False)
    blog_content = db.Column(db.Text(), nullable=False)
    blog_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        return '<Blog {}>'.format(self.blog_title)


class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)
    role_desc = db.Column(db.Text())

    def __repr__(self):
        return '<Role {}>'.format(self.role_name)
