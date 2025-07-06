# 🔐 Smart Resource Access Gateway (FastAPI + JWT)

A production-ready API gateway built with **FastAPI**, designed to authenticate users and issue **resource-scoped JWT tokens** for accessing separate service backends (e.g., hotel, event management, hospital systems, etc.).

This project features **rate-limiting (Redis)**, **audit logging (AWS S3 or DynamoDB)**, and **alerting (SNS)** — showcasing scalable, secure backend engineering.

---

## 📽️ Explaination Videos

| Feature                    | Watch                                      |
|---------------------------|---------------------------------------------|
| 🧠 Intro and Setting Up Project | [LINK](https://www.loom.com/share/2edf0ae02e6c486f97fa14a314e5934a?sid=70952695-47b1-48bc-97a4-e5b5d5a14ba4) |
| 📦 Project Setup & Databases | [LINK](https://www.loom.com/share/4131970b521e479da35a90d11a20eb33?sid=36e4df4d-dfbb-4698-b359-e2c99d8c5c09) |
| 🎫 JWT Encoding | [LINK](https://www.loom.com/share/2970c725894a40ccbc9ada1b1b7ab181?sid=b89c08ba-8d95-4bd5-9958-5b605d350b0d) |
| 🎫 Hash & JWT Decoding | [LINK](https://www.loom.com/share/72d0465376644404b62d102005dd7450?sid=b00bb99e-bd63-414f-a1bb-4e4f64f7fc9a) |
| 🎫 _comingsoon_ | [_comingsoon_](https://www.loom.com/share/your-video-token) |


---

## 🧠 Project Overview

This API gateway:
- Authenticates users via `username + password`
- Issues **JWT tokens** scoped to specific resources (e.g., `hotel`, `event`)
- Validates tokens on protected endpoints
- Logs all access (audit logs)
- Sends alerts for abuse
- Fully deployable to AWS (ECS + Secrets + S3 + CloudWatch)

---

## 📦 Tech Stack

| Layer         | Tech                  |
|---------------|-----------------------|
| Web Framework | FastAPI + Uvicorn     |
| Auth          | JWT (`python-jose`)   |
| Rate Limiting | Redis                 |
| Logging       | AWS S3 / DynamoDB     |
| Alerts        | AWS SNS               |
| Deployment    | Docker + ECS + ECR    |
| Secrets       | AWS Secrets Manager   |
| CI/CD         | GitHub Actions        |

---

## 🧑‍💻 API Endpoints

### `POST /auth/login`
Authenticate the user and issue a **resource-scoped JWT token**.

**Request:**
```json
{
  "username": "saad",
  "password": "1234",
  "resource": "hotel"
}
```

**Response:**
```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

---

### `GET /hotel-db`
Protected endpoint. Requires a token with `"resource": "hotel"`.

**Header:**
```
Authorization: Bearer <JWT>
```

**Response:**
```json
{
  "message": "You accessed hotel data!"
}
```

---

### 🧾 JWT Structure
```json
{
  "sub": "user_123",
  "resource": "hotel",
  "exp": 1725693217
}
```
- `sub` – user ID
- `resource` – the resource this token is scoped to (e.g., hotel, event)
- `exp` – expiration timestamp

---

## ⚙️ Setup & Run

### 1. Clone & Install
```bash
git clone https://github.com/your-username/smart-access-gateway.git
cd smart-access-gateway
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run App
```bash
uvicorn main:app --reload
```

### 3. Redis (for rate limiting)
```bash
docker run -d -p 6379:6379 redis
```

---

## 🌩️ AWS Integration (Advanced)

| Feature  | Service                |
|----------|------------------------|
| Secrets  | AWS Secrets Manager    |
| Logs     | AWS S3 / DynamoDB      |
| Alerts   | AWS SNS                |
| Hosting  | ECS Fargate or EC2     |
| CI/CD    | GitHub Actions         |
| Metrics  | AWS CloudWatch         |

---

## 📁 Folder Structure
```
smart-access-gateway/
├── main.py
├── routes/
│   ├── auth.py
│   ├── hotel.py
│   └── event.py
├── auth/
│   └── token.py
├── db/
│   ├── hotel.py
│   └── event.py
├── middleware/
│   └── verify_token.py
├── schemas.py
├── requirements.txt
└── README.md
```

---

## 🧠 Future Ideas
- 🔁 Refresh token support
- 🔒 Role-based permissions (admin, guest)
- 🚧 Token revocation via Redis
- 🧩 Multi-tenant resource logic

---

## 🧑‍🎓 Author
**Mohammad Saad**  
Backend + Cloud + Security Enthusiast  
🌐 GitHub: [@saad1901](https://github.com/saad1901)  
📌 LinkedIn: [https://www.linkedin.com/in/saad99]