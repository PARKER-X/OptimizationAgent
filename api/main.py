from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Import your existing routers
from api.routes import planner, explainer, solver

# Create FastAPI app
app = FastAPI(
    title="MILP Optimization Agent API",
    description="Advanced Mixed-Integer Linear Programming solutions powered by AI",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your existing routers
app.include_router(planner.router, prefix="/planner", tags=["planner"])
app.include_router(solver.router, prefix="/solver", tags=["solver"])
app.include_router(explainer.router, prefix="/explainer", tags=["explainer"])

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the main HTML files
@app.get("/")
async def read_index():
    """Serve the main index page"""
    return FileResponse("templates/index.html")

@app.get("/index.html")
async def read_index_alt():
    """Alternative route for index page"""
    return FileResponse("templates/index.html")

@app.get("/results.html")
async def read_results():
    """Serve the results page"""
    return FileResponse("templates/results.html")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "MILP Optimization Agent API is running"}

# API status endpoint
@app.get("/api/status")
async def api_status():
    """Get API status and available endpoints"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "endpoints": {
            "solver": "/solver/solve",
            "planner": "/planner/plan", 
            "explainer": "/explainer/solve",
            "code": "/solver/code"
        },
        "frontend": {
            "index": "/",
            "results": "/results.html"
        }
    }

# Root redirect to index
@app.get("/home")
async def redirect_home():
    """Redirect to home page"""
    return FileResponse("templates/index.html")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors by serving index page"""
    return FileResponse("templates/index.html")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print("🚀 MILP Optimization Agent API is starting...")
    print("📊 Available endpoints:")
    print("   - POST /solver/solve - Solve optimization problems")
    print("   - POST /planner/plan - Generate execution plans")
    print("   - POST /explainer/solve - Explain solutions")
    print("   - GET /solver/code - Get generated code")
    print("🌐 Frontend available at: http://localhost:8000/")
    print("📚 API docs available at: http://localhost:8000/docs")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 MILP Optimization Agent API is shutting down...")

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
