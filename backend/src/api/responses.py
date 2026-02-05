"""
Response formatting module for standardized API responses following Hackathon II requirements.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from enum import Enum


def format_success_response(data: Any = None, message: str = "", timestamp: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Format a successful API response following the Hackathon II standard.

    Args:
        data: Response data (can be a single object or a list)
        message: Optional success message
        timestamp: Optional timestamp (defaults to current time)

    Returns:
        Dictionary with standardized success response format
    """
    if timestamp is None:
        timestamp = datetime.utcnow()

    response = {
        "success": True,
        "data": data,
        "message": message,
        "timestamp": timestamp.isoformat()
    }

    # For collections, add pagination info
    if isinstance(data, list):
        response["total"] = len(data)
        response["page"] = 1  # Default page
        response["limit"] = len(data)  # Default limit

    return response


def format_error_response(error_code: str = "", error_message: str = "", details: Any = None, timestamp: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Format an error API response following the Hackathon II standard.

    Args:
        error_code: Error code
        error_message: Error message
        details: Optional error details
        timestamp: Optional timestamp (defaults to current time)

    Returns:
        Dictionary with standardized error response format
    """
    if timestamp is None:
        timestamp = datetime.utcnow()

    return {
        "success": False,
        "error": {
            "code": error_code,
            "message": error_message,
            "details": details or {}
        },
        "timestamp": timestamp.isoformat()
    }


def format_collection_response(
    data: List[Any],
    message: str = "",
    total: Optional[int] = None,
    page: int = 1,
    limit: int = 10,
    timestamp: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Format a collection response following the Hackathon II standard.

    Args:
        data: List of response data
        message: Optional success message
        total: Total count (defaults to length of data)
        page: Current page number
        limit: Number of items per page
        timestamp: Optional timestamp (defaults to current time)

    Returns:
        Dictionary with standardized collection response format
    """
    if timestamp is None:
        timestamp = datetime.utcnow()

    if total is None:
        total = len(data)

    return {
        "success": True,
        "data": data,
        "message": message,
        "total": total,
        "page": page,
        "limit": limit,
        "timestamp": timestamp.isoformat()
    }