# 💎 PROMURA Dashboard - OnlySnarf Multi-Model Management System

A comprehensive web dashboard for managing OnlyFans content across multiple models with advanced scheduling, queue management, real-time monitoring, and sophisticated media library system.

## 🎨 Version 2.1 - Dark Feminine Header & Personalization

**NEW**: Dynamic user greeting with dark feminine aesthetic, motivational quotes system, and enhanced typography with Playfair Display and Lora fonts.

## 🎨 Version 2.0 - Complete Dark Theme Overhaul

Elegant dark theme with glass-morphism effects, SVG icon system, and comprehensive content library for media management.

## 🌟 Features

### Dynamic Personalized Header (NEW v2.1)
- **User-Specific Greeting** - Dynamic "Good [morning/afternoon/evening], [YourName]!" with exclamation and blinking cursor
- **Dark Feminine Aesthetic** - Elegant Playfair Display serif typography with soft purple-pink gradients
- **Motivational Quotes** - 100+ rotating empowering quotes with typewriter animation
- **Sharp & Clear** - High-contrast text optimized for readability (greeting: 2.8rem, name: 3.2rem)
- **Brand Colors** - Purple-pink gradient (#a99de8 → #e0b3d6) with accent highlights (#ff77c6)
- **Performance Optimized** - Minimal animations, no heavy shadows or boxes
- **Fully Responsive** - Scales perfectly across desktop, tablet, and mobile devices

### Multi-Model Management
- **Searchable Model Selector** - Quick search and selection of target models
- **Bulk Operations** - Post to multiple models simultaneously
- **Visual Model Pills** - Selected models displayed as removable tags with soft pink accent
- **Quick Actions** - Select All / Deselect All functionality

### Advanced Queue System
- **Tabbed Interface** - Separate Queue and History views with elegant styling
- **Real-time Status** - SVG icons for post states (Scheduled, Posting, Completed, Failed)
- **Post Actions** - Edit, Cancel, or Delete posts directly from queue
- **Media Thumbnails** - Preview attached images/videos with hover effects
- **Glass-morphism UI** - Semi-transparent cards with backdrop blur effects

### Content Library System (NEW)
- **Centralized Media Storage** - Store and organize all your content in one place
- **Smart Media Management** - Upload, tag, search, and filter images/videos
- **Library-to-Post Workflow** - Select media from library and mix with new uploads
- **Usage Tracking** - Monitor how many times each asset has been used
- **Thumbnail Generation** - Automatic thumbnail creation for quick browsing
- **Search & Filter** - Find media by name, tags, or date
- **Sort Options** - Recent, Popular (by usage), or Alphabetical

### System Monitoring & Metrics
- **Live Status Indicator** - Real-time connection monitoring with animated pulse
- **Auto-refresh** - Dashboard updates every 30 seconds
- **Performance Metrics** - Comprehensive analytics dashboard
  - API success rate and response times
  - Post statistics (completed, scheduled, failed)
  - System status (uptime, memory usage)
  - Recent activity feed
  - Error tracking and logging

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- OnlySnarf installation (optional, runs in mock mode without it)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/onlysnarf-dashboard.git
cd onlysnarf-dashboard
```

2. **Set up virtual environment**
```bash
python3 -m venv dashboard_env
source dashboard_env/bin/activate  # On Windows: dashboard_env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn jinja2 python-multipart
```

4. **Run the dashboard**
```bash
cd app
python main.py
```

5. **Access the dashboard**
Open your browser and navigate to:
```
http://localhost:8000
```

## 📁 Project Structure

```
onlysnarf-dashboard/
├── app/
│   ├── main.py                     # FastAPI application
│   ├── onlysnarf_client.py         # OnlySnarf integration client (mock)
│   ├── real_onlysnarf_client.py    # Production OnlySnarf client
│   ├── profile_manager.py          # Profile management system
│   ├── content_library.py          # Content library backend (NEW)
│   ├── logging_system.py           # Activity and error logging (NEW)
│   ├── templates/
│   │   ├── index.html              # Main dashboard page
│   │   ├── queue.html              # Queue management page
│   │   └── metrics.html            # System metrics dashboard (NEW)
│   └── static/
│       ├── style-elegant.css       # Dark theme styling (NEW)
│       ├── icons.js                # SVG icon system (NEW)
│       ├── content-library.js      # Library management UI (NEW)
│       ├── dashboard.js            # Client-side JavaScript
│       ├── images/
│       │   ├── Promura.png         # Brand logo watermark (NEW)
│       │   └── README.md           # Image documentation
│       ├── library/                # Content library storage (NEW)
│       │   ├── images/
│       │   │   ├── original/
│       │   │   └── thumbnails/
│       │   ├── videos/
│       │   │   ├── original/
│       │   │   └── thumbnails/
│       │   └── metadata.json       # Library metadata
│       └── models/                 # Model avatar images
├── .onlysnarf/                     # Configuration directory
│   └── conf/
│       └── users/                  # User profile configs
├── uploads/                        # Uploaded media files
├── CHANGELOG.md                    # Detailed change history (NEW)
├── README.md                       # This file
└── requirements.txt                # Python dependencies
```

## 🔧 Configuration

### Model Configuration
Models are configured in `main.py`. To add or modify models:

```python
models_data = [
    {"id": 1, "name": "Model Name", "avatar": "/static/models/avatar.jpg", "status": "active"},
    # Add more models here
]
```

### OnlySnarf Integration
The dashboard includes a mock client for testing. To connect to real OnlySnarf:

1. Install OnlySnarf following its documentation
2. Update `onlysnarf_client.py` with actual implementation
3. Configure credentials in `.onlysnarf/conf/users/`

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard page |
| `/queue` | GET | Queue management page |
| `/api/models` | GET | Get available models |
| `/api/queue` | GET | Get queue and history |
| `/api/status` | GET | System status check |
| `/api/history` | GET | Completed posts |
| `/schedule-post` | POST | Schedule a new post |
| `/api/queue/{id}/cancel` | POST | Cancel scheduled post |
| `/api/queue/{id}/edit` | POST | Edit post content |
| `/api/queue/{id}` | DELETE | Delete post |

## 🎨 Features in Detail

### Multi-Model Selector
- Search models by name with instant filtering
- Visual avatars with elegant borders
- Active/inactive status indicators
- Persistent selection across form submissions
- Soft pink accent color for selected models

### Post Scheduling
- Rich text content editor with dark theme
- Multi-file upload support (images & videos)
- DateTime picker with elegant styling
- Immediate or scheduled posting
- Mix library content with new uploads (NEW)

### Content Library (NEW)
- **Upload & Organize**: Add media to library with tags and descriptions
- **Browse & Search**: Filter by type, search by name/tags, sort by popularity
- **Use in Posts**: Click to add library items to new posts
- **Track Usage**: See how many times each media item has been used
- **Smart Management**: Automatic deduplication, thumbnail generation, file size tracking
- **Visual Preview**: Full-screen modal preview for any media item

### Queue Management
- **Queue Tab**: View and manage scheduled posts with glass-morphism cards
- **History Tab**: Review completed posts with engagement metrics
- **Actions**: Edit content, change schedule, cancel posts
- **Visual Status**: SVG icon indicators (no emoji dependencies)
- **Hover Effects**: Smooth animations and elevated shadows

### Real-time Updates
- System status monitoring with animated pulse
- Queue count badges with soft pink accent
- Auto-refresh without page reload
- Metrics dashboard with 5-second auto-refresh
- WebSocket support (optional)

### Dark Theme Design System
- **Glass-morphism**: Semi-transparent cards with backdrop blur
- **Color Palette**: Deep blacks with soft pink accents (#FFDEE2)
- **Typography**: Ultra-light Helvetica/Optima with elegant spacing
- **Animations**: Floating logo, pulsing indicators, smooth transitions
- **Responsive**: Mobile-optimized with comprehensive breakpoints

## 🔐 Security Notes

⚠️ **Important Security Considerations:**
- Credentials are stored in plain text (development only)
- Use environment variables for production
- Implement proper authentication
- Enable HTTPS for production deployment
- Sanitize user inputs

## 🛠️ Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Adding New Features

1. **Backend (FastAPI)**
   - Add endpoints in `main.py`
   - Update data models as needed

2. **Frontend (HTML/JS)**
   - Modify templates in `templates/`
   - Update JavaScript in `static/dashboard.js`
   - Style changes in `static/style.css`

### Mock Mode
The dashboard runs in mock mode by default, simulating OnlySnarf functionality without requiring actual OnlyFans credentials.

## 📊 Performance

- Handles 100+ models efficiently
- Sub-second response times
- Minimal resource usage
- Scalable architecture

## 🐛 Troubleshooting

### Port Already in Use
```bash
lsof -i:8000
kill -9 [PID]
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Permission Denied
```bash
chmod +x main.py
sudo python main.py  # Not recommended
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OnlySnarf project for the automation framework
- FastAPI for the excellent web framework
- The content creator community for feedback

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team
- Check the documentation

## 🚀 Roadmap

### Completed (v2.1)
- [x] Dynamic personalized greeting header
- [x] Dark feminine aesthetic with Playfair Display & Lora fonts
- [x] 100+ motivational quotes system
- [x] Exclamation mark with blinking cursor animation
- [x] Sharp brand gradient colors
- [x] Performance optimizations (removed heavy animations)

### Completed (v2.0)
- [x] Complete dark theme overhaul
- [x] Content library system
- [x] SVG icon replacement
- [x] Metrics dashboard
- [x] Glass-morphism UI
- [x] Mobile responsiveness
- [x] Library-to-post workflow

### Planned (v2.2+)
- [ ] User authentication system
- [ ] Database integration (PostgreSQL/MySQL)
- [ ] Video thumbnail extraction
- [ ] Bulk media operations
- [ ] Advanced tagging with autocomplete
- [ ] AI-powered content suggestions
- [ ] Mobile app companion
- [ ] Webhook integrations
- [ ] Export/Import functionality
- [ ] Multi-language support

---

## 📝 Documentation

- **CHANGELOG.md**: Detailed version history and changes
- **README.md**: This file - setup and feature documentation
- **Code Comments**: Inline documentation throughout source files

---

## 🎨 Design System

### Color Palette
- **Background**: `#0a0a0f`, `#151520`, `#1e1e2e`
- **Accent**: `#FFDEE2` (soft pink), `#ff77c6` (bright pink)
- **Header Gradient**: `#a99de8` → `#e0b3d6` (purple-pink)
- **Text**: `#f8fafc`, `#e8eaed`, `#cbd5e1`, `#d4c5e0`, `#b4a5c7`
- **Cursors**: `#c77dff` (vivid purple)
- **Status**: Success `#10b981`, Warning `#f59e0b`, Error `#ef4444`, Info `#3b82f6`

### Typography
- **Primary**: Inter, -apple-system, BlinkMacSystemFont, Segoe UI
- **Headers**: Playfair Display (serif, 2.8rem), Montserrat (sans-serif, 3.2rem)
- **Quotes**: Lora (italic serif, 1.15rem)
- **Titles**: Helvetica Light, Optima, Bodoni Moda
- **Weight**: Medium (500-600) for headers, Regular (400) for body

### Effects
- **Glass-morphism**: `backdrop-filter: blur(10px)`
- **Shadows**: Multiple elevation levels (sm, md, lg, xl)
- **Transitions**: Cubic-bezier easing (0.4, 0, 0.2, 1)

---

**Built with care for content creators by the PROMURA team**

*Version: 2.1.0*
*Last Updated: October 8, 2025*
*License: MIT*