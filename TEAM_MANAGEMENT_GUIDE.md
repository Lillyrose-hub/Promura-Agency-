# 👥 PROMURA Team Management Guide

**Last Updated:** October 8, 2025
**Version:** 2.3 - Complete User Management System

---

## 🔐 DEFAULT LOGIN CREDENTIALS

### Pre-Created System Accounts

#### **1. Owner Account (Full Access)**
- **Username:** `lea`
- **Password:** `admin123`
- **Role:** Owner
- **Permissions:** Full system access (all)
- **Can:** Manage all features, add/edit/remove users, system configuration

#### **2. Management Account**
- **Username:** `social_manager`
- **Password:** `manager123`
- **Role:** Management
- **Permissions:** `schedule`, `view`, `edit`, `queue`, `captions`, `metrics`
- **Can:** Schedule posts, view analytics, edit content, manage queue, add team members

#### **3. Content Assistant Account**
- **Username:** `content_assistant`
- **Password:** `assistant123`
- **Role:** Content Assistant
- **Permissions:** `view`, `schedule`, `captions`
- **Can:** Create/edit captions, schedule posts, view content library
- **Cannot:** Access analytics, manage team, change system settings

---

## ⚠️ CRITICAL SECURITY WARNING

**🔴 CHANGE ALL DEFAULT PASSWORDS IMMEDIATELY!**

The default passwords (`admin123`, `manager123`, `assistant123`) are **NOT SECURE** and should be changed before:
- Sharing access with team members
- Deploying to production
- Connecting to real social media accounts

### How to Change Password:
1. Login with default credentials
2. Click your username in the top-right
3. Select "Change Password"
4. Enter old password and new password
5. Save changes

---

## 📋 QUICK START FOR BUSINESS PARTNER

### Option 1: Use Existing Account (Quick)
1. Navigate to: `http://your-server:8000/login`
2. Choose appropriate account:
   - **Full Partner Access** → `social_manager` / `manager123`
   - **Content Help Only** → `content_assistant` / `assistant123`
3. Login and **IMMEDIATELY** change password

### Option 2: Create Custom Account (Recommended)
1. Login as Owner: `lea` / `admin123`
2. Go to Team Management: Click 👥 icon or navigate to `/team`
3. Fill out "Add Team Member" form:
   - **Username:** Partner's username (e.g., `sarah_partner`)
   - **Email:** Partner's email address
   - **Password:** Strong temporary password
   - **Full Name:** Partner's actual name
   - **Role:** Select appropriate role (see below)
4. Click "Add Team Member"
5. Share credentials securely with partner
6. Partner should change password on first login

---

## 👑 ROLE DEFINITIONS & PERMISSIONS

### **Owner Role**
**Best for:** Business owners, founders, administrators

**Permissions:**
- ✅ ALL - Complete system access

**Can Do:**
- Add, edit, and remove team members
- Change system configuration
- View all analytics and metrics
- Schedule and publish posts
- Manage content library
- Access audit logs
- Change all settings

**Cannot Do:**
- Nothing - full access

---

### **Management Role**
**Best for:** Social media managers, marketing partners, senior team members

**Permissions:**
- ✅ `schedule` - Schedule and publish posts
- ✅ `view` - View all content
- ✅ `edit` - Edit posts and content
- ✅ `queue` - Manage post queue
- ✅ `captions` - Access caption library
- ✅ `metrics` - View analytics dashboard

**Can Do:**
- Schedule posts to models
- View and analyze performance metrics
- Edit captions and content
- Manage post queue (cancel/reschedule)
- Add/edit/remove team members
- Upload media to content library
- Use bulk actions
- Access scheduling AI suggestions

**Cannot Do:**
- Change system configuration
- Delete owner accounts
- Modify security settings

---

### **Content Assistant Role**
**Best for:** Caption writers, content creators, junior team members

**Permissions:**
- ✅ `view` - View content
- ✅ `schedule` - Schedule posts
- ✅ `captions` - Access caption library

**Can Do:**
- Create and edit captions
- Schedule posts
- View content library
- Upload media
- Suggest post times

**Cannot Do:**
- View analytics or metrics
- Manage team members
- Change user roles
- Access audit logs
- Modify system settings
- Use bulk delete actions

---

## 🎯 ROLE RECOMMENDATION FLOWCHART

```
┌─────────────────────────────────────┐
│ Does partner need FULL control?     │
│ (finances, team, all settings)      │
└────────────┬────────────────────────┘
             │
        ┌────┴────┐
        │   YES   │ → **OWNER ROLE**
        └─────────┘
             │
        ┌────┴────┐
        │    NO   │
        └────┬────┘
             │
┌────────────┴─────────────────────────┐
│ Does partner need analytics access?  │
│ (metrics, performance data)          │
└────────────┬─────────────────────────┘
             │
        ┌────┴────┐
        │   YES   │ → **MANAGEMENT ROLE**
        └─────────┘
             │
        ┌────┴────┐
        │    NO   │ → **CONTENT ASSISTANT ROLE**
        └─────────┘
```

---

## 🚀 ACCESS URLS

- **Login Page:** `http://your-server:8000/login`
- **Main Dashboard:** `http://your-server:8000/`
- **Team Management:** `http://your-server:8000/team`
- **Caption Library:** `http://your-server:8000/captions`
- **Post Queue:** `http://your-server:8000/queue`
- **Analytics:** `http://your-server:8000/metrics`

---

## 🛠️ TEAM MANAGEMENT FEATURES

### Add Team Member
1. Navigate to Team Management page
2. Fill out form in left panel:
   - Username (3-20 characters, alphanumeric)
   - Email address
   - Secure password (min 8 characters)
   - Full name
   - Role selection
3. View permission preview
4. Click "Add Team Member"

### Edit Team Member
1. Locate user in team list (right panel)
2. Click "Edit" button
3. Modal opens with user details
4. Modify:
   - Full name
   - Email address
   - Role (permissions auto-update)
5. View updated permissions
6. Click "Save Changes"

### Remove Team Member
1. Locate user in team list
2. Click "Remove" button
3. Confirm deletion
4. User access revoked immediately

### Restrictions
- ❌ Cannot delete your own account
- ❌ Cannot delete other owner accounts
- ❌ Only owners can manage team members

---

## 📊 STATISTICS TRACKING

Team Management page displays:
- **Total Users** - All active accounts
- **Managers** - Management role count
- **Assistants** - Content Assistant role count

Statistics update in real-time when adding/editing/removing users.

---

## 🔍 AUDIT LOGGING

All team management actions are logged:
- User login/logout
- User creation
- User updates (role changes)
- User deletion
- Permission changes
- Failed login attempts

**View Audit Logs:**
- Owner accounts only
- Navigate to: `/api/audit/logs` (API endpoint)
- Shows: timestamp, username, action, details, IP address

---

## 💡 BEST PRACTICES

### Security
1. ✅ Change all default passwords immediately
2. ✅ Use strong, unique passwords (12+ characters)
3. ✅ Review audit logs regularly
4. ✅ Remove inactive users promptly
5. ✅ Use least-privilege principle (lowest role needed)

### Team Management
1. ✅ Create individual accounts (no sharing)
2. ✅ Use descriptive usernames
3. ✅ Keep email addresses updated
4. ✅ Document who has what access
5. ✅ Review team list monthly

### Onboarding New Team Members
1. Create account with Management/Assistant role
2. Provide temporary password
3. Have them change password on first login
4. Walk through dashboard features
5. Assign specific responsibilities

---

## 🆘 TROUBLESHOOTING

### "Access denied" error
- **Cause:** User doesn't have required permission
- **Fix:** Owner must update user's role to higher level

### Cannot delete user
- **Cause:** Trying to delete owner or self
- **Fix:** Only non-owner users can be deleted, cannot delete yourself

### User not appearing in list
- **Cause:** Page needs refresh
- **Fix:** Reload page or click "Refresh" button

### Forgot password
- **Current:** Owner must manually update password in system files
- **Future:** Password reset feature coming soon

---

## 📞 SUPPORT

For issues or questions:
1. Check this guide first
2. Review audit logs for errors
3. Contact system administrator (Owner)

---

## 🎨 DESIGN NOTES

Team Management page features:
- Dark feminine aesthetic (matching dashboard)
- Gradient purple/pink accents
- Smooth animations
- Responsive design (mobile-friendly)
- Real-time updates
- Beautiful modal popups

---

**Built with PROMURA Dashboard v2.3**
*Empowering creators with elegant, powerful tools* ✨
