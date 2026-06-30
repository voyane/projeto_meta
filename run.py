from app import create_app

app = create_app()

print("Servidor a iniciar...")

if __name__ == "__main__":
    app.run(debug=True)
