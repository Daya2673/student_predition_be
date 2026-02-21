# Student routes for student-specific operations
from flask import Blueprint, request, jsonify
from services.data_service import DataService

# Create blueprint for student routes
student_bp = Blueprint('student', __name__, url_prefix='/api')

@student_bp.route('/student/<reg_no>', methods=['GET'])
def get_student_dashboard(reg_no):
    """
    Get student dashboard data
    Returns student's academic details
    """
    try:
        student = DataService.get_student(reg_no)
        
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        # Return student data (without password)
        student_data = {
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
        
        return jsonify({
            'success': True,
            'data': student_data
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@student_bp.route('/student/<reg_no>/report', methods=['GET'])
def get_student_report(reg_no):
    """
    Get student performance report with suggestions
    """
    try:
        report = DataService.get_student_performance_report(reg_no)
        
        if not report:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        return jsonify({
            'success': True,
            'data': report
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
