from app import create_app

app = create_app()

if __name__ == "__main__":
    print("Servidor a iniciar...")
    app.run(debug=True)
