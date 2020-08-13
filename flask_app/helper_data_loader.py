import csv
import psycopg2
from app import db
from app.models import User, Role, Blog


def load_data_users():
    """ this function loads data from csv"""
    try:
        with open("data/user.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)  # This skips the 1st row which is the header.
            for record in reader:
                user = User(
                    user_id=record[0],
                    public_id=record[1],
                    user_name=record[2],
                    user_email=record[3],
                    user_address=record[4],
                    user_mobile=record[5],
                    password=record[6],
                )
                db.session.add(user)
            db.session.commit()
            print("loaded data  to user table")
    except (Exception, psycopg2.Error) as e:
        print(e)


def load_data_blogs():
    """ this function loads data from csv"""
    try:
        with open("data/blog.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for record in reader:
                blog = Blog(
                    blog_id=record[0],
                    blog_title=record[1],
                    blog_type=record[2],
                    blog_desc=record[3],
                    blog_content=record[4],
                    blog_user_id=record[5],
                )
                db.session.add(blog)
            db.session.commit()
            print("loaded data to blog table")

    except psycopg2.Error as e:
        print(e)
    except Exception as error:
        print(error)


def load_data_roles():
    """ this function loads data from csv"""
    try:
        with open("data/role.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for record in reader:
                role = Role(role_id=record[0], role_name=record[1], role_desc=record[2])
                db.session.add(role)
            db.session.commit()
            print("loaded data to role table")
        db.session.close()
    except (Exception, psycopg2.Error) as e:
        print(e)


if __name__ == "__main__":
    load_data_roles()
    load_data_users()
    load_data_blogs()
