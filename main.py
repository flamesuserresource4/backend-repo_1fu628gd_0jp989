import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from database import db, create_document, get_documents
from schemas import Lead, BlogPost, Product

app = FastAPI(title="FreeDAIY API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "FreeDAIY backend is running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["connection_status"] = "Connected"
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:120]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"

    return response


# Simple endpoints to capture leads and list content
class LeadIn(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    interest: Optional[str] = None
    asset: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = None


@app.post("/api/leads")
def create_lead(payload: LeadIn):
    try:
        lead = Lead(**payload.model_dump())
        inserted_id = create_document("lead", lead)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/blogs")
def list_blogs(limit: int = 10):
    try:
        docs = get_documents("blogpost", {}, limit)
        # Convert ObjectId and datetime to strings
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
            for k, v in list(d.items()):
                if hasattr(v, "isoformat"):
                    d[k] = v.isoformat()
        return {"items": docs}
    except Exception as e:
        # Return empty list if no DB configured
        return {"items": [], "note": str(e)}


@app.get("/api/products")
def list_products(limit: int = 12, category: Optional[str] = None):
    try:
        filter_dict = {"category": category} if category else {}
        docs = get_documents("product", filter_dict, limit)
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
            for k, v in list(d.items()):
                if hasattr(v, "isoformat"):
                    d[k] = v.isoformat()
        return {"items": docs}
    except Exception as e:
        return {"items": [], "note": str(e)}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
