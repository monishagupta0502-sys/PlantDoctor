import sqlite3
import hashlib

DB_NAME = "database/users.db"


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )
    """)

    # Diagnosis History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diagnosis_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL,

        plant TEXT NOT NULL,

        disease TEXT NOT NULL,

        confidence REAL NOT NULL,

        prediction_time REAL NOT NULL,

        scan_date TEXT NOT NULL

    )
    """)

    conn.commit()
    conn.close()


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ============================================================
# REGISTER USER
# ============================================================

def register_user(username, password):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users(username,password)
            VALUES(?,?)
            """,
            (
                username,
                hash_password(password)
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ============================================================
# LOGIN USER
# ============================================================

def login_user(username, password):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=? AND password=?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user


# ============================================================
# SAVE SCAN
# ============================================================

def save_scan(
    username,
    plant,
    disease,
    confidence,
    prediction_time,
    scan_date
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO diagnosis_history
        (
            username,
            plant,
            disease,
            confidence,
            prediction_time,
            scan_date
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            plant,
            disease,
            confidence,
            prediction_time,
            scan_date
        )
    )

    conn.commit()

    conn.close()


# ============================================================
# GET HISTORY
# ============================================================

def get_history(username):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            plant,
            disease,
            confidence,
            prediction_time,
            scan_date
        FROM diagnosis_history
        WHERE username=?
        ORDER BY id DESC
        """,
        (username,)
    )

    history = cursor.fetchall()

    conn.close()

    return history