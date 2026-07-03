# GigHub API

## Student Details

Registration Number: C027-01-1885/2023

## Project Description

GigHub API is a FastAPI application that manages freelance gig listings. It allows users to create, retrieve, update, search, and delete freelance gigs.

## Features

- View all gigs
- Filter gigs by category and budget
- View a gig by ID
- Search gigs by title
- Create a new gig
- Update a gig's budget or status
- Delete a gig

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pydantic

## How to Run

1. Install the dependencies:

```bash
pip install fastapi uvicorn
```

2. Run the application:

```bash
python -m uvicorn main:app --reload
```

3. Open your browser and visit:

```
http://127.0.0.1:8000/docs
```

to access the Swagger UI.