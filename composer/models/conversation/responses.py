"""Conversation response models."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ConversationResponse(BaseModel):
    """Response from creating a conversation."""

    model_config = {"populate_by_name": True}

    id: str
    message_id: Optional[str] = None
    location: str


class StartingPoint(BaseModel):
    """A starting point for conversation."""

    model_config = {"populate_by_name": True}

    starting_point_id: str
    title: str
    text: str
    icon_id: Optional[str] = None
    index: int


class DiscoverPrompt(BaseModel):
    """A discover prompt."""

    model_config = {"populate_by_name": True}

    text: str
    index: int
    category: Optional[str] = None


class StartingPointsResponse(BaseModel):
    """Response with starting points."""

    model_config = {"populate_by_name": True}

    starting_points: List[StartingPoint] = []
    discover_prompts: List[DiscoverPrompt] = []


class ConversationState(BaseModel):
    """Current conversation state."""

    model_config = {"populate_by_name": True}

    processing_message_id: Optional[str] = None
    processing_message_since: Optional[Any] = None


class ConversationMessage(BaseModel):
    """A message in conversation history."""

    model_config = {"populate_by_name": True}

    role: Optional[str] = None
    type: Optional[str] = None
    content: Optional[Any] = None
    stop_reason: Optional[str] = None
    message_uuid: Optional[str] = None
    content_index: Optional[float] = None


class Conversation(BaseModel):
    """Conversation history."""

    model_config = {"populate_by_name": True}

    id: str
    account_id: str
    starting_point_id: Optional[str] = None
    current_state: Optional[ConversationState] = None
    messages: List[ConversationMessage] = []
