# 🤖 PROMURA Automation Features Documentation

Comprehensive automation systems added in v2.2 while preserving the dark feminine UI design.

---

## 📊 1. Auto-Refresh Metrics System

### Overview
Real-time metrics dashboard that updates automatically every 5 seconds without page reload.

### Features
- ✅ System status monitoring (online/offline, uptime)
- ✅ API metrics (total requests, success rate, response times)
- ✅ Post statistics (total, successful, failed, pending)
- ✅ Recent activity feed with timestamps
- ✅ Error logs with categorization
- ✅ Pause/resume controls
- ✅ Last refresh timestamp display

### Implementation
```javascript
// Auto-refresh is initialized automatically on metrics page
// Access controls via global object:
window.metricsAutoRefresh.pause();   // Pause updates
window.metricsAutoRefresh.resume();  // Resume updates
window.metricsAutoRefresh.refresh(); // Manual refresh
```

### File Location
- `app/static/metrics-auto-refresh.js`
- Automatically loaded on `/metrics` page

---

## 📦 2. Bulk Actions for Content Library

### Overview
Perform operations on multiple media items simultaneously.

### Endpoints

#### Bulk Delete
```http
POST /api/library/bulk-delete
Content-Type: application/json
Authorization: Required (edit permission)

{
  "media_ids": ["id1", "id2", "id3"]
}

Response:
{
  "success": true,
  "deleted_count": 3,
  "failed_ids": [],
  "message": "Successfully deleted 3 media items"
}
```

#### Bulk Tag
```http
POST /api/library/bulk-tag
Content-Type: application/json
Authorization: Required (edit permission)

{
  "media_ids": ["id1", "id2"],
  "tags": ["sunset", "beach", "summer"],
  "action": "add"  // or "replace"
}

Response:
{
  "success": true,
  "updated_count": 2,
  "failed_ids": [],
  "message": "Successfully updated tags for 2 media items"
}
```

### Actions
- **add**: Adds new tags to existing tags (keeps old tags)
- **replace**: Replaces all existing tags with new ones

### Usage Example
```javascript
// Select multiple items
const selectedIds = ['media-123', 'media-456', 'media-789'];

// Delete multiple items
await fetch('/api/library/bulk-delete', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ media_ids: selectedIds })
});

// Add tags to multiple items
await fetch('/api/library/bulk-tag', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    media_ids: selectedIds,
    tags: ['promotional', 'Q4-2025'],
    action: 'add'
  })
});
```

---

## 🧠 3. Smart Scheduling Suggestions (AI)

### Overview
AI-powered system that analyzes posting history to recommend optimal posting times.

### Endpoints

#### Get Scheduling Suggestions
```http
GET /api/scheduling/suggestions?count=5
Authorization: Required

Response:
{
  "success": true,
  "suggestions": [
    {
      "datetime": "2025-10-13T10:00:00",
      "day_name": "Monday",
      "time": "10:00 AM",
      "confidence": 85,
      "avg_engagement": 12.5,
      "success_rate": 95.2,
      "reason": "Monday morning - high engagement (23 posts)"
    }
  ],
  "message": "Generated 5 scheduling suggestions"
}
```

#### Get Posting Insights
```http
GET /api/scheduling/insights
Authorization: Required

Response:
{
  "success": true,
  "insights": {
    "status": "success",
    "total_posts": 156,
    "best_day": {
      "day": "Thursday",
      "avg_engagement": 15.8
    },
    "best_hour": {
      "hour": 19,
      "formatted": "19:00",
      "avg_engagement": 18.2
    },
    "insights": [
      "Your best posting day is Thursday",
      "Optimal posting time is around 19:00",
      "Total posts analyzed: 156"
    ]
  }
}
```

### Algorithm Features
- Analyzes historical post performance
- Considers day of week and time of day
- Calculates confidence scores based on sample size
- Provides default optimal times when insufficient data
- Tracks engagement and success rates

### Integration Example
```javascript
// Get suggestions when user clicks "Suggest Times" button
async function getSuggestedTimes() {
  const response = await fetch('/api/scheduling/suggestions?count=5');
  const data = await response.json();

  // Display suggestions to user
  data.suggestions.forEach(suggestion => {
    console.log(`${suggestion.day_name} ${suggestion.time}`);
    console.log(`Confidence: ${suggestion.confidence}%`);
    console.log(`Reason: ${suggestion.reason}`);
  });
}
```

---

## 📝 4. Post Template System

### Overview
Save and reuse post templates for recurring content patterns.

### Endpoints

#### Create Template
```http
POST /api/templates
Content-Type: application/json
Authorization: Required (edit permission)

{
  "name": "Weekly Motivation Monday",
  "content": "Happy Monday! Let's crush this week 💪",
  "models": ["model1", "model2"],
  "tags": ["motivation", "weekly"],
  "media_ids": ["media-123"],
  "schedule_pattern": "weekly"
}

Response:
{
  "success": true,
  "template": {
    "id": "template-uuid",
    "name": "Weekly Motivation Monday",
    "content": "Happy Monday! Let's crush this week 💪",
    "models": ["model1", "model2"],
    "tags": ["motivation", "weekly"],
    "media_ids": ["media-123"],
    "schedule_pattern": "weekly",
    "created_by": "username",
    "created_at": "2025-10-08T15:30:00",
    "updated_at": "2025-10-08T15:30:00",
    "usage_count": 0,
    "last_used": null
  },
  "message": "Template created successfully"
}
```

#### Get All Templates
```http
GET /api/templates
GET /api/templates?tags=motivation,weekly
Authorization: Required

Response:
{
  "success": true,
  "templates": [...],
  "count": 15
}
```

#### Get Single Template
```http
GET /api/templates/{template_id}
Authorization: Required
```

#### Update Template
```http
PUT /api/templates/{template_id}
Content-Type: application/json
Authorization: Required (edit permission)

{
  "name": "Updated Name",
  "content": "Updated content"
}
```

#### Delete Template
```http
DELETE /api/templates/{template_id}
Authorization: Required (admin permission)
```

#### Use Template
```http
POST /api/templates/{template_id}/use
Authorization: Required

Response:
{
  "success": true,
  "template": {
    ...template data with incremented usage_count
  }
}
```

#### Duplicate Template
```http
POST /api/templates/{template_id}/duplicate
Content-Type: application/json
Authorization: Required (edit permission)

{
  "new_name": "Copy of Template Name"
}

Response:
{
  "success": true,
  "template": {...new template},
  "message": "Template duplicated successfully"
}
```

#### Get Popular Templates
```http
GET /api/templates/stats/popular?limit=10
Authorization: Required

Response:
{
  "success": true,
  "templates": [
    {
      "id": "...",
      "name": "Most Used Template",
      "usage_count": 42,
      ...
    }
  ]
}
```

#### Get Recent Templates
```http
GET /api/templates/stats/recent?limit=10
Authorization: Required
```

#### Get Template Statistics
```http
GET /api/templates/stats/overview
Authorization: Required

Response:
{
  "success": true,
  "statistics": {
    "total_templates": 25,
    "total_uses": 387,
    "most_popular": {...template},
    "recently_used": 12
  }
}
```

### Usage Flow
```javascript
// 1. Create a template
const createResponse = await fetch('/api/templates', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: "Daily Morning Post",
    content: "Good morning! ☀️",
    models: ["model1"],
    tags: ["daily", "morning"]
  })
});

// 2. Get all templates
const templates = await fetch('/api/templates').then(r => r.json());

// 3. Use a template
const useResponse = await fetch(`/api/templates/${templateId}/use`, {
  method: 'POST'
});
const templateData = await useResponse.json();

// 4. Pre-fill post form with template data
document.getElementById('content').value = templateData.template.content;
// ... fill other fields
```

### Schedule Patterns
Supported patterns for recurring posts:
- `daily` - Post every day
- `weekly` - Post weekly on specific day
- `biweekly` - Post every two weeks
- `monthly` - Post monthly
- Custom patterns can be defined

---

## 🔐 Authentication & Permissions

All endpoints require authentication. Permissions levels:
- **view**: Read-only access
- **edit**: Can create/update templates and bulk operations
- **admin**: Can delete templates and access all features

### Authentication Headers
```javascript
// Include authentication token in requests
fetch('/api/templates', {
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN_HERE'
  }
});
```

---

## 📁 File Structure

```
app/
├── scheduling_ai.py          # Smart scheduling algorithm
├── template_system.py        # Template management system
├── main.py                   # Updated with new endpoints
├── data/
│   ├── templates.json        # Template storage
│   └── .gitkeep
└── static/
    └── metrics-auto-refresh.js  # Frontend auto-refresh
```

---

## 🚀 Integration Examples

### Complete Workflow: Creating Post from Template

```javascript
async function createPostFromTemplate(templateId) {
  // 1. Use template (increments usage count)
  const response = await fetch(`/api/templates/${templateId}/use`, {
    method: 'POST'
  });
  const { template } = await response.json();

  // 2. Get scheduling suggestions
  const suggestionsResponse = await fetch('/api/scheduling/suggestions?count=3');
  const { suggestions } = await suggestionsResponse.json();

  // 3. Pre-fill post form
  document.getElementById('content').value = template.content;
  document.getElementById('schedule_time').value = suggestions[0].datetime;

  // Select models from template
  template.models.forEach(modelId => {
    document.querySelector(`[data-model-id="${modelId}"]`).checked = true;
  });

  // 4. Submit post
  // ... form submission logic
}
```

### Bulk Tagging Workflow

```javascript
async function bulkTagSelectedItems() {
  // Get selected items from UI
  const selectedItems = Array.from(
    document.querySelectorAll('.media-item.selected')
  ).map(el => el.dataset.mediaId);

  // Get tags from input
  const tags = document.getElementById('bulkTags').value.split(',');

  // Apply tags
  const response = await fetch('/api/library/bulk-tag', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      media_ids: selectedItems,
      tags: tags,
      action: 'add'
    })
  });

  const result = await response.json();
  console.log(`Tagged ${result.updated_count} items`);
}
```

---

## ⚡ Performance Considerations

### Auto-Refresh Metrics
- Updates every 5 seconds by default
- Lightweight JSON payloads (~5-10KB)
- Use pause/resume to conserve resources when tab not in focus

### Bulk Operations
- Process items in batches if dealing with 100+ items
- Failed operations are tracked separately
- Audit logs all bulk actions

### Scheduling AI
- Caches analysis results
- Requires minimum 10 posts for accurate suggestions
- Provides default recommendations with lower confidence

### Templates
- JSON file storage (suitable for 1000s of templates)
- Consider database migration for 10,000+ templates
- Usage tracking is automatic and lightweight

---

## 🎯 Next Steps

To fully utilize these automation features:

1. **Enable auto-refresh** on metrics page (already active)
2. **Create templates** for recurring posts
3. **Use scheduling suggestions** when posting
4. **Implement bulk selection UI** in content library
5. **Monitor template statistics** to optimize workflow

---

## 🐛 Troubleshooting

### Metrics Not Auto-Refreshing
- Check browser console for errors
- Verify `/api/metrics` endpoint is accessible
- Use `window.metricsAutoRefresh.start()` to manually start

### Bulk Operations Failing
- Verify user has "edit" permission
- Check media IDs are valid
- Review audit logs for detailed error messages

### Scheduling Suggestions Empty
- Need at least 10 completed posts for analysis
- Default suggestions provided if insufficient data
- Check completed_posts data structure

### Template Not Saving
- Verify user has "edit" permission
- Check `app/data/` directory is writable
- Review error logs in `app/data/audit_logs.json`

---

**Version**: 2.2.0
**Last Updated**: October 8, 2025
**Maintained By**: PROMURA Team

*All features preserve the dark feminine UI design*
