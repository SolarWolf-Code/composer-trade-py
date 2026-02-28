"""AI Agents response models."""

import enum

from pydantic import BaseModel


class AIAgentStatus(enum.StrEnum):
    """AI Agent status."""

    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"


class AIAgent(BaseModel):
    """AI Agent."""

    model_config = {"populate_by_name": True}

    ai_agent_sid: str
    name: str
    description: str | None = None
    prompt_text: str | None = None
    langfuse_starting_point_id: str | None = None
    langfuse_label: str | None = None
    broker_account_id: str
    schedule_cron: str
    schedule_timezone: str
    status: AIAgentStatus
    last_execution_at: str | None = None
    last_execution_status: str | None = None
    next_execution_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AIAgentsResponse(BaseModel):
    """Response from listing AI agents."""

    model_config = {"populate_by_name": True}

    agents: list[AIAgent] = []


class AIExecutionStatus(enum.StrEnum):
    """AI Execution status."""

    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class AIExecutionType(enum.StrEnum):
    """AI Execution type."""

    AUTO = "AUTO"
    MANUAL = "MANUAL"


class AIExecution(BaseModel):
    """AI Agent execution."""

    model_config = {"populate_by_name": True}

    execution_sid: str
    ai_agent_sid: str
    conversation_sid: str | None = None
    prompt_text_snapshot: str | None = None
    langfuse_starting_point_id: str | None = None
    langfuse_label: str | None = None
    langfuse_prompt_version: int | None = None
    status: AIExecutionStatus
    execution_type: AIExecutionType | None = None
    error_message: str | None = None
    started_at: str
    completed_at: str | None = None


class AIExecutionsResponse(BaseModel):
    """Response from listing AI agent executions."""

    model_config = {"populate_by_name": True}

    executions: list[AIExecution] = []
