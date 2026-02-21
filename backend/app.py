# Main Flask application file
# Sets up the Flask app and registers all routes

from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.student import student_bp
from routes.teacher import teacher_bp

# Create Flask app instance
app = Flask(__name__)

# Enable CORS for Streamlit frontend to communicate
CORS(app)

# Register blueprints (route modules)
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {
        'status': 'success',
        'message': 'Student Performance Management API is running!'
    }, 200

@app.route('/api/health', methods=['GET'])
def api_health():
    """API health check endpoint"""
    return {
        'status': 'success',
        'message': 'API is operational'
    }, 200

if __name__ == '__main__':
    # Run Flask app in debug mode
    # This will reload the app when code changes
    print("🚀 Starting Student Performance Management API...")
    print("📍 Backend running on http://localhost:5000")
    print("\n📚 Available Endpoints:")
    print("  POST   /api/login - Login (student/teacher)")
    print("  GET    /api/student/<reg_no> - Get student dashboard")
    print("  GET    /api/student/<reg_no>/report - Get student report")
    print("  GET    /api/students - Get all students (teacher)")
    print("  POST   /api/student/add - Add new student (teacher)")
    print("  PUT    /api/student/update/<reg_no> - Update student (teacher)")
    print("  GET    /api/teacher/<teacher_id> - Get teacher dashboard")
    print()
    
    app.run(debug=True, host='localhost', port=5000)