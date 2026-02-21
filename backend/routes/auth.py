# Authentication routes for login functionality
from flask import Blueprint, request, jsonify
from services.data_service import DataService

# Create blueprint for auth routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handle login for both students and teachers
    Expected JSON:
    {
        "role": "student" or "teacher",
        "username": "reg_no" (for student) or "teacher_id" (for teacher),
        "password": "password"
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'role' not in data or 'username' not in data or 'password' not in data:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        role = data.get('role').lower()
        username = data.get('username')
        password = data.get('password')
        
        # Authenticate based on role
        if role == 'student':
            user = DataService.authenticate_student(username, password)
            if user:
                return jsonify({
                    'success': True,
                    'message': 'Student login successful',
                    'role': 'student',
                    'user': {
                        'reg_no': user['reg_no'],
                        'name': user['name'],
                        'email': user['email']
                    }
                }), 200
            else:
                return jsonify({'success': False, 'message': 'Invalid student credentials'}), 401
        
        elif role == 'teacher':
            user = DataService.authenticate_teacher(username, password)
            if user:
                return jsonify({
                    'success': True,
                    'message': 'Teacher login successful',
                    'role': 'teacher',
                    'user': {
                        'teacher_id': user['teacher_id'],
                        'name': user['name'],
                        'email': user['email']
                    }
                }), 200
            else:
                return jsonify({'success': False, 'message': 'Invalid teacher credentials'}), 401
        
        else:
            return jsonify({'success': False, 'message': 'Invalid role'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
