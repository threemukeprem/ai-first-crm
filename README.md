# AI-First CRM – HCP Interaction Management System

A production-style **AI-enabled CRM application for Healthcare Professional (HCP) management**, built with **React, FastAPI, PostgreSQL, and cloud deployment services**.

This project demonstrates **full-stack development, REST API design, cloud deployment, database integration, and frontend-backend communication** using modern industry tools.

---

## Live Demo

### Frontend (Vercel)

**https://ai-first-crm-green.vercel.app**

### Backend API (Render)

**https://ai-first-crm-backend-dwf2.onrender.com**

### API Health Check

**https://ai-first-crm-backend-dwf2.onrender.com/health**

---

## Features

### HCP Management

* Add Healthcare Professionals
* View all HCP records
* Delete HCP records
* Persistent cloud database storage
* Automatic UI refresh after CRUD operations

### Backend API

* RESTful FastAPI endpoints
* SQLAlchemy ORM integration
* PostgreSQL database support
* CORS configuration for local and production frontends
* Health and database status monitoring endpoints

### Cloud Deployment

* **Frontend:** Vercel
* **Backend:** Render
* **Database:** Supabase PostgreSQL

---

## Tech Stack

| Layer           | Technology            |
| --------------- | --------------------- |
| Frontend        | React + Vite          |
| HTTP Client     | Axios                 |
| Backend         | FastAPI               |
| ORM             | SQLAlchemy            |
| Database        | PostgreSQL (Supabase) |
| Migrations      | Alembic               |
| Deployment      | Vercel + Render       |
| Version Control | Git + GitHub          |

---

## Project Structure

```
AI_FIRST_CRM/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   ├── alembic/
│   ├── requirements.txt
│   └── alembic.ini
│
└── frontend/
    ├── src/
    │   ├── api/
    │   ├── assets/
    │   ├── App.jsx
    │   └── App.css
    ├── package.json
    └── vite.config.js
```

---

## API Endpoints

### Health

| Method | Endpoint     | Description                 |
| ------ | ------------ | --------------------------- |
| GET    | `/health`    | Backend health status       |
| GET    | `/health/db` | Database connectivity check |

### HCPs

| Method | Endpoint     | Description    |
| ------ | ------------ | -------------- |
| GET    | `/hcps`      | List all HCPs  |
| POST   | `/hcps`      | Create new HCP |
| GET    | `/hcps/{id}` | Get HCP by ID  |
| PATCH  | `/hcps/{id}` | Update HCP     |
| DELETE | `/hcps/{id}` | Delete HCP     |

---

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/threemukeprem/ai-first-crm.git
cd ai-first-crm
```

---

### 2. Backend Setup

```bash
cd backend

python -m venv .venv

# Windows
.venv\\Scripts\\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
DB_HOST=your_supabase_host
DB_PORT=5432
DB_NAME=postgres
DB_USER=your_db_user
DB_PASSWORD=your_db_password

GROQ_API_KEY=your_groq_api_key
```

Run database migrations:

```bash
alembic upgrade head
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```
http://localhost:8000
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at:

```
http://localhost:5173
```

---

## Environment Variables

### Frontend (`.env`)

```env
VITE_API_URL=https://ai-first-crm-backend-dwf2.onrender.com
```

### Backend (`.env`)

```env
DB_HOST=...
DB_PORT=5432
DB_NAME=postgres
DB_USER=...
DB_PASSWORD=...
GROQ_API_KEY=...
```

---

## Deployment Configuration

### Vercel (Frontend)

| Setting          | Value           |
| ---------------- | --------------- |
| Framework        | Vite            |
| Root Directory   | `frontend`      |
| Build Command    | `npm run build` |
| Output Directory | `dist`          |

### Render (Backend)

| Setting        | Value                                              |
| -------------- | -------------------------------------------------- |
| Root Directory | `backend`                                          |
| Build Command  | `pip install -r requirements.txt`                  |
| Start Command  | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

---

## What Makes This Project Different?

Unlike a basic CRUD demo, this project includes:

* **Cloud-native architecture**
* **Separated frontend and backend deployments**
* **Managed PostgreSQL database**
* **Production CORS configuration**
* **Environment-based configuration management**
* **Health monitoring endpoints**
* **Real deployment troubleshooting and debugging workflow**

This reflects a **real-world SaaS-style full-stack application structure** rather than a simple local-only student project.

---

## Skills Demonstrated

### Frontend

* React Hooks (`useState`, `useEffect`)
* Axios API integration
* Form handling
* Dynamic table rendering
* Environment variable management

### Backend

* FastAPI route design
* Dependency injection
* SQLAlchemy ORM operations
* Error handling with HTTP exceptions
* Database session management
* CORS middleware configuration

### DevOps / Deployment

* Git & GitHub workflow
* Vercel deployment pipeline
* Render web service deployment
* Supabase PostgreSQL integration
* Environment variable configuration
* Production debugging and log analysis

---

## Future Enhancements

* Edit / Update HCP records from UI
* Interaction logging module
* Follow-up scheduling system
* AI-generated interaction summaries
* Authentication and role-based access
* Dashboard analytics and reporting
* Search and filtering capabilities
* Docker containerization

---

## Screenshots

Add screenshots here after pushing to GitHub:

```
docs/screenshots/homepage.png
docs/screenshots/add-hcp.png
docs/screenshots/hcp-list.png
```

---

## Resume Project Description

**AI-First CRM – HCP Interaction Management System**

Developed a cloud-deployed full-stack CRM application for managing Healthcare Professionals using **React, FastAPI, SQLAlchemy, PostgreSQL, Render, and Vercel**. Implemented RESTful APIs, PostgreSQL persistence, frontend-backend integration, CORS handling, health monitoring, and production deployment workflows. Demonstrated skills in **full-stack development, API design, cloud deployment, database integration, and environment configuration management**.

---

## Author

**Prem Kumar Threemuke**

* GitHub: **https://github.com/threemukeprem**
* Project Repository: **https://github.com/threemukeprem/ai-first-crm**

---

## Acknowledgements

Built as a **portfolio-grade AI-first CRM project** to demonstrate practical experience with modern **full-stack web development, cloud deployment, and healthcare-focused CRM workflows** using open-source technologies.

---

## License

This project is released under the **MIT License** and is intended for **learning, portfolio, and demonstration purposes**.
