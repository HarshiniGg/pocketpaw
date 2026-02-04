# Mission Control

Multi-agent orchestration system for PocketPaw. Coordinate multiple AI agents working together like a team.

## Overview

Mission Control provides a shared workspace where AI agents can:

- **Work on tasks together** - Tasks with lifecycle management (inbox → assigned → in_progress → review → done)
- **Communicate via @mentions** - Agents can mention each other in task comments
- **Share documents** - Create and collaborate on deliverables
- **Stay in sync** - Activity feed shows what's happening in real-time
- **Check in periodically** - Heartbeat system wakes agents to check for work

## Quick Start

### 1. Create Agents

```python
from pocketclaw.mission_control import get_mission_control_manager

manager = get_mission_control_manager()

# Create your first agent
jarvis = await manager.create_agent(
    name="Jarvis",
    role="Squad Lead",
    description="Coordinates the team and handles direct requests",
    specialties=["coordination", "planning", "delegation"],
)

# Create specialized agents
shuri = await manager.create_agent(
    name="Shuri",
    role="Product Analyst",
    description="Skeptical tester who finds edge cases",
    specialties=["testing", "UX", "competitive analysis"],
)
```

### 2. Create Tasks

```python
# Create a task
task = await manager.create_task(
    title="Research competitors",
    description="Analyze top 5 competitors for comparison page",
    priority="high",
    tags=["research", "marketing"],
)

# Assign agents
await manager.assign_task(task.id, [shuri.id])
```

### 3. Communicate

```python
# Post a message (automatically parses @mentions)
await manager.post_message(
    task_id=task.id,
    from_agent_id=jarvis.id,
    content="@Shuri, please start with competitor pricing. @all FYI.",
)

# Shuri gets notified automatically
notifications = await manager.get_notifications_for_agent(shuri.id)
```

### 4. Track Progress

```python
# Update task status
await manager.update_task_status(task.id, "in_progress", agent_id=shuri.id)

# Get activity feed
activities = await manager.get_activity_feed()

# Generate daily standup
standup = await manager.generate_standup()
print(standup)
```

## API Reference

### REST Endpoints

Mission Control exposes a REST API at `/api/mission-control/`:

#### Agents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/agents` | List all agents |
| POST | `/agents` | Create agent |
| GET | `/agents/{id}` | Get agent |
| PATCH | `/agents/{id}` | Update agent |
| DELETE | `/agents/{id}` | Delete agent |
| POST | `/agents/{id}/heartbeat` | Record heartbeat |

#### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List tasks (filter by status, assignee, tags) |
| POST | `/tasks` | Create task |
| GET | `/tasks/{id}` | Get task with messages |
| PATCH | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |
| POST | `/tasks/{id}/assign` | Assign agents |
| POST | `/tasks/{id}/status` | Update status |
| GET | `/tasks/{id}/messages` | Get messages |
| POST | `/tasks/{id}/messages` | Post message |

#### Documents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/documents` | List documents |
| POST | `/documents` | Create document |
| GET | `/documents/{id}` | Get document |
| PATCH | `/documents/{id}` | Update document |
| DELETE | `/documents/{id}` | Delete document |

#### Activity & Stats

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/activity` | Activity feed |
| GET | `/stats` | Dashboard statistics |
| GET | `/standup` | Daily standup report |

#### Notifications

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notifications` | List notifications |
| POST | `/notifications/{id}/delivered` | Mark delivered |
| POST | `/notifications/{id}/read` | Mark read |

### Example API Calls

```bash
# Create an agent
curl -X POST http://localhost:8888/api/mission-control/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "Jarvis", "role": "Squad Lead"}'

# Create a task
curl -X POST http://localhost:8888/api/mission-control/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Research competitors", "priority": "high"}'

# Post a message
curl -X POST http://localhost:8888/api/mission-control/tasks/{task_id}/messages \
  -H "Content-Type: application/json" \
  -d '{"from_agent_id": "{agent_id}", "content": "Starting research now!"}'

# Get activity feed
curl http://localhost:8888/api/mission-control/activity
```

## Data Models

### AgentProfile

```python
{
    "id": "uuid",
    "name": "Jarvis",
    "role": "Squad Lead",
    "description": "Team coordinator",
    "session_key": "agent:jarvis:main",
    "backend": "claude_agent_sdk",
    "status": "idle",  # idle, active, blocked, offline
    "level": "specialist",  # intern, specialist, lead
    "current_task_id": null,
    "specialties": ["coordination", "planning"],
    "last_heartbeat": "2026-02-05T12:00:00Z",
    "created_at": "2026-02-05T10:00:00Z",
    "updated_at": "2026-02-05T12:00:00Z"
}
```

### Task

```python
{
    "id": "uuid",
    "title": "Research competitors",
    "description": "Full competitive analysis",
    "status": "in_progress",  # inbox, assigned, in_progress, review, done, blocked
    "priority": "high",  # low, medium, high, urgent
    "assignee_ids": ["agent-uuid-1", "agent-uuid-2"],
    "creator_id": "agent-uuid",
    "parent_task_id": null,
    "blocked_by": [],
    "tags": ["research", "marketing"],
    "due_date": "2026-02-10T00:00:00Z",
    "started_at": "2026-02-05T10:00:00Z",
    "completed_at": null,
    "created_at": "2026-02-05T09:00:00Z",
    "updated_at": "2026-02-05T10:00:00Z"
}
```

### Message

```python
{
    "id": "uuid",
    "task_id": "task-uuid",
    "from_agent_id": "agent-uuid",
    "content": "Hey @Shuri, please review this!",
    "attachment_ids": ["doc-uuid"],
    "mentions": ["shuri"],  # Extracted from content
    "created_at": "2026-02-05T10:30:00Z"
}
```

### Activity

```python
{
    "id": "uuid",
    "type": "task_created",  # task_created, task_updated, message_sent, etc.
    "agent_id": "agent-uuid",
    "message": "Jarvis created task: Research competitors",
    "task_id": "task-uuid",
    "document_id": null,
    "created_at": "2026-02-05T10:00:00Z"
}
```

### Document

```python
{
    "id": "uuid",
    "title": "Competitor Analysis Report",
    "content": "# Analysis\n\nFindings here...",
    "type": "deliverable",  # deliverable, research, protocol, template, draft
    "task_id": "task-uuid",
    "author_id": "agent-uuid",
    "tags": ["research", "competitors"],
    "version": 2,
    "created_at": "2026-02-05T10:00:00Z",
    "updated_at": "2026-02-05T14:00:00Z"
}
```

### Notification

```python
{
    "id": "uuid",
    "agent_id": "agent-uuid",
    "type": "mention",
    "content": "Jarvis mentioned you in 'Research competitors'",
    "source_message_id": "message-uuid",
    "source_task_id": "task-uuid",
    "delivered": true,
    "read": false,
    "created_at": "2026-02-05T10:30:00Z",
    "delivered_at": "2026-02-05T10:31:00Z"
}
```

## Heartbeat System

The heartbeat daemon periodically wakes agents to check for work.

### Configuration

```python
from pocketclaw.mission_control import get_heartbeat_daemon

# Get daemon (default 15 minute interval)
daemon = get_heartbeat_daemon()

# Or with custom interval
daemon = get_heartbeat_daemon(interval_minutes=5)
```

### Starting the Daemon

```python
async def broadcast_heartbeat(agent_id: str, event_data: dict):
    """Callback for heartbeat events."""
    print(f"Agent {event_data['agent_name']} checked in")
    print(f"  Has work: {event_data['has_work']}")
    print(f"  Notifications: {event_data['unread_notifications']}")
    print(f"  Tasks: {event_data['assigned_tasks']}")

daemon.start(callback=broadcast_heartbeat)
```

### What Happens During a Heartbeat

1. **Wake agent** - Agent's session is activated
2. **Check for work** - Look for:
   - Unread @mentions (urgent)
   - Assigned tasks
   - Activity feed updates
3. **Record heartbeat** - Update `last_heartbeat` timestamp
4. **Update status** - Set to ACTIVE if urgent work, else IDLE
5. **Fire callback** - Notify listeners of the heartbeat

### Manual Triggering

```python
# Trigger heartbeat for specific agent (e.g., after assigning a task)
work_summary = await daemon.trigger_heartbeat(agent_id)
print(f"Agent has {work_summary['assigned_tasks']} tasks")
```

## Storage

Mission Control uses file-based JSON storage at `~/.pocketclaw/mission_control/`:

```
~/.pocketclaw/mission_control/
├── agents.json       # Agent profiles
├── tasks.json        # All tasks
├── messages.json     # Task comments
├── activities.json   # Activity feed
├── documents.json    # Shared documents
└── notifications.json # @mention notifications
```

This follows PocketPaw's design philosophy of simple, transparent, file-based storage that works on any system without database setup.

## Integration with PocketPaw

Mission Control integrates with PocketPaw's existing systems:

- **AgentRouter** - Agents can use any backend (claude_agent_sdk, open_interpreter, etc.)
- **MessageBus** - Activity events can be broadcast via WebSocket
- **Memory System** - Agents maintain their own memory alongside Mission Control state
- **Proactive Daemon** - Heartbeat daemon can share scheduler with intentions

### Starting with Dashboard

The Mission Control API is automatically mounted when running the dashboard:

```bash
pocketclaw dashboard
# API available at http://localhost:8888/api/mission-control/
```

### Manual Integration

```python
from fastapi import FastAPI
from pocketclaw.mission_control import mission_control_router, get_heartbeat_daemon

app = FastAPI()
app.include_router(mission_control_router, prefix="/api/mission-control")

@app.on_event("startup")
async def startup():
    daemon = get_heartbeat_daemon()
    daemon.start()

@app.on_event("shutdown")
async def shutdown():
    daemon = get_heartbeat_daemon()
    daemon.stop()
```

## Inspiration

Mission Control is inspired by [OpenClaw](https://github.com/pbteja1998/openclaw)'s multi-agent system, but designed to be:

- **Simpler** - File-based storage, no external database required
- **More general** - Not hardcoded to marketing/SaaS use cases
- **Integrated** - Built into PocketPaw's existing architecture

## Future Enhancements

Planned features:

- [ ] UI Dashboard for Mission Control
- [ ] WebSocket real-time updates for activity feed
- [ ] Agent execution (actually running agent tasks)
- [ ] Thread subscriptions (auto-notify on task updates)
- [ ] Team templates (pre-configured agent squads)
