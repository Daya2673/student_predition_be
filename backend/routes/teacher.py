# Teacher routes for teacher-specific operations
from flask import Blueprint, request, jsonify
from services.data_service import DataService

# Create blueprint for teacher routes
teacher_bp = Blueprint('teacher', __name__, url_prefix='/api')

@teacher_bp.route('/teacher/<teacher_id>', methods=['GET'])
def get_teacher_dashboard(teacher_id):
    """
    Get teacher dashboard data
    Returns teacher profile and assigned subjects
    """
    try:
        teacher = DataService.get_teacher(teacher_id)
        
        if not teacher:
            return jsonify({'success': False, 'message': 'Teacher not found'}), 404
        
        # Return teacher data (without password)
        teacher_data = {
            'teacher_id': teacher['teacher_id'],
            'name': teacher['name'],
            'email': teacher['email'],
            'subjects': teacher['subjects'],
            'experience': teacher['experience']
        }
        
        return jsonify({
            'success': True,
            'data': teacher_data
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher_bp.route('/students', methods=['GET'])
def get_all_students():
    """
    Get all student records for teacher view
    Returns list of all students (without passwords)
    """
    try:
        students = DataService.get_all_students()
        
        # Remove passwords from student data
        students_data = []
        for student in students:
            student_info = {
                'reg_no': student['reg_no'],
                'name': student['name'],
                'email': student['email'],
                'attendance': student['attendance'],
                'assignments': student['assignments'],
                'marks': student['marks'],
                'study_hours': student['study_hours'],
                'cgpa': student['cgpa'],
                'subjects': student['subjects']
            }
            students_data.append(student_info)
        
        return jsonify({
            'success': True,
            'data': students_data
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher_bp.route('/student/add', methods=['POST'])
def add_student():
    """
    Add a new student to the system
    Expected JSON:
    {
        "reg_no": "STU105",
        "password": "password",
        "name": "Student Name",
        "email": "student@school.com",
        "attendance": 85,
        "assignments": 8,
        "marks": 78,
        "study_hours": 4,
        "cgpa": 7.6,
        "subjects": ["Math", "Science"]
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['reg_no', 'password', 'name', 'email', 'attendance', 'assignments', 'marks', 'study_hours', 'cgpa', 'subjects']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        result = DataService.add_student(data)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher_bp.route('/student/update/<reg_no>', methods=['PUT'])
def update_student(reg_no):
    """
    Update existing student information
    Can update: attendance, assignments, marks, study_hours, cgpa, email
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        result = DataService.update_student(reg_no, data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher_bp.route('/student/<reg_no>/suggestions', methods=['GET'])
def get_student_suggestions(reg_no):
    """
    Get improvement suggestions for a student based on performance
    """
    try:
        report = DataService.get_student_performance_report(reg_no)
        
        if not report:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        return jsonify({
            'success': True,
            'reg_no': report['reg_no'],
            'name': report['name'],
            'suggestions': report['suggestions']
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
