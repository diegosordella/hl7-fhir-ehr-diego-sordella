from app.app import app

if _name_ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)