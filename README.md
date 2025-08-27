# 👷🛠️ Local Skill Matching System 🛠️👷

Local Skill Matching System, a simple and user-friendly CLI project that helps connect skilled local workers with service requests. It streamlines managing workers, service requests, and reviews, using realistic Kenyan data for demonstration. The system makes it easy to find workers, assign them to tasks, and track feedback efficiently.


## Table of Contents
- [Project Overview](#project-overview)  
- [Features](#features)  
- [Installation](#installation)  
- [How to Use](#how-to-use)  
- [Models & Relationships](#models--relationships)  
- [Seeding Data](#seeding-data)  
- [Dependencies](#dependencies)  
- [Author](#-author)  
- [License](#-license)

---

## Project Overview

The Local Skill Matching System is designed for small businesses or individuals in Kenya to:

- Find local skilled workers quickly.
- Track service requests and their statuses.
- Collect and manage reviews for workers.

This CLI is **interactive, user-friendly, and data-driven**, with clear menus and validations to prevent errors.

---
![WhatsApp Image 2025-08-27 at 18 57 38_ebc79245](https://github.com/user-attachments/assets/6032bf3d-1781-496f-8875-499f6180272c)

## How to Use

1. **Start the CLI**
Run
```
pipenv shell
```
```
python -m lib.cli
```
### Main Menu
Choose a number:  
  1. **Workers**  
  2. **Service Requests**  
  3. **Reviews**  
  0. **Exit**

### Submenus
- Each menu lets you **add, update, delete, list, or search** items.  
- Enter the number to perform an action.  
- Use `0` to go back or exit.

### Entering Data
- Type the requested information when prompted.  
- Leave fields blank during updates to keep existing values.  
- Confirm deletions or changes when asked.

### Viewing Data
- Lists are displayed in **tables**.  
- Worker menus also show related service requests and reviews.

### Exit
- Choose `0` from the Main Menu to exit the application.
```
🙋 Welcome Back Again!! 👋 Goodbye!
```
## Features

### Worker Management
- Add, update, and delete workers.
- Search by ID, name, skill, or location.
- View a worker's service requests and reviews.

### Service Requests
- Create and delete service requests.
- Track request status and view assigned workers.
- Update requests with notes and status changes.

### Reviews
- Add, view, and delete reviews for workers.
- Search reviews by ID.
- Quickly view the worker associated with a review.
---

## Installation

1. Clone the repository:
```
git clone https://github.com/briancheruiyot11/local-skill-matching-system.git
cd LOCAL-SKILL-MATCHING
```
2. Install dependencies using Pipenv:
```
pipenv install
pipenv shell
```
3. Run the CLI:
```
python -m lib.cli
```

## Models & Relationships

### Worker
- **Fields:** id, name, skill, phone, location, created_at  
- **Relations:** has many service requests and reviews  
- **Validation:** name ≥ 2 chars, skill in allowed SKILLS, phone in +2547XXXXXXXX format, location required  

### ServiceRequest
- **Fields:** id, worker_id, requester_name, date, status, notes  
- **Validation:** status in STATUS tuple, date ≥ 2000-01-01  

### Review
- **Fields:** id, worker_id, rating, comment, created_at  
- **Validation:** rating 1–5, comment ≤ 500 chars
 

---

## Seeding Data

The project includes seed scripts using uses **Faker** to generate realistic Kenyan data to sample data:

- **Workers:** 20  
- **Service Requests:** 10  
- **Reviews:** 30  

---

## Dependencies

- **Python 3.8+**  
- **Pipenv** (for dependency management)  
- **SQLAlchemy** (ORM)  
- **tabulate** (for tabular display)  
- **Faker** (for generating seed data)  

---

## 👨‍💻 Author
Created by **Brian Cheruiyot**

## 📄 License
MIT License  
Copyright (c) 2025 Brian Cheruiyot

