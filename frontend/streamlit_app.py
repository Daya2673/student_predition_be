import streamlit as st
import requests
import pandas as pd

# Configure page
st.set_page_config(page_title="Student Performance Management", layout="wide")

# Backend API URL
API_URL = "http://localhost:5000/api"

# ============ SESSION STATE MANAGEMENT ============
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_id = None
    st.session_state.user_name = None

# ============ LOGIN PAGE ============
def login_page():
    """Display login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🎓 Student Performance Management")
        st.write("---")
        
        # Role selection
        role = st.radio("Select Your Role", ["Student", "Teacher"], horizontal=True)
        st.write("---")
        
        if role == "Student":
            st.subheader("📚 Student Login")
            
            col_a, col_b = st.columns(2)
            with col_a:
                reg_no = st.text_input("Registration Number", placeholder="e.g., STU101")
            with col_b:
                password = st.text_input("Password", type="password", placeholder="e.g., stu@101")
            
            st.write("**Demo Credentials:**")
            st.write("STU101 / stu@101 | STU102 / stu@102 | STU103 / stu@103 | STU104 / stu@104")
            
            if st.button("🔓 Login as Student", use_container_width=True):
                if reg_no and password:
                    try:
                        response = requests.post(
                            f"{API_URL}/login",
                            json={'role': 'student', 'username': reg_no, 'password': password}
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.logged_in = True
                            st.session_state.role = 'student'
                            st.session_state.user_id = reg_no
                            st.session_state.user_name = data['user']['name']
                            st.success(f"✅ Welcome, {data['user']['name']}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Please try again.")
                    except requests.exceptions.RequestException:
                        st.error("❌ Cannot connect to backend. Make sure Flask is running on port 5000.")
                else:
                    st.warning("⚠️ Please enter both registration number and password.")
        
        else:  # Teacher
            st.subheader("👨‍🏫 Teacher Login")
            
            col_a, col_b = st.columns(2)
            with col_a:
                teacher_id = st.text_input("Teacher ID", placeholder="e.g., TCH001")
            with col_b:
                password = st.text_input("Password", type="password", placeholder="e.g., teacher@123")
            
            st.write("**Demo Credentials:**")
            st.write("TCH001 / teacher@123")
            
            if st.button("🔓 Login as Teacher", use_container_width=True):
                if teacher_id and password:
                    try:
                        response = requests.post(
                            f"{API_URL}/login",
                            json={'role': 'teacher', 'username': teacher_id, 'password': password}
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.logged_in = True
                            st.session_state.role = 'teacher'
                            st.session_state.user_id = teacher_id
                            st.session_state.user_name = data['user']['name']
                            st.success(f"✅ Welcome, {data['user']['name']}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Please try again.")
                    except requests.exceptions.RequestException:
                        st.error("❌ Cannot connect to backend. Make sure Flask is running on port 5000.")
                else:
                    st.warning("⚠️ Please enter both teacher ID and password.")

# ============ STUDENT DASHBOARD ============
def student_dashboard():
    """Display student dashboard"""
    st.title(f"📚 Student Dashboard - {st.session_state.user_name}")
    
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.rerun()
    
    st.write("---")
    
    try:
        # Fetch student data
        response = requests.get(f"{API_URL}/student/{st.session_state.user_id}")
        
        if response.status_code == 200:
            student_data = response.json()['data']
            
            # Display academic details
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Attendance", f"{student_data['attendance']}%")
            with col2:
                st.metric("📝 Assignments Done", student_data['assignments'])
            with col3:
                st.metric("⭐ CGPA", f"{student_data['cgpa']}"
                )
            st.write("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("📈 Marks Obtained", student_data['marks'])
            with col2:
                st.metric("⏱️ Study Hours", f"{student_data['study_hours']} hrs/day")
            
            st.write("---")
            
            # Display detailed information
            st.subheader("📋 Detailed Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {student_data['name']}")
                st.write(f"**Reg No:** {student_data['reg_no']}")
                st.write(f"**Email:** {student_data['email']}")
            
            with col2:
                st.write(f"**Subjects Enrolled:**")
                for subject in student_data['subjects']:
                    st.write(f"  • {subject}")
            
            st.write("---")
            
            # Display performance report with suggestions
            st.subheader("📊 Performance Report & Suggestions")
            
            report_response = requests.get(f"{API_URL}/student/{st.session_state.user_id}/report")
            if report_response.status_code == 200:
                report_data = report_response.json()['data']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Performance Metrics:**")
                    st.write(f"  • Attendance: {report_data['attendance']}%")
                    st.write(f"  • Marks: {report_data['marks']}")
                    st.write(f"  • CGPA: {report_data['cgpa']}")
                    st.write(f"  • Study Hours: {report_data['study_hours']}")
                
                with col2:
                    st.write("**Suggestions for Improvement:**")
                    for suggestion in report_data['suggestions']:
                        st.write(f"  {suggestion}")
        else:
            st.error("❌ Unable to fetch student data.")
    
    except requests.exceptions.RequestException:
        st.error("❌ Cannot connect to backend.")

# ============ TEACHER DASHBOARD ============
def teacher_dashboard():
    """Display teacher dashboard"""
    st.title(f"👨‍🏫 Teacher Dashboard - {st.session_state.user_name}")
    
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.rerun()
    
    st.write("---")
    
    try:
        # Fetch teacher data
        response = requests.get(f"{API_URL}/teacher/{st.session_state.user_id}")
        
        if response.status_code == 200:
            teacher_data = response.json()['data']
            
            # Display teacher profile
            st.subheader("👤 Teacher Profile")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Name:** {teacher_data['name']}")
                st.write(f"**Teacher ID:** {teacher_data['teacher_id']}")
                st.write(f"**Email:** {teacher_data['email']}")
            
            with col2:
                st.write(f"**Experience:** {teacher_data['experience']} years")
                st.write(f"**Subjects:**")
                for subject in teacher_data['subjects']:
                    st.write(f"  • {subject}")
            
            st.write("---")
            
            # Tabs for different features
            tab1, tab2, tab3, tab4 = st.tabs(["📊 All Students", "➕ Add Student", "✏️ Update Student", "💡 View Suggestions"])
            
            # TAB 1: View all students
            with tab1:
                st.subheader("📊 View All Students")
                
                students_response = requests.get(f"{API_URL}/students")
                if students_response.status_code == 200:
                    students_data = students_response.json()['data']
                    
                    # Create dataframe for better display
                    df = pd.DataFrame(students_data)
                    st.dataframe(df, use_container_width=True)
                    
                    st.info(f"ℹ️ Total Students: {len(students_data)}")
                else:
                    st.error("❌ Unable to fetch student list.")
            
            # TAB 2: Add new student
            with tab2:
                st.subheader("➕ Add New Student")
                
                with st.form("add_student_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        reg_no = st.text_input("Registration Number", placeholder="STU105")
                        password = st.text_input("Password", type="password")
                        name = st.text_input("Student Name")
                        email = st.text_input("Email")
                    
                    with col2:
                        attendance = st.number_input("Attendance %", 0, 100, 80)
                        assignments = st.number_input("Assignments Done", 0, 15, 8)
                        marks = st.number_input("Marks Obtained", 0, 100, 75)
                        study_hours = st.number_input("Study Hours/Day", 0.0, 10.0, 4.0)
                    
                    cgpa = st.number_input("CGPA", 0.0, 10.0, 7.5)
                    subjects = st.multiselect("Subjects", ["Mathematics", "Physics", "Chemistry", "Computer Science", "English", "History"])
                    
                    submit = st.form_submit_button("✅ Add Student", use_container_width=True)
                    
                    if submit:
                        if not reg_no or not password or not name or not email or not subjects:
                            st.error("❌ Please fill in all required fields.")
                        else:
                            student_payload = {
                                'reg_no': reg_no,
                                'password': password,
                                'name': name,
                                'email': email,
                                'attendance': attendance,
                                'assignments': assignments,
                                'marks': marks,
                                'study_hours': study_hours,
                                'cgpa': cgpa,
                                'subjects': subjects
                            }
                            
                            add_response = requests.post(
                                f"{API_URL}/student/add",
                                json=student_payload
                            )
                            
                            if add_response.status_code == 201:
                                st.success("✅ Student added successfully!")
                            else:
                                st.error(f"❌ Error: {add_response.json()['message']}")
            
            # TAB 3: Update student
            with tab3:
                st.subheader("✏️ Update Student Information")
                
                students_response = requests.get(f"{API_URL}/students")
                if students_response.status_code == 200:
                    students_data = students_response.json()['data']
                    student_names = {s['reg_no']: f"{s['name']} ({s['reg_no']})" for s in students_data}
                    
                    selected_student_display = st.selectbox("Select Student", list(student_names.values()))
                    selected_reg_no = [k for k, v in student_names.items() if v == selected_student_display][0]
                    
                    with st.form("update_student_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            attendance = st.number_input("Attendance %", 0, 100, 80)
                            marks = st.number_input("Marks", 0, 100, 75)
                        
                        with col2:
                            assignments = st.number_input("Assignments", 0, 15, 8)
                            study_hours = st.number_input("Study Hours", 0.0, 10.0, 4.0)
                        
                        cgpa = st.number_input("CGPA", 0.0, 10.0, 7.5)
                        email = st.text_input("Email")
                        
                        submit = st.form_submit_button("💾 Update Student", use_container_width=True)
                        
                        if submit:
                            update_payload = {
                                'attendance': attendance,
                                'marks': marks,
                                'assignments': assignments,
                                'study_hours': study_hours,
                                'cgpa': cgpa,
                                'email': email
                            }
                            
                            update_response = requests.put(
                                f"{API_URL}/student/update/{selected_reg_no}",
                                json=update_payload
                            )
                            
                            if update_response.status_code == 200:
                                st.success("✅ Student updated successfully!")
                            else:
                                st.error(f"❌ Error: {update_response.json()['message']}")
            
            # TAB 4: View suggestions
            with tab4:
                st.subheader("💡 View Student Improvement Suggestions")
                
                students_response = requests.get(f"{API_URL}/students")
                if students_response.status_code == 200:
                    students_data = students_response.json()['data']
                    student_names = {s['reg_no']: f"{s['name']} ({s['reg_no']})" for s in students_data}
                    
                    selected_student_display = st.selectbox("Select Student to View Suggestions", list(student_names.values()))
                    selected_reg_no = [k for k, v in student_names.items() if v == selected_student_display][0]
                    
                    if st.button("📋 Get Suggestions"):
                        suggestions_response = requests.get(
                            f"{API_URL}/student/{selected_reg_no}/suggestions"
                        )
                        
                        if suggestions_response.status_code == 200:
                            suggestions_data = suggestions_response.json()
                            
                            st.write(f"**Student:** {suggestions_data['name']} ({suggestions_data['reg_no']})")
                            st.write("**Improvement Suggestions:**")
                            
                            for suggestion in suggestions_data['suggestions']:
                                st.write(f"  {suggestion}")
                        else:
                            st.error("❌ Unable to fetch suggestions.")
        else:
            st.error("❌ Unable to fetch teacher data.")
    
    except requests.exceptions.RequestException:
        st.error("❌ Cannot connect to backend.")

# ============ MAIN APP LOGIC ============
if st.session_state.logged_in:
    if st.session_state.role == 'student':
        student_dashboard()
    else:  # teacher
        teacher_dashboard()
else:
    login_page()