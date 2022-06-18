from Mems import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001, host="0.0.0.0")