# Data service to handle all data operations
# This service provides methods to interact with the in-memory data

from dummy_data import STUDENTS, TEACHERS

class DataService:
    """Service class to manage student and teacher data"""
    
    # ============ AUTHENTICATION METHODS ============
    
    @staticmethod
    def authenticate_student(reg_no, password):
        """
        Authenticate a student using registration number and password
        Returns: Student data if authenticated, None otherwise
        """
        if reg_no in STUDENTS:
            student = STUDENTS[reg_no]
            if student['password'] == password:
                return student
        return None
    
    @staticmethod
    def authenticate_teacher(teacher_id, password):
        """
        Authenticate a teacher using teacher ID and password
        Returns: Teacher data if authenticated, None otherwise
        """
        if teacher_id in TEACHERS:
            teacher = TEACHERS[teacher_id]
            if teacher['password'] == password:
                return teacher
        return None
    
    # ============ STUDENT DATA METHODS ============
    
    @staticmethod
    def get_student(reg_no):
        """Get student data by registration number"""
        return STUDENTS.get(reg_no)
    
    @staticmethod
    def get_all_students():
        """Get all student records"""
        return list(STUDENTS.values())
    
    @staticmethod
    def add_student(student_data):
        """
        Add a new student to the system
        student_data: dictionary with student information
        """
        reg_no = student_data.get('reg_no')
        if reg_no and reg_no not in STUDENTS:
            STUDENTS[reg_no] = student_data
            return {"success": True, "message": "Student added successfully"}
        return {"success": False, "message": "Student already exists or invalid data"}
    
    @staticmethod
    def update_student(reg_no, update_data):
        """
        Update existing student information
        Only updates provided fields
        """
        if reg_no in STUDENTS:
            # Only allow updating specific fields
            allowed_fields = ['attendance', 'assignments', 'marks', 'study_hours', 'cgpa', 'email']
            for field in allowed_fields:
                if field in update_data:
                    STUDENTS[reg_no][field] = update_data[field]
            return {"success": True, "message": "Student updated successfully"}
        return {"success": False, "message": "Student not found"}
    
    @staticmethod
    def get_student_performance_report(reg_no):
        """
        Generate performance report for a student
        Includes analysis and suggestions
        """
        student = STUDENTS.get(reg_no)
        if not student:
            return None
        
        # Generate suggestions based on performance
        suggestions = []
        
        if student['attendance'] < 80:
            suggestions.append("⚠️ Attendance is low. Try to attend classes regularly.")
        
        if student['marks'] < 70:
            suggestions.append("📚 Marks need improvement. Consider extra study sessions.")
        
        if student['study_hours'] < 4:
            suggestions.append("⏱️ Increase study hours. Aim for at least 4 hours daily.")
        
        if student['cgpa'] < 7.0:
            suggestions.append("🎯 Focus on improving CGPA. Set clear academic goals.")
        
        if student['assignments'] < 8:
            suggestions.append("✏️ Complete more assignments to improve practical knowledge.")
        
        if not suggestions:
            suggestions.append("✅ Great performance! Keep up the excellent work.")
        
        return {
            "reg_no": student['reg_no'],
            "name": student['name'],
            "attendance": student['attendance'],
            "marks": student['marks'],
            "cgpa": student['cgpa'],
            "study_hours": student['study_hours'],
            "assignments": student['assignments'],
            "suggestions": suggestions
        }
    
    # ============ TEACHER DATA METHODS ============
    
    @staticmethod
    def get_teacher(teacher_id):
        """Get teacher data by teacher ID"""
        return TEACHERS.get(teacher_id)
    
    @staticmethod
    def get_teacher_subjects(teacher_id):
        """Get subjects assigned to a teacher"""
        teacher = TEACHERS.get(teacher_id)
        if teacher:
            return teacher['subjects']
        return []
