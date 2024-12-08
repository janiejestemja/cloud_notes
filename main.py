from website import create_app

app = create_app()

if __name__ == "__main__":
    # Running the application
    app.run(debug=True)
