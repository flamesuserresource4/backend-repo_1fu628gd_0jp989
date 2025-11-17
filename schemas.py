"""
Database Schemas for FreeDAIY

Each Pydantic model represents a collection in MongoDB. The collection name is the lowercase of the class name.
"""
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, EmailStr


class Lead(BaseModel):
    """
    Leads captured from download forms or contact forms
    Collection: "lead"
    """
    email: EmailStr = Field(..., description="Email address")
    name: Optional[str] = Field(None, description="Full name")
    interest: Optional[str] = Field(None, description="Area of interest (voice, n8n, make, self-hosted, consulting)")
    asset: Optional[str] = Field(None, description="Requested asset identifier or slug")
    message: Optional[str] = Field(None, description="Optional note or context")
    source: Optional[str] = Field(None, description="Where the lead came from (download, hire, newsletter)")


class BlogPost(BaseModel):
    """
    Blog posts for FreeDAIY
    Collection: "blogpost"
    """
    title: str = Field(..., description="Post title")
    slug: str = Field(..., description="URL-friendly slug")
    excerpt: Optional[str] = Field(None, description="Short summary")
    content: str = Field(..., description="Markdown or HTML content")
    cover_image: Optional[HttpUrl] = Field(None, description="Cover image URL")
    tags: List[str] = Field(default_factory=list, description="Tags for filtering")


class Product(BaseModel):
    """
    Digital products such as n8n workflows, templates, automations
    Collection: "product"
    """
    title: str = Field(..., description="Product name")
    slug: str = Field(..., description="URL-friendly slug")
    description: Optional[str] = Field(None, description="What it does and how it helps")
    category: str = Field(..., description="Category like n8n, make, voice, infra")
    price: float = Field(0.0, ge=0, description="Price in USD; 0 for free")
    download_url: Optional[HttpUrl] = Field(None, description="Direct download URL if public")
    thumbnail: Optional[HttpUrl] = Field(None, description="Image URL")
