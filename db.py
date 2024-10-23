from app import app, db  # Remplacez "your_flask_app" par le nom de votre fichier Flask

def create_database():
    with app.app_context():
        db.create_all()
        

if __name__ == '__main__':
    create_database()
