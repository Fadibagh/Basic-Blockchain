from app import app

# This is the handler for Vercel
def handler(request):
    return app(request.environ, request.start_response)

# Export the app for Vercel
application = app

if __name__ == "__main__":
    app.run(debug=True) 