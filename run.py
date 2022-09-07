from app import app
from app .models import User, Post, db, Product, Product2

@app.shell_context_processor
def makeShellContext():
    return {'db': db, 'User': User, 'Post': Post, 'Product': Product, 'Product2': Product2}

if __name__ == '__main__':
    app.run()