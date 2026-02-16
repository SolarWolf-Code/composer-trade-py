"""Conversation request models."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class MessageContentItem(BaseModel):
    """Message content item."""

    model_config = {"populate_by_name": True}

    type: str = Field(description="Type of content (e.g., 'text')")
    text: str = Field(description="Content text")
    user_content: Optional[str] = Field(None, description="What is returned in client requests")
    user_content_type: Optional[str] = Field(None, description="How to render user content")


class FileItem(BaseModel):
    """File item."""

    model_config = {"populate_by_name": True}

    file_id: str


class CreateConversationRequest(BaseModel):
    """Request to create a new conversation."""

    model_config = {"populate_by_name": True}

    account_id: str = Field(..., description="Account UUID")
    text: Optional[str] = Field(None, description="Initial message text")
    message_content: Optional[List[MessageContentItem]] = Field(
        None, description="Message content items"
    )
    files: Optional[List[FileItem]] = Field(None, description="Files to attach")


class SendMessageRequest(BaseModel):
    """Request to send a message to a conversation."""

    model_config = {"populate_by_name": True}

    text: Optional[str] = Field(None, description="Message text")
    message_content: Optional[List[MessageContentItem]] = Field(
        None, description="Message content items"
    )
    files: Optional[List[FileItem]] = Field(None, description="Files to attach")


class FeedbackActionDetails(BaseModel):
    """Feedback action details."""

    model_config = {"populate_by_name": True}

    action_type: str
    details: Dict[str, Any] = {}


class FeedbackRequest(BaseModel):
    """Request to submit feedback on a conversation."""

    model_config = {"populate_by_name": True}

    message_id: str
    action: FeedbackActionDetails


class UpdateStateRequest(BaseModel):
    """Request to update client state."""

    model_config = {"populate_by_name": True}

    pass
