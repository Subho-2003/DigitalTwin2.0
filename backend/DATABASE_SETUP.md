# Database Setup for Vapi Structured Outputs

This document explains the database setup for storing Vapi structured outputs (call summaries and memories).

## Database Schema

### CallSummary Table
Stores conversation summaries from Vapi calls.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key, auto-increment |
| content | Text | The summary text from Vapi |
| created_at | DateTime | Timestamp when summary was created |

### Memory Table
Stores long-term memory-worthy information from conversations.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key, auto-increment |
| content | Text | The memory content from Vapi |
| source | String(50) | Source of memory (default: "voice") |
| created_at | DateTime | Timestamp when memory was created |

## How It Works

### 1. Webhook Endpoint
When Vapi sends a webhook event with structured outputs, the `/vapi/webhook` endpoint:

1. Receives the webhook payload
2. Extracts structured outputs from: `call.analysis.structuredOutputs`
3. Checks for:
   - `callSummary` → saves to `CallSummary` table
   - `memoryCandidate` → saves to `Memory` table
4. Validates content is meaningful (not empty, >10 characters)
5. Logs all save operations

### 2. API Endpoints

#### Get Summaries
```
GET /api/summaries?limit=100
```
Returns all call summaries, ordered by most recent first.

#### Get Memories
```
GET /api/memories?limit=100
```
Returns all stored memories, ordered by most recent first.

#### Delete Memory
```
DELETE /api/memories/{memory_id}
```
Deletes a specific memory by ID (for user control).

## Database File

The SQLite database file is created at:
```
backend/digital_twin.db
```

This file is automatically created when the application starts if it doesn't exist.

## Webhook Configuration in Vapi

To enable this functionality, configure your Vapi assistant with:

1. **Structured Outputs** enabled
2. **Webhook URL**: `https://your-domain.com/vapi/webhook`
3. **Structured Output Fields**:
   - `callSummary` (string)
   - `memoryCandidate` (string)

## Example Webhook Payload

```json
{
  "type": "call-end",
  "call": {
    "id": "call_123",
    "analysis": {
      "structuredOutputs": {
        "callSummary": "User discussed their goals for next week and expressed interest in learning Spanish.",
        "memoryCandidate": "User wants to learn Spanish for an upcoming trip to Barcelona in March."
      }
    }
  }
}
```

## Testing

### Test Webhook Locally

Use a tool like ngrok to expose your local server:

```bash
ngrok http 8000
```

Then set the webhook URL in Vapi to: `https://your-ngrok-url.ngrok.io/vapi/webhook`

### Test API Endpoints

```bash
# Get summaries
curl http://localhost:8000/api/summaries

# Get memories
curl http://localhost:8000/api/memories

# Delete a memory
curl -X DELETE http://localhost:8000/api/memories/1
```

## Notes

- Database is automatically initialized on application startup
- All database operations use SQLAlchemy ORM
- Database sessions are managed via FastAPI dependencies
- Content validation ensures only meaningful data is saved
- All operations are logged for debugging

