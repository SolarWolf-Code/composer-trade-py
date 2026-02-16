"""Conversation resource for AI conversation/chat endpoints."""

from typing import Optional, Dict, Any, List
from ..models.conversation import (
    CreateConversationRequest,
    SendMessageRequest,
    FeedbackRequest,
    FeedbackActionDetails,
    UpdateStateRequest,
    ConversationResponse,
    StartingPointsResponse,
    Conversation as ConversationModel,
    MessageContentItem,
    FileItem,
)


class Conversation:
    """Resource for AI conversation/chat endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def create(
        self,
        account_id: str,
        text: Optional[str] = None,
        message_content: Optional[List[MessageContentItem]] = None,
        files: Optional[List[FileItem]] = None,
    ) -> ConversationResponse:
        """
        Create a new conversation.

        Args:
            account_id: The account UUID
            text: Initial message text
            message_content: Message content items
            files: Files to attach

        Returns:
            Created conversation response with ID and location
        """
        request = CreateConversationRequest(
            account_id=account_id,
            text=text,
            message_content=message_content,
            files=files,
        )
        response = self._client.post(
            "/api/v1/conversation",
            json=request.model_dump(exclude_none=True),
        )
        return ConversationResponse.model_validate(response)

    def get_starting_points(
        self,
        tools_api_version: Optional[str] = None,
    ) -> StartingPointsResponse:
        """
        Get available starting points for new conversations.

        Args:
            tools_api_version: Optional API version for tools

        Returns:
            Starting points and discover prompts
        """
        params = {}
        if tools_api_version:
            params["tools_api_version"] = tools_api_version
        response = self._client.get(
            "/api/v1/conversation/starting-points",
            params=params if params else None,
        )
        return StartingPointsResponse.model_validate(response)

    def get(self, conversation_id: str) -> ConversationModel:
        """
        Get a conversation by ID.

        Args:
            conversation_id: The conversation UUID

        Returns:
            Conversation details including messages and state
        """
        response = self._client.get(f"/api/v1/conversation/{conversation_id}")
        return ConversationModel.model_validate(response)

    def send_message(
        self,
        conversation_id: str,
        text: Optional[str] = None,
        message_content: Optional[List[MessageContentItem]] = None,
        files: Optional[List[FileItem]] = None,
    ) -> ConversationResponse:
        """
        Send a message to an existing conversation.

        Args:
            conversation_id: The conversation UUID
            text: Message text
            message_content: Message content items
            files: Files to attach

        Returns:
            Updated conversation response
        """
        request = SendMessageRequest(
            text=text,
            message_content=message_content,
            files=files,
        )
        response = self._client.post(
            f"/api/v1/conversation/{conversation_id}",
            json=request.model_dump(exclude_none=True),
        )
        return ConversationResponse.model_validate(response)

    def send_feedback(
        self,
        conversation_id: str,
        message_id: str,
        action_type: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Send feedback on a conversation message.

        Args:
            conversation_id: The conversation UUID
            message_id: The message ID to provide feedback on
            action_type: Type of feedback action
            details: Additional feedback details

        Returns:
            Feedback response
        """
        request = FeedbackRequest(
            message_id=message_id,
            action=FeedbackActionDetails(
                action_type=action_type,
                details=details or {},
            ),
        )
        response = self._client.post(
            f"/api/v1/conversation/{conversation_id}/feedback/action",
            json=request.model_dump(exclude_none=True),
        )
        return response

    def cancel_processing_message(
        self,
        conversation_id: str,
        message_id: str,
    ) -> Dict[str, Any]:
        """
        Cancel a processing message in a conversation.

        Args:
            conversation_id: The conversation UUID
            message_id: The message ID to cancel

        Returns:
            Cancellation response
        """
        response = self._client.delete(
            f"/api/v1/conversation/{conversation_id}/processing-message/{message_id}",
        )
        return response

    def upload_file(
        self,
        file_path: str,
    ) -> Dict[str, Any]:
        """
        Upload a file for use in conversations.

        Args:
            file_path: Path to the file to upload

        Returns:
            Upload response with file ID
        """
        with open(file_path, "rb") as f:
            response = self._client.post(
                "/api/v1/conversation/file",
                files={"file": f},
            )
        return response

    def update_state(
        self,
        conversation_id: str,
        message_uuid: str,
    ) -> Dict[str, Any]:
        """
        Update the client state for a conversation.

        Args:
            conversation_id: The conversation UUID
            message_uuid: The message UUID to update state for

        Returns:
            State update response
        """
        request = UpdateStateRequest()
        response = self._client.post(
            f"/api/v1/conversation/{conversation_id}/state/{message_uuid}",
            json=request.model_dump(exclude_none=True),
        )
        return response
