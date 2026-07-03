from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI(
    title="GigHub API",
    description="API for managing freelance gigs  C027-01-1885/2023",
    version="1.0.0"
)

# Registration Number: C027-01-1885/2023

gigs_db = [
    {
        "id": 1,
        "title": "Social Media Campaign",
        "description": "Create and manage a social media campaign for a retail business.",
        "category": "Marketing",
        "budget": 500.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "Alice Johnson"
    },
    {
        "id": 2,
        "title": "Sales Data Analysis",
        "description": "Analyze monthly sales data and prepare a detailed report.",
        "category": "Data",
        "budget": 750.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "Brian Mwangi"
    },
    {
        "id": 3,
        "title": "Business Strategy Consulting",
        "description": "Provide strategic consulting services for a growing startup.",
        "category": "Consulting",
        "budget": 1200.0,
        "currency": "USD",
        "status": "In Progress",
        "client_name": "Carol Smith"
    },
    {
        "id": 4,
        "title": "SEO Marketing Project",
        "description": "Improve website ranking using modern SEO techniques.",
        "category": "Marketing",
        "budget": 650.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "David Kimani"
    },
    {
        "id": 5,
        "title": "Customer Data Cleaning",
        "description": "Clean and organize customer records for accurate reporting.",
        "category": "Data",
        "budget": 400.0,
        "currency": "USD",
        "status": "Closed",
        "client_name": "Emily Brown"
    },
    {
        "id": 6,
        "title": "Financial Advisory Session",
        "description": "Advise a small business on budgeting and financial planning.",
        "category": "Consulting",
        "budget": 900.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "Frank Otieno"
    },
    {
        "id": 7,
        "title": "Email Marketing Campaign",
        "description": "Design and execute an email marketing campaign for new customers.",
        "category": "Marketing",
        "budget": 550.0,
        "currency": "USD",
        "status": "In Progress",
        "client_name": "Grace Wanjiku"
    },
    {
        "id": 8,
        "title": "Survey Data Visualization",
        "description": "Create charts and dashboards from survey results.",
        "category": "Data",
        "budget": 700.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "Henry Ouma"
    },
    {
        "id": 9,
        "title": "Operations Consulting",
        "description": "Review business operations and recommend improvements.",
        "category": "Consulting",
        "budget": 1000.0,
        "currency": "USD",
        "status": "Closed",
        "client_name": "Irene Njeri"
    },
    {
        "id": 10,
        "title": "Digital Advertising Project",
        "description": "Plan and manage digital advertising campaigns across platforms.",
        "category": "Marketing",
        "budget": 850.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "John Kamau"
    }
]


# -----------------------------
# Pydantic Models
# -----------------------------

class GigCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=20, max_length=500)
    category: Literal["Marketing", "Data", "Consulting"]
    budget: float = Field(..., gt=0)
    client_name: str = Field(..., min_length=2, max_length=50)


class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["Open", "In Progress", "Closed"]] = None


# -----------------------------
# GET ALL GIGS
# -----------------------------

@app.get("/gigs")
def get_gigs(
    category: Optional[str] = None,
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None
):

    results = gigs_db

    if category:
        results = [
            gig for gig in results
            if gig["category"].lower() == category.lower()
        ]

    if min_budget is not None:
        results = [
            gig for gig in results
            if gig["budget"] >= min_budget
        ]

    if max_budget is not None:
        results = [
            gig for gig in results
            if gig["budget"] <= max_budget
        ]

    return results


# -----------------------------
# GET GIG BY ID
# -----------------------------

@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):

    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig

    raise HTTPException(status_code=404, detail="Gig not found")


# -----------------------------
# SEARCH GIGS
# -----------------------------

@app.get("/gigs/search")
def search_gigs(q: str):

    results = []

    for gig in gigs_db:
        if q.lower() in gig["title"].lower():
            results.append(gig)

    return results


# -----------------------------
# CREATE GIG
# -----------------------------

@app.post("/gigs")
def create_gig(gig: GigCreate):

    new_id = max(g["id"] for g in gigs_db) + 1

    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": "USD",
        "status": "Open",
        "client_name": gig.client_name
    }

    gigs_db.append(new_gig)

    return {
        "message": "Gig created successfully",
        "gig": new_gig
    }


# -----------------------------
# UPDATE GIG
# -----------------------------

@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, update: GigUpdate):

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            if update.budget is not None:
                gigs_db[index]["budget"] = update.budget

            if update.status is not None:
                gigs_db[index]["status"] = update.status

            return {
                "message": "Gig updated successfully",
                "gig": gigs_db[index]
            }

    raise HTTPException(status_code=404, detail="Gig not found")


# -----------------------------
# DELETE GIG
# -----------------------------

@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            deleted = gigs_db.pop(index)

            return {
                "message": "Gig deleted successfully",
                "gig": deleted
            }

    raise HTTPException(status_code=404, detail="Gig not found")