# 🚀✨ Smart Resource Access Gateway ✨🚀

> **A blazing-fast, secure API gateway for resource-scoped JWT authentication, event management, and more!**

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/your-username/smart-access-gateway/actions)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 📖 What is this project about?

Smart Resource Access Gateway is a FastAPI-based API gateway that authenticates users, issues resource-scoped JWT tokens, and provides a robust event management backend. It features rate limiting (Redis), audit logging (AWS S3/DynamoDB), alerting (SNS), and is designed for scalable, secure backend engineering. The project is production-ready, cloud-deployable, and developer-friendly.

---

## 🧑‍💻 Event API Endpoints

> **Note:** 🏨 Hotel endpoints are **not yet implemented**. The following endpoints are for the Event system only.

### 📊 Visual API Flow

```mermaid
graph TD
    A[User] -->|POST /events/login| B[Login]
    B -->|JWT| A
    A -->|GET /events/getuser| C[Get User]
    A -->|GET /events/getalluser| D[Get All Users]
    A -->|POST /events/adduser| E[Add User]
    A -->|GET /events/events| F[Get Events]
    A -->|POST /events/addevent| G[Add Event]
    A -->|GET /events/orginfo| H[Get Org Info]
    A -->|PUT /events/orginfo| I[Update Org Info]
    A -->|GET /events/participants| J[Get Participants]
    A -->|GET /events/getupi| K[Get UPI IDs]
    A -->|POST /events/addupi| L[Add UPI]
    A -->|PUT /events/updateupi| M[Update UPI]
    A -->|DELETE /events/deleteupi| N[Delete UPI]
```

---

### 📝 Endpoint Details

<details>
<summary>🔑 <b>POST /events/login</b></summary>

Authenticate and get a JWT token.

**Request:**
```json
{
  "username": "saad",
  "password": "1234"
}
```
**Response:**
```json
{
  "Token": "Bearer <JWT>",
  "Token Type": "access/jwt"
}
```
</details>

<details>
<summary>👤 <b>GET /events/getuser</b></summary>

Get current user info (JWT required).

**Header:**
```
Authorization: Bearer <JWT>
```
**Response:**
```json
{
  "id": 1,
  "username": "saad",
  ...
}
```
</details>

<details>
<summary>👥 <b>GET /events/getalluser</b></summary>

Get all users.

**Response:**
```json
[
  { "id": 1, "username": "saad", ... },
  { "id": 2, "username": "alex", ... }
]
```
</details>

<details>
<summary>➕ <b>POST /events/adduser</b></summary>

Add a new user (superuser JWT required).

**Request:**
```json
{
  "username": "alex",
  "password": "pass",
  "email": "alex@email.com",
  "first_name": "Alex",
  "last_name": "Smith"
}
```
**Response:**
```json
{ "User Added Succesfully" }
```
</details>

<details>
<summary>🗓️ <b>GET /events/events</b></summary>

Get all events (JWT required).

**Response:**
```json
[
  {
    "title": "Chess Tournament",
    "max_participants": 100,
    "status": "published",
    ...
  }
]
```
</details>

<details>
<summary>🆕 <b>POST /events/addevent</b></summary>

Add a new event.

**Request:**
```json
{
  "title": "Chess Tournament",
  "max_participants": 100,
  "status": "published",
  ...
}
```
</details>

<details>
<summary>🏢 <b>GET /events/orginfo</b></summary>

Get organization info.

**Response:**
```json
{
  "name": "Event Org",
  "add": "123 Main St",
  "wp": "+1234567890",
  "email": "org@email.com"
}
```
</details>

<details>
<summary>🏢 <b>PUT /events/orginfo</b></summary>

Update organization info.

**Request:**
```json
{
  "name": "Event Org",
  "add": "123 Main St",
  "wp": "+1234567890",
  "email": "org@email.com"
}
```
**Response:**
```json
{ "Details Updated Sucessfully" }
```
</details>

<details>
<summary>🧑‍🤝‍🧑 <b>GET /events/participants</b></summary>

Get all participants.

**Response:**
```json
[
  {
    "full_name": "John Doe",
    "registration_id": "...",
    "status": "registered",
    ...
  }
]
```
</details>

<details>
<summary>🏦 <b>GET /events/getupi</b></summary>

Get all UPI IDs.

**Response:**
```json
[
  { "id": 1, "name": "Org UPI", "upi_id": "org@upi", "nickname": "main" }
]
```
</details>

<details>
<summary>➕ <b>POST /events/addupi</b></summary>

Add a new UPI ID.

**Request:**
```json
{
  "name": "Org UPI",
  "upi_id": "org@upi",
  "nickname": "main"
}
```
**Response:**
```json
{ "Success" }
```
</details>

<details>
<summary>✏️ <b>PUT /events/updateupi</b></summary>

Update a UPI ID.

**Request:**
```json
{
  "id": 1,
  "name": "Org UPI",
  "upi_id": "org@upi",
  "nickname": "main"
}
```
**Response:**
```json
{ "details": "UPI ID updated Successfully" }
```
</details>

<details>
<summary>❌ <b>DELETE /events/deleteupi</b></summary>

Delete a UPI ID.

**Query Param:** `id=1`

**Response:**
```json
{ "details": "UPI ID deleted Successfully" }
```
</details>

---

## 🗂️ Folder Structure

```text
project/
├── main.py
├── routers/         # 🚦 API Routers
│   ├── events.py
│   ├── hotels.py
│   ├── jwtSec.py
│   └── test.py
├── config/          # ⚙️ Config & Dependencies
│   ├── authentication.py
│   └── dependencies.py
├── models/          # 🗄️ Data Models
│   ├── djangomodels.py
│   ├── Emodels.py
│   └── Hmodels.py
├── structure/       # 🏗️ Domain Structures
│   ├── Event.py
│   └── Hotel.py
├── testing/         # 🧪 Tests & Hashing
│   ├── __init__.py
│   ├── hashing.py
│   └── testmain.py
├── requirements.txt
├── Dockerfile
└── readme.md
```

---

## 🧠 Future Ideas
- 🔁 Refresh token support
- 🔒 Role-based permissions (admin, guest)
- 🚧 Token revocation via Redis
- 🧩 Multi-tenant resource logic

---

## 👨‍💻 Author & Credits

**Mohammad Saad**  
Backend + Cloud + Security Enthusiast  
[![GitHub](https://img.shields.io/badge/GitHub-@saad1901-black?logo=github)](https://github.com/saad1901)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-saad99-blue?logo=linkedin)](https://www.linkedin.com/in/saad99)

---

<p align="center">
  Made with ❤️ by Mohammad Saad
</p>