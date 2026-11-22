# Team Task Manager — Full-Stack RBAC Project

A portfolio-ready team task management application built with Django REST Framework, PostgreSQL, JWT authentication, role-based permissions, and React.

## Core capabilities
- JWT login and refresh using Simple JWT.
- Workspace membership with `OWNER`, `ADMIN`, `MEMBER` roles.
- Role-aware API permissions and workspace-scoped data access.
- Create, assign, update, filter, and comment on tasks.
- Task statuses: `TODO`, `IN_PROGRESS`, `DONE`; priorities: `LOW`, `MEDIUM`, `HIGH`.
- Audit-friendly timestamps and server-side validation.
- React UI with login, workspace task board, create-task form, status changes, filters, and comments.
- Docker Compose for PostgreSQL + backend + frontend.
- Backend tests for authentication, workspace isolation, role restrictions, and task workflows.

## Architecture
```text
React (Vite) ── HTTP/JWT ── Django REST Framework ── PostgreSQL
                                  │
                           RBAC + serializers
```

## Quick start (Docker)
Requirements: Docker Desktop.

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:5173
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

Create an admin account:
```bash
docker compose exec backend python manage.py createsuperuser
```

Register a user from the frontend, then create a workspace. The workspace creator becomes its `OWNER`.

## Local development
Backend:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
python manage.py migrate
python manage.py runserver
```
For local development without Docker, set `DATABASE_URL` to a local PostgreSQL database.

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## API overview
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register/` | Register |
| POST | `/api/auth/token/` | Obtain access + refresh JWT |
| POST | `/api/auth/token/refresh/` | Refresh JWT |
| GET/POST | `/api/workspaces/` | List/create workspaces |
| GET/POST | `/api/workspaces/{id}/members/` | List/add members |
| GET/POST | `/api/workspaces/{id}/tasks/` | List/create tasks |
| PATCH/DELETE | `/api/tasks/{id}/` | Update/delete task |
| GET/POST | `/api/tasks/{id}/comments/` | List/add comments |

All task and membership operations are scoped to a workspace the authenticated user belongs to. Only owners/admins can manage workspace membership; members can create tasks and update tasks assigned to them. Owners/admins can update any task in their workspace.

## Role matrix
| Action | Owner | Admin | Member |
|---|---:|---:|---:|
| View workspace/tasks | Yes | Yes | Yes |
| Add/remove members | Yes | Yes | No |
| Create tasks | Yes | Yes | Yes |
| Update any task | Yes | Yes | No |
| Update own assigned task | Yes | Yes | Yes |
| Delete tasks | Yes | Yes | No |

## Security notes
- Passwords use Django's password hashing.
- JWT access tokens are short-lived; refresh tokens rotate and are blacklisted.
- Object-level workspace membership checks prevent cross-workspace access.
- Inputs are validated with serializers.
- CORS is restricted to the configured frontend origin.
- This is a strong learning/portfolio foundation, not a security-audited production service. For production, add HTTPS, managed secrets, rate limiting, observability, backups, and deployment hardening.

## Tests
```bash
cd backend
python manage.py test
```

## Suggested demo flow
1. Register a user.
2. Create a workspace (you become owner).
3. Add a second user as `MEMBER` or `ADMIN`.
4. Create tasks and assign them.
5. Log in as the member and verify that only assigned tasks can be edited.
6. Try accessing a task from a workspace where the user is not a member; the API should return 404.

## Resume bullets (use only after running and verifying)
- Built a full-stack team task management platform using Django REST Framework, PostgreSQL, JWT authentication, and a React frontend.
- Implemented workspace-scoped RBAC for Owner, Admin, and Member roles, with task assignment, status workflows, comments, and API tests.
