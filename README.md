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
User Model
│
├── SocialAccount (Google, Facebook, etc.)
├── OTP System (Email verification / Login / Password reset)
├── JWT Authentication Layer
│
└── Auth Services (Business Logic Layer)


---

## 📌 Authentication Flow

### 1. Email/Password Login
```
User → /auth/login/ → Validate credentials → JWT Token
```

---

### 2. OTP Registration Flow
```
User enters email + password
        ↓
Send OTP → /auth/send-otp/
        ↓
Verify OTP → /auth/verify-otp/
        ↓
Create User → Return JWT
```

---

### 3. Google Social Login
```
Frontend Google Login → ID Token
        ↓
POST /auth/google/
        ↓
Verify Google Token
        ↓
Create or Login User
        ↓
Return JWT
```

---

## 🔐 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | /auth/register/ | Register with email/password (OTP flow) |
| POST | /auth/login/ | Login with email/password |
| POST | /auth/refresh/ | Refresh JWT token |
| POST | /auth/logout/ | Logout user |

---

### OTP System
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | /auth/send-otp/ | Send OTP to email |
| POST | /auth/verify-otp/ | Verify OTP |

---

### Social Authentication
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | /auth/google/ | Google login/register |

---

## 🧠 Database Models

### User Model
- Custom user model using email as primary identifier
- Stores authentication and verification state

### SocialAccount
- Links user accounts with social providers
- Supports multiple providers per user

### OTP Model / Redis Cache
- Stores temporary OTPs
- Supports multiple purposes:
  - Registration verification
  - Password reset
  - Login verification

---

## 🔒 Security Design

- Passwords are never stored in plain text
- OTPs are time-limited and expire automatically
- Google authentication uses ID token verification
- JWT tokens used for stateless authentication
- Optional Redis caching for temporary auth data
