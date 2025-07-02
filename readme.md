# 🔐 Smart Resource Access Gateway (FastAPI + JWT + AWS)

A production-ready API gateway built with **FastAPI**, designed to authenticate users and issue **resource-scoped JWT tokens** to access separate service backends (like hotel, event management, hospital systems, etc.).

This project also features **rate-limiting (Redis)**, **audit logging (AWS S3 or DynamoDB)**, and **alerting (SNS)** — showcasing scalable, secure backend engineering.

---

## 📽️ Loom Demo Videos

| Feature | Watch |
|--------|-------|
| 🔑 Login + Token Issuance | [Loom Video 1](https://www.loom.com/share/your-video-token) |
| 🎫 Resource Access Control | [Loom Video 2](https://www.loom.com/share/your-video-token) |
| 🚦 Rate Limiting & Alerts | [Loom Video 3](https://www.loom.com/share/your-video-token) |
| ☁️ AWS Logging & Deployment | [Loom Video 4](https://www.loom.com/share/your-video-token) |

---

## 🧠 Project Overview

This API gateway:
- Authenticates users via `username + password`
- Issues **JWT tokens** scoped to specific resources (e.g. `hotel`, `event`)
- Validates tokens on protected endpoints
- Logs all access (audit logs)
- Sends alerts for abuse
- Fully deployable to AWS (ECS + Secrets + S3 + CloudWatch)

---

## 📦 Tech Stack

| Layer           | Tech                  |
|----------------|-----------------------|
| Web Framework   | FastAPI + Uvicorn     |
| Auth            | JWT (`python-jose`)   |
| Rate Limiting   | Redis                 |
| Logging         | AWS S3 / DynamoDB     |
| Alerts          | AWS SNS               |
| Deployment      | Docker + ECS + ECR    |
| Secrets         | AWS Secrets Manager   |
| CI/CD           | GitHub Actions        |

---

## 🧑‍💻 API Endpoints

### `POST /auth/login`
Authenticate the user and issue a **resource-scoped JWT token**.

#### Request:
```json
{
  "username": "saad",
  "password": "1234",
  "resource": "hotel"
}
