# PROMURA Dashboard - Complete Project Overview

## 🎯 What This Project Is

**PROMURA** is a multi-model content management and scheduling dashboard for OnlyFans creators and agencies. It provides a centralized platform to manage multiple creator accounts, schedule posts, manage captions, and coordinate team members.

---

## 📍 Current Status (As of October 6, 2025)

### ✅ What's Working

**Core Dashboard:**
- ✅ **19 Burner Test Models** - Safe development accounts (testmodel_amber, testmodel_bella, etc.)
- ✅ **346 Captions** - Organized by 7 categories from "Caption Library NEW.xlsx"
- ✅ **Pink Glassmorphic Design** - Brand color #FFDEE2 throughout
- ✅ **Team Management** - Role-based access control (Owner, Manager, Assistant)
- ✅ **Authentication System** - JWT-based with secure login
- ✅ **Multi-page Dashboard** - Dashboard, Queue, Captions, Metrics, Team Management

**Features:**
- Post scheduling with multi-model selection
- Caption library with search and categories
- Content library for media management
- User audit logging
- Real-time system metrics

**Technical Stack:**
- Backend: FastAPI (Python)
- Frontend: Vanilla JavaScript with glassmorphic CSS
- Database: JSON files (captions, users, audit logs)
- Integration: OnlySnarf for OnlyFans API

---

## 🗂️ Project Structure

```
/opt/promura/                           ← MAIN PROJECT LOCATION
├── app/                                ← Application code
│   ├── main.py                         ← Main FastAPI application (882 lines)
│   ├── burner_models.py                ← 19 test models for development
│   ├── auth_system.py                  ← Authentication & user management
│   ├── caption_manager.py              ← Caption library management
│   ├── content_library.py              ← Media/content management
│   ├── logging_system.py               ← Activity logging
│   ├── onlysnarf_client.py             ← OnlyFans API integration
│   ├── real_onlysnarf_client.py        ← Direct OnlySnarf wrapper
│   │
│   ├── data/                           ← Data storage
│   │   ├── captions.json               ← 346 captions from Excel
│   │   ├── users.json                  ← User accounts & permissions
│   │   └── audit_logs.json             ← Activity logs
│   │
│   ├── static/                         ← Frontend assets
│   │   ├── style-elegant.css           ← Main pink glassmorphic styles
│   │   ├── auth.js                     ← Login/auth handling
│   │   ├── dashboard.js                ← Main dashboard logic
│   │   ├── caption-library.js          ← Caption functionality
│   │   ├── content-library.js          ← Media management
│   │   ├── sidebar.js                  ← Navigation
│   │   └── images/
│   │       └── Promura.png             ← Brand logo
│   │
│   ├── templates/                      ← HTML pages
│   │   ├── index.html                  ← Main dashboard
│   │   ├── login.html                  ← Login page
│   │   ├── captions.html               ← Caption library
│   │   ├── queue.html                  ← Post queue
│   │   ├── metrics.html                ← System metrics
│   │   └── team_management.html        ← User management
│   │
│   └── uploads/                        ← Uploaded media files
│
├── data/                               ← Data backup location
│   ├── captions.json
│   └── users.json
│
├── requirements.txt                    ← Python dependencies
├── start-dashboard.sh                  ← Startup script
├── .gitignore                          ← Git ignore rules
└── README.md                           ← Quick reference
```

---

## 🔑 Critical Information

### Server Details
- **IP Address**: 31.220.90.245
- **SSH User**: root
- **SSH Password**: Stargaze154
- **Dashboard URL**: http://31.220.90.245:8000
- **Project Location**: `/opt/promura/`

### Git Repository
- **GitHub**: https://github.com/Lillyrose-hub/Promura-Agency-.git
- **Branch**: main
- **Status**: Clean, properly organized
- **⚠️ Note**: SSH keys NOT set up - requires password for push

### Default Login Credentials
- **Username**: lea
- **Password**: admin123
- **Role**: Owner (full access)

### OnlyFans Account
- **Test Account**: purplefan420
- **Status**: Connected via OnlySnarf
- **Mode**: DRY RUN (safe testing mode)

---

## 🎨 BRANDING STANDARDS - FINAL

**⚠️ THIS IS THE BRAND BIBLE - All future development MUST follow these exact standards**

### Color Palette (OFFICIAL)

**Backgrounds:**
- **Primary Background**: `#0a0a0a` (Deep Charcoal) - Main page background
- **Secondary Background**: `#1a1a1a` to `#2d2d2d` (Dark Gray) - Card backgrounds
- **Glassmorphic Cards**: `linear-gradient(135deg, rgba(20, 20, 20, 0.95), rgba(30, 30, 30, 0.95))` with `backdrop-filter: blur(20px)`

**Accent Colors:**
- **Rose Gold**: `#b76e79` - Primary brand accent
- **Lavender**: `#c4b5fd` - Secondary brand accent
- **Gold Highlights**: `#d4af37` - Decorative accents and emphasis
- **Pink Legacy**: `#FFDEE2` - Maintained for backward compatibility

**Text Colors:**
- **Primary Text**: `#f8fafc` (Warm White) - Main content
- **Secondary Text**: `#c0c0c0` (Soft Silver) - Subheadings and greetings
- **Muted Text**: `#94a3b8` to `#a0a0a0` (Soft Gray) - Supporting text
- **Interactive Hover**: `#a8a7e6` (Purple-tint) - Links and hover states

**Status Colors:**
- **Success**: `#10b981` / `#52d869` (Green)
- **Warning**: `#f59e0b` / `#ffcc00` (Amber/Yellow)
- **Error**: `#ef4444` / `#ff6b63` (Red)

---

### Typography Standards

**Font Stack:**
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', sans-serif;
```

**Alternative Fonts:**
- **Light/Elegant**: `'HelveticaNeue-Light', 'Helvetica Neue Light', 'Optima'`
- **Serif/Quotes**: `'Playfair Display', 'Georgia', serif`
- **Bold/Headers**: `'HelveticaNeue-Bold', 'Helvetica Neue'`

**Text Sizes & Hierarchy:**
- **Page Header**: 36px, weight 800, gradient text
- **Large Name/Title**: 3.5rem (56px), weight 700, gradient
- **Subheader**: 14px, uppercase, letter-spacing 0.5px
- **Greeting Text**: 1.8rem, weight 300
- **Body Text**: 16px (1rem), weight 400
- **Quote Text**: 1.4rem, weight 400, italic, serif
- **Small Text**: 12px, weight 600, uppercase

**Text Styling:**
- Line height: 1.6-1.8 for readability
- Letter spacing: 0.02em-0.1em (subtle elegance)
- Text shadows: `0 2px 8px rgba(0, 0, 0, 0.1)` for depth

---

### Design Principles

**1. Dark Elegant Feminine Aesthetic**
- Sophisticated color gradients (rose gold → lavender)
- Soft, delicate decorative elements (sparkles, quotation marks)
- Refined typography with generous spacing
- Subtle animations that feel graceful, not aggressive

**2. Clean, Minimal Headers**
- ❌ **NO boxes or borders around headers**
- ❌ **NO background containers for headers**
- ✅ Headers float cleanly on page background
- ✅ Use gradient text for visual interest
- ✅ Elegant underlines (gradient lines) instead of boxes

**3. Glassmorphism & Depth**
- Cards use frosted glass effect with blur
- Subtle borders: `1px solid rgba(255, 255, 255, 0.1)`
- Soft rounded corners: 12-20px
- Delicate shadows: `0 4px 20px rgba(0, 0, 0, 0.08)`
- Backdrop filter: `blur(20px)` for depth

**4. Animations & Transitions**
- All transitions: `0.3s ease` or `0.8s cubic-bezier(0.4, 0, 0.2, 1)`
- Staggered reveals for sequential elements
- Smooth gradient sweeps (6-8s infinite)
- Gentle hover effects: scale(1.02), translateY(-2px)
- Floating particle effects for decorative elements

**5. Spacing System**
- Base unit: 8px
- Small spacing: 8-12px
- Medium spacing: 16-24px
- Large spacing: 32-40px
- Section spacing: 40-60px
- Consistent padding in cards: 20-30px

---

### UI Components Standards

**Buttons:**
```css
/* Primary Action Button */
background: linear-gradient(135deg, #7877c6 0%, #ff77c6 100%);
padding: 14px 24px;
border-radius: 10px;
font-weight: 600;
text-transform: uppercase;
letter-spacing: 0.5px;
transition: all 0.3s ease;

/* Hover State */
transform: translateY(-2px);
box-shadow: 0 10px 30px rgba(120, 119, 198, 0.3);
```

**Input Fields:**
```css
background: rgba(255, 255, 255, 0.03);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 10px;
padding: 12px 16px;
color: #fff;

/* Focus State */
border-color: rgba(120, 119, 198, 0.5);
box-shadow: 0 0 0 3px rgba(120, 119, 198, 0.1);
```

**Cards:**
```css
background: linear-gradient(135deg, rgba(20, 20, 20, 0.95) 0%, rgba(30, 30, 30, 0.95) 100%);
backdrop-filter: blur(20px);
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 16-20px;
padding: 30px;
```

**Badges/Pills:**
```css
padding: 4px 12px;
border-radius: 12-20px;
font-size: 11px;
text-transform: uppercase;
letter-spacing: 0.5px;
background: rgba(183, 110, 121, 0.2);
border: 1px solid rgba(183, 110, 121, 0.3);
```

---

### Greeting System Standards

**Typography Hierarchy:**
- Greeting: 1.8rem, weight 300, color #c0c0c0
- Name: 3.5rem, weight 700, rose gold → lavender gradient
- Quote: 1.4rem, serif font, italic, color #f8fafc

**Required Elements:**
- Staggered reveal animations (0.2s, 0.5s, 1s delays)
- Gradient sweep on name (8s cycle)
- Floating sparkle particles (✨)
- Elegant quotation marks in gold (#d4af37)
- Gradient underline beneath name
- Gold decorative lines with author

**Interactive Behavior:**
- Hover on quote: scale(1.02)
- Smooth fade transitions between quotes
- Typing animation for greeting text

---

### Required for All Future Pages

**1. MUST Use Exact Color Palette**
- All backgrounds: #0a0a0a base with card gradients
- All accents: Rose gold (#b76e79) and Lavender (#c4b5fd)
- All text: Warm white (#f8fafc) primary

**2. MUST Follow Typography Standards**
- System font stack for consistency
- Specified sizes for each hierarchy level
- Proper letter-spacing and line-height

**3. MUST Maintain Clean Header Design**
- NO boxes or borders around page headers
- Headers float on background with gradient text
- Elegant underlines instead of containers

**4. MUST Preserve Dark Elegant Feminine Vibe**
- Sophisticated not flashy
- Soft animations and transitions
- Delicate decorative elements
- Generous white space
- Refined color gradients

**5. MUST Use Glassmorphism for Cards**
- Frosted glass effect with backdrop-filter
- Subtle borders and shadows
- Consistent rounded corners

**6. MUST Implement Consistent Spacing**
- 24px base spacing system
- 8px increments for all padding/margins
- Ample white space around all elements

---

### Code Templates

**Page Header (No Box):**
```html
<div class="page-header">
    <h1 class="page-title">Your Title</h1>
    <p class="page-subtitle">Your subtitle</p>
</div>
```
```css
.page-header {
    margin-bottom: 40px;
    padding-bottom: 20px;
    /* NO border, NO background, NO box */
}

.page-title {
    font-size: 36px;
    font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, #999 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
```

**Glassmorphic Card:**
```html
<div class="glass-card">
    <h2 class="section-title">Section Title</h2>
    <!-- Content -->
</div>
```
```css
.glass-card {
    background: linear-gradient(135deg, rgba(20, 20, 20, 0.95) 0%, rgba(30, 30, 30, 0.95) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 30px;
}
```

---

### Responsive Breakpoints

- **Desktop**: 1024px+
- **Tablet**: 768px - 1023px
- **Mobile**: 480px - 767px
- **Small Mobile**: < 480px

**Responsive Rules:**
- Font sizes scale down proportionally
- Padding/spacing reduces by ~25% on mobile
- Cards stack vertically on mobile
- Navigation becomes hamburger menu (if applicable)

---

### File Locations

**Main Stylesheet:**
- `/opt/promura/app/static/style-elegant.css` - Contains all branding standards

**Key Sections in CSS:**
- Lines 165-220: Header styles (clean, no boxes)
- Lines 2900-3400: Greeting system (elegant typography)
- Lines 1490-1900: Content library and cards

**Brand Assets:**
- Logo: `/opt/promura/app/static/images/Promura.png`

---

**Last Updated: October 8, 2025**
**Version: 2.0 - Finalized Branding Standards**

---

## 📊 Data Models

### Caption Structure
```json
{
  "id": "uuid-string",
  "text": "Caption content...",
  "category": "Tip Prompt",
  "source": "Caption Library NEW.xlsx",
  "created_at": "2025-10-02T10:17:27",
  "usage_count": 0
}
```

### User Structure
```json
{
  "username": "lea",
  "password": "hashed_bcrypt",
  "role": "owner",
  "permissions": ["all"],
  "email": "lea@example.com",
  "full_name": "Lea Smith",
  "created_at": "2025-10-01T00:00:00",
  "active": true
}
```

### Burner Model Structure
```json
{
  "id": 1,
  "name": "testmodel_amber",
  "displayName": "Amber Rose",
  "status": "active",
  "tier": "premium",
  "avatar": "/static/models/default.jpg",
  "connected": true,
  "subscribers": 150,
  "posts": 45,
  "earnings": "$1250"
}
```

---

## 🚨 IMPORTANT WARNINGS

### ⚠️ Before Production Deployment

**1. REMOVE BURNER TEST MODELS**
   - File: `/opt/promura/app/burner_models.py`
   - These are fake test accounts
   - Delete this file before going live
   - Or call API endpoint: `/api/models/cleanup-burners`

**2. Change Default Credentials**
   - Current: lea/admin123
   - Update via Team Management page

**3. Enable Real OnlySnarf Authentication**
   - Configure in `.onlysnarf/conf/users/`
   - Switch from DRY_RUN mode to production

**4. Set Up SSH Keys for GitHub**
   - Currently requires password
   - Generate SSH key: `ssh-keygen -t ed25519`
   - Add to GitHub account

**5. Configure Backup System**
   - Data files are NOT in git (see .gitignore)
   - Set up automated backups for:
     - `/opt/promura/app/data/captions.json`
     - `/opt/promura/app/data/users.json`
     - `/opt/promura/app/data/audit_logs.json`

---

## 🔧 How to Start/Stop Dashboard

### Start Dashboard
```bash
ssh root@31.220.90.245
cd /opt/promura
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
```

### Stop Dashboard
```bash
ssh root@31.220.90.245
pkill -9 -f "uvicorn.*8000"
```

### Check if Running
```bash
ps aux | grep uvicorn
curl http://localhost:8000/status
```

### View Logs
```bash
tail -f /opt/promura/dashboard.log
```

---

## 📝 Caption Categories

The system has **7 caption categories** with **346 total captions**:

1. **Tip Prompt** (24 captions) - Request tips from subscribers
2. **Unlock Prompt** (31 captions) - Promote locked content
3. **Bundle Prompt** (23 captions) - Sell content bundles
4. **PPV Captions** (20 captions) - Pay-per-view content
5. **Campaign Ideas** (24 captions) - Marketing campaigns
6. **LIVE BOOST** (20 captions) - Live stream promotions
7. **Mass Message** (204 captions) - Bulk messaging templates

---

## 👥 User Roles & Permissions

### Owner (Full Access)
- Permission: `["all"]`
- Can: Everything including user management
- Default: lea/admin123

### Manager
- Permissions: `["schedule", "view", "edit", "queue", "captions", "metrics"]`
- Can: Schedule posts, manage captions, view metrics
- Cannot: Add/remove users

### Assistant
- Permissions: `["view", "schedule", "captions"]`
- Can: View dashboard, schedule posts, use captions
- Cannot: Edit system settings, manage users

---

## 🔗 Key API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Current user info

### Models
- `GET /api/models` - List all models (19 burners currently)
- `GET /api/burner-models` - Burner test models info

### Captions
- `GET /api/captions` - All captions (346 total)
- `GET /api/captions/stats` - Statistics
- `POST /api/captions/upload` - Upload Excel file
- `POST /api/captions/{id}/use` - Track usage

### Posts
- `POST /schedule-post` - Schedule new post
- `GET /api/queue` - View scheduled posts
- `GET /api/history` - Completed posts

### Team
- `GET /api/team/users` - List users (requires Owner)
- `POST /api/team/add-user` - Add user (requires Owner)
- `DELETE /api/team/delete-user/{username}` - Remove user

### System
- `GET /api/status` - System health check
- `GET /api/metrics` - Dashboard metrics
- `GET /api/audit/logs` - Audit logs (requires Owner)

---

## 📦 Dependencies

**Python Packages** (from requirements.txt):
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- pandas==2.1.3
- openpyxl==3.1.2
- python-multipart==0.0.6
- pydantic==2.5.0
- bcrypt
- PyJWT
- python-jose

---

## 🐛 Known Issues

1. **OnlySnarf Authentication**
   - Currently shows: "No such file or directory: 'snarf'"
   - Running in DRY RUN mode (safe)
   - Need to configure OnlySnarf properly for production

2. **Data Persistence**
   - Using JSON files (not ideal for production)
   - Consider migrating to PostgreSQL/MySQL

3. **No Automated Backups**
   - Data files can be lost
   - Set up cron job for backups

4. **GitHub Push Requires Password**
   - No SSH keys configured
   - Need to generate and add keys

---

## 📚 Related Files

- `ARCHITECTURE.md` - Detailed technical architecture
- `DEPLOYMENT_GUIDE.md` - Step-by-step deployment
- `TROUBLESHOOTING.md` - Common problems and solutions
- `API_REFERENCE.md` - Complete API documentation
- `DEVELOPMENT_GUIDE.md` - How to add features

---

## 🆘 Emergency Contacts

**If Something Breaks:**
1. Check logs: `tail -f /opt/promura/dashboard.log`
2. Restart dashboard: `pkill -f uvicorn && cd /opt/promura && uvicorn app.main:app --host 0.0.0.0 --port 8000 &`
3. Check if port 8000 is blocked: `ss -tlnp | grep 8000`
4. Restore from git: `cd /opt/promura && git status && git restore .`

**GitHub Repository:**
https://github.com/Lillyrose-hub/Promura-Agency-.git

---

*Last Updated: October 6, 2025*
*Dashboard Version: 1.0.0 with Burner Models*
