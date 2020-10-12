from recipe import app,db
import os

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    if not os.path.exists('site.db'):
        db.create_all()
    app.run(debug=True)
