"""
Database Module for Ophthalmic Care System
Handles SQLite database operations
Author: Ophthalmic AI Research Team
"""

import sqlite3
import os
from datetime import datetime
import hashlib
import json

class DatabaseManager:
    """
    Manages all database operations for the ophthalmic care system
    """
    
    def __init__(self, db_path='ophthalmic_care.db'):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def connect(self):
        """
        Connect to database
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"✓ Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"✗ Database connection error: {e}")
    
    def close(self):
        """
        Close database connection
        """
        if self.conn:
            self.conn.close()
    
    def init_database(self):
        """
        Initialize database tables
        """
        self.connect()
        
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT DEFAULT 'doctor',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Patients table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                contact TEXT,
                medical_history TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Examinations table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS examinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                image_path TEXT NOT NULL,
                predicted_class INTEGER,
                severity TEXT,
                confidence REAL,
                all_probabilities TEXT,
                risk_level TEXT,
                description TEXT,
                gradcam_path TEXT,
                recommendation TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(patient_id) REFERENCES patients(id),
                FOREIGN KEY(doctor_id) REFERENCES users(id)
            )
        ''')
        
        # Statistics table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        print("✓ Database tables initialized")
    
    def hash_password(self, password):
        """
        Hash password using SHA256
        
        Args:
            password: Plain password
        
        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, password, email, role='doctor'):
        """
        Create new user
        
        Args:
            username: Username
            password: Password
            email: Email address
            role: User role (doctor/admin)
        
        Returns:
            Success status and user_id
        """
        try:
            hashed_password = self.hash_password(password)
            self.cursor.execute('''
                INSERT INTO users (username, password, email, role)
                VALUES (?, ?, ?, ?)
            ''', (username, hashed_password, email, role))
            self.conn.commit()
            return True, self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print("✗ Username or email already exists")
            return False, None
        except Exception as e:
            print(f"✗ Error creating user: {e}")
            return False, None
    
    def authenticate_user(self, username, password):
        """
        Authenticate user login
        
        Args:
            username: Username
            password: Password
        
        Returns:
            User data if authenticated, None otherwise
        """
        try:
            hashed_password = self.hash_password(password)
            self.cursor.execute('''
                SELECT id, username, email, role FROM users
                WHERE username = ? AND password = ?
            ''', (username, hashed_password))
            user = self.cursor.fetchone()
            
            if user:
                # Update last login
                self.cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user[0],))
                self.conn.commit()
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'role': user[3]
                }
            return None
        except Exception as e:
            print(f"✗ Authentication error: {e}")
            return None
    
    def create_patient(self, patient_name, age, gender, contact, medical_history=''):
        """
        Create new patient record
        
        Args:
            patient_name: Patient name
            age: Age
            gender: Gender
            contact: Contact number
            medical_history: Medical history
        
        Returns:
            Patient ID if successful
        """
        try:
            self.cursor.execute('''
                INSERT INTO patients (patient_name, age, gender, contact, medical_history)
                VALUES (?, ?, ?, ?, ?)
            ''', (patient_name, age, gender, contact, medical_history))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"✗ Error creating patient: {e}")
            return None
    
    def get_patient(self, patient_id):
        """
        Get patient information
        
        Args:
            patient_id: Patient ID
        
        Returns:
            Patient data
        """
        try:
            self.cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
            patient = self.cursor.fetchone()
            if patient:
                return {
                    'id': patient[0],
                    'name': patient[1],
                    'age': patient[2],
                    'gender': patient[3],
                    'contact': patient[4],
                    'medical_history': patient[5]
                }
            return None
        except Exception as e:
            print(f"✗ Error fetching patient: {e}")
            return None
    
    def create_examination(self, patient_id, doctor_id, image_path, prediction_data):
        """
        Create examination record
        
        Args:
            patient_id: Patient ID
            doctor_id: Doctor ID
            image_path: Path to uploaded image
            prediction_data: Dictionary with prediction results
        
        Returns:
            Examination ID if successful
        """
        try:
            probabilities_json = json.dumps(prediction_data.get('all_probabilities', {}))
            
            self.cursor.execute('''
                INSERT INTO examinations
                (patient_id, doctor_id, image_path, predicted_class, severity,
                 confidence, all_probabilities, risk_level, description, recommendation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_id,
                doctor_id,
                image_path,
                prediction_data.get('predicted_class'),
                prediction_data.get('severity'),
                prediction_data.get('confidence'),
                probabilities_json,
                prediction_data.get('risk_level'),
                prediction_data.get('description'),
                prediction_data.get('recommendation', '')
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"✗ Error creating examination: {e}")
            return None
    
    def get_patient_examinations(self, patient_id):
        """
        Get all examinations for a patient
        
        Args:
            patient_id: Patient ID
        
        Returns:
            List of examinations
        """
        try:
            self.cursor.execute('''
                SELECT id, image_path, severity, confidence, risk_level, created_at
                FROM examinations
                WHERE patient_id = ?
                ORDER BY created_at DESC
            ''', (patient_id,))
            
            examinations = []
            for exam in self.cursor.fetchall():
                examinations.append({
                    'id': exam[0],
                    'image_path': exam[1],
                    'severity': exam[2],
                    'confidence': exam[3],
                    'risk_level': exam[4],
                    'date': exam[5]
                })
            return examinations
        except Exception as e:
            print(f"✗ Error fetching examinations: {e}")
            return []
    
    def get_examination(self, exam_id):
        """
        Get specific examination details
        
        Args:
            exam_id: Examination ID
        
        Returns:
            Examination data
        """
        try:
            self.cursor.execute('''
                SELECT * FROM examinations WHERE id = ?
            ''', (exam_id,))
            
            exam = self.cursor.fetchone()
            if exam:
                return {
                    'id': exam[0],
                    'patient_id': exam[1],
                    'doctor_id': exam[2],
                    'image_path': exam[3],
                    'predicted_class': exam[4],
                    'severity': exam[5],
                    'confidence': exam[6],
                    'all_probabilities': json.loads(exam[7]) if exam[7] else {},
                    'risk_level': exam[8],
                    'description': exam[9],
                    'recommendation': exam[11],
                    'created_at': exam[13]
                }
            return None
        except Exception as e:
            print(f"✗ Error fetching examination: {e}")
            return None
    
    def get_dashboard_stats(self):
        """
        Get statistics for dashboard
        
        Returns:
            Dashboard statistics
        """
        try:
            # Total patients
            self.cursor.execute('SELECT COUNT(*) FROM patients')
            total_patients = self.cursor.fetchone()[0]
            
            # Total examinations
            self.cursor.execute('SELECT COUNT(*) FROM examinations')
            total_examinations = self.cursor.fetchone()[0]
            
            # Severity distribution
            self.cursor.execute('''
                SELECT severity, COUNT(*) as count
                FROM examinations
                GROUP BY severity
            ''')
            severity_dist = {}
            for row in self.cursor.fetchall():
                severity_dist[row[0]] = row[1]
            
            # Average confidence
            self.cursor.execute('SELECT AVG(confidence) FROM examinations')
            avg_confidence = self.cursor.fetchone()[0] or 0
            
            return {
                'total_patients': total_patients,
                'total_examinations': total_examinations,
                'severity_distribution': severity_dist,
                'average_confidence': round(avg_confidence, 4),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"✗ Error fetching statistics: {e}")
            return {}
    
    def search_patients(self, search_term):
        """
        Search patients by name or contact
        
        Args:
            search_term: Search term
        
        Returns:
            List of matching patients
        """
        try:
            self.cursor.execute('''
                SELECT id, patient_name, age, gender, contact
                FROM patients
                WHERE patient_name LIKE ? OR contact LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%'))
            
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'id': row[0],
                    'name': row[1],
                    'age': row[2],
                    'gender': row[3],
                    'contact': row[4]
                })
            return results
        except Exception as e:
            print(f"✗ Error searching patients: {e}")
            return []


def demo_database():
    """
    Demo database operations
    """
    print("\n" + "=" * 70)
    print("DATABASE OPERATIONS DEMO")
    print("=" * 70)
    
    # Initialize database
    db = DatabaseManager('ophthalmic_care_demo.db')
    
    # Create sample user
    print("\n→ Creating sample doctor user...")
    success, user_id = db.create_user('dr_sharma', 'password123', 'dr_sharma@hospital.com', 'doctor')
    if success:
        print(f"✓ User created with ID: {user_id}")
    
    # Create sample patient
    print("\n→ Creating sample patient...")
    patient_id = db.create_patient('John Doe', 55, 'M', '9876543210', 'Diabetic')
    if patient_id:
        print(f"✓ Patient created with ID: {patient_id}")
    
    # Get patient
    print("\n→ Retrieving patient information...")
    patient = db.get_patient(patient_id)
    if patient:
        print(f"✓ Patient: {patient['name']}, Age: {patient['age']}")
    
    # Get dashboard stats
    print("\n→ Retrieving dashboard statistics...")
    stats = db.get_dashboard_stats()
    print(f"✓ Total Patients: {stats.get('total_patients', 0)}")
    print(f"✓ Total Examinations: {stats.get('total_examinations', 0)}")
    
    db.close()
    print("\n✓ Database demo completed!")
    print("=" * 70)


if __name__ == "__main__":
    demo_database()
