"""Conversation response models."""

from typing import Any

from pydantic import BaseModel


class ConversationResponse(BaseModel):
    """Response from creating a conversation."""

    model_config = {"populate_by_name": True}

    id: str
    message_id: str | None = None
    location: str


class StartingPoint(BaseModel):
    """A starting point for conversation."""

    model_config = {"populate_by_name": True}

    starting_point_id: str
    title: str
    text: str
    icon_id: str | None = None
    index: int


class DiscoverPrompt(BaseModel):
    """A discover prompt."""

    model_config = {"populate_by_name": True}

    text: str
    index: int
    category: str | None = None


class StartingPointsResponse(BaseModel):
    """Response with starting points."""

    model_config = {"populate_by_name": True}

    starting_points: list[StartingPoint] = []
    discover_prompts: list[DiscoverPrompt] = []


class ConversationState(BaseModel):
    """Current conversation state."""

    model_config = {"populate_by_name": True}

    processing_message_id: str | None = None
    processing_message_since: Any | None = None


class ConversationMessage(BaseModel):
    """A message in conversation history."""

    model_config = {"populate_by_name": True}

    role: str | None = None
    type: str | None = None
    content: Any | None = None
    stop_reason: str | None = None
    message_uuid: str | None = None
    content_index: float | None = None


class Conversation(BaseModel):
    """Conversation history."""

    model_config = {"populate_by_name": True}

    id: str
    account_id: str
    starting_point_id: str | None = None
    current_state: ConversationState | None = None
    messages: list[ConversationMessage] = []
