# Project Management System

A terminal-based project and task management system built with Python and curses for Advanced programming class project.

## Features

- User authentication and registration
- Admin account with elevated privileges
- Project creation and management
- Task creation with deadlines and status tracking
- Department-based access control
- User assignment to projects and tasks
- Search functionality for projects, tasks, and users

## Requirements

- Python 3.x
- peewee
- validator_collection
- curses (built-in on Unix/Linux/macOS)

## Installation

```bash
pip install peewee validator-collection
```

## Usage

Run the application:
```bash
python main.py
```

Default admin credentials:
- Username: `admin`
- Password: `admin`

## Database

Uses SQLite (`database.db`) with the following models:
- User
- Project
- Task
- UserAndProjects (many-to-many)
- UserAndTasks (many-to-many)

## Navigation

The interface uses single-key commands:
- `[L]` Log in / `[S]` Sign up
- `[N]` New project / `[P]` Projects / `[T]` Tasks
- `[F]` Find / `[E]` Edit / `[B]` Back

---

*readme written with AI.*