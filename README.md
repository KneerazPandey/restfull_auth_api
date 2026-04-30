# RESTful Authentication API (Django + JWT + OTP + Social Login)

A production-ready authentication system built with Django REST Framework that supports multiple authentication methods including email/password login, OTP-based authentication, and Google social login with JWT-based session management.

This project is designed to demonstrate real-world backend architecture used in modern scalable applications.

---

## 🚀 Features

### Authentication Methods
- Email & Password authentication (JWT-based)
- OTP-based authentication (Email verification & passwordless login)
- Google Social Authentication (OAuth2 ID Token verification)

### Security Features
- JWT Access & Refresh Tokens (SimpleJWT)
- Password hashing (Django built-in hasher)
- OTP expiration system
- Rate limiting support (extendable with Redis)
- Account verification system

### Advanced Features
- Social account linking (Google → existing user)
- Auto user creation on social login
- OTP-based registration flow
- Password reset via OTP
- Secure token refresh & logout support

---

## 🏗️ Tech Stack

- Python 3.x
- Django
- Django REST Framework
- SimpleJWT
- PostgreSQL (or SQLite for development)
- Redis (for OTP caching - optional but recommended)
- Google OAuth2 (social login verification)

---

## 📦 Project Architecture
