from recipe import app

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    app.run(debug=True)
