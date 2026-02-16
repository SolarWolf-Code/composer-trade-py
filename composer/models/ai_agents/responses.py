"""AI Agents response models."""

import enum
from typing import List, Optional
from pydantic import BaseModel


class AIAgentStatus(str, enum.Enum):
    """AI Agent status."""

    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"


class AIAgent(BaseModel):
    """AI Agent."""

    model_config = {"populate_by_name": True}

    ai_agent_sid: str
    name: str
    description: Optional[str] = None
    prompt_text: Optional[str] = None
    langfuse_starting_point_id: Optional[str] = None
    langfuse_label: Optional[str] = None
    broker_account_id: str
    schedule_cron: str
    schedule_timezone: str
    status: AIAgentStatus
    last_execution_at: Optional[str] = None
    last_execution_status: Optional[str] = None
    next_execution_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class AIAgentsResponse(BaseModel):
    """Response from listing AI agents."""

    model_config = {"populate_by_name": True}

    agents: List[AIAgent] = []


class AIExecutionStatus(str, enum.Enum):
    """AI Execution status."""

    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class AIExecutionType(str, enum.Enum):
    """AI Execution type."""

    AUTO = "AUTO"
    MANUAL = "MANUAL"


class AIExecution(BaseModel):
    """AI Agent execution."""

    model_config = {"populate_by_name": True}

    execution_sid: str
    ai_agent_sid: str
    conversation_sid: Optional[str] = None
    prompt_text_snapshot: Optional[str] = None
    langfuse_starting_point_id: Optional[str] = None
    langfuse_label: Optional[str] = None
    langfuse_prompt_version: Optional[int] = None
    status: AIExecutionStatus
    execution_type: Optional[AIExecutionType] = None
    error_message: Optional[str] = None
    started_at: str
    completed_at: Optional[str] = None


class AIExecutionsResponse(BaseModel):
    """Response from listing AI agent executions."""

    model_config = {"populate_by_name": True}

    executions: List[AIExecution] = []
