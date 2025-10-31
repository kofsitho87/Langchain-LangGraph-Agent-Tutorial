"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

import base64
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from typing import Any, Callable, List, Optional, cast

from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from langchain.tools import tool
from langchain_tavily import TavilySearch
from langgraph.runtime import get_runtime
from pydantic import Field
from typing_extensions import Annotated

from react_agent.context import Context
from react_agent.utils import get_service

calendar = GoogleCalendar(
    "kofsitho@gmail.com", token_path="token.pickle", credentials_path="credentials.json"
)


@tool
async def search(query: str) -> Optional[dict[str, Any]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    runtime = get_runtime(Context)
    wrapped = TavilySearch(max_results=runtime.context.max_search_results)
    return cast(dict[str, Any], await wrapped.ainvoke({"query": query}))


@tool
def get_calendar_events(
    query: Optional[str] = None,
    time_min: Annotated[
        Optional[str],
        Field(
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            description="The start date of the events to get. Format: YYYY-MM-DD (e.g., 2024-01-15)",
        ),
    ] = None,
    time_max: Annotated[
        Optional[str],
        Field(
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            description="The end date of the events to get. Format: YYYY-MM-DD (e.g., 2024-12-31)",
        ),
    ] = None,
) -> Optional[dict[str, Any]]:
    """Get calendar events.

    This function gets calendar events from the Google Calendar API.
    """

    if time_min:
        time_min = datetime.strptime(time_min, "%Y-%m-%d").date()

    if time_max:
        time_max = datetime.strptime(time_max, "%Y-%m-%d").date() + timedelta(days=1)

    events = calendar.get_events(
        query=query,
        time_min=time_min,
        time_max=time_max,
        order_by="startTime",
        single_events=True,
    )

    events_list = [
        {
            "id": event.id,
            "start": event.start.strftime("%Y-%m-%d %H:%M:%S"),
            "end": event.end.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": event.summary,
            "location": event.location,
            "attendees": event.attendees,
            "reminders": event.reminders,
        }
        for event in events
    ]
    return events_list


@tool
def create_calendar_event(
    title: str,
    start: Annotated[
        str,
        Field(
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            description="The start date of the event. Format: YYYY-MM-DD (e.g., 2024-01-15)",
        ),
    ],
    end: Annotated[
        Optional[str],
        Field(
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            description="The end date of the event. Format: YYYY-MM-DD (e.g., 2024-01-15)",
        ),
    ] = None,
    location: Optional[str] = None,
    # attendees: Optional[list[str]] = None,
    # reminders: Optional[list[str]] = None,
) -> bool:
    """Create a calendar event."""
    end = datetime.strptime(end, "%Y-%m-%d").date() if end else None

    event = Event(
        title,
        start=datetime.strptime(start, "%Y-%m-%d").date(),
        end=end,
        location=location,
        # attendees=attendees,
        # reminders=reminders,
    )
    calendar.add_event(event)

    return True


@tool
def delete_calendar_event(
    event_id: Annotated[str, "The id of the event to delete."],
) -> bool:
    """Delete a calendar event."""
    calendar.delete_event(event_id)
    return True


@tool
def get_my_emails() -> Optional[dict[str, Any]]:
    """Get my emails."""

    service = get_service()

    # 최근 이메일 10개 가져오기
    results = service.users().messages().list(userId="me", maxResults=10).execute()
    messages = results.get("messages", [])

    email_list = []

    for msg in messages:
        msg_id = msg["id"]
        msg_data = (
            service.users()
            .messages()
            .get(userId="me", id=msg_id, format="full")
            .execute()
        )

        headers = msg_data["payload"]["headers"]
        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"), "(제목 없음)"
        )
        sender = next(
            (h["value"] for h in headers if h["name"] == "From"), "(보낸이 없음)"
        )

        # 본문 가져오기
        if "parts" in msg_data["payload"]:
            data = msg_data["payload"]["parts"][0]["body"].get("data")
        else:
            data = msg_data["payload"]["body"].get("data")

        if data:
            decoded = base64.urlsafe_b64decode(data)
            msg_body = decoded.decode("utf-8", errors="ignore")
        else:
            msg_body = "(본문 없음)"

        email_list.append(
            {
                "subject": subject,
                "sender": sender,
                "body": msg_body,
            }
        )
    return email_list


@tool
def send_email(to: str, subject: str, body: str) -> bool:
    """Send an email."""
    service = get_service()

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"raw": raw}

    sent = service.users().messages().send(userId="me", body=body).execute()
    print(sent)
    return True


TOOLS: List[Callable[..., Any]] = [
    # search,
    get_calendar_events,
    create_calendar_event,
    delete_calendar_event,
    get_my_emails,
    send_email,
]
