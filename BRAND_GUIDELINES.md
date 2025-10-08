# PROMURA Brand Guidelines

## 🎨 Color Palette

### Primary Colors
- **Background Dark**: `#0a0a0a` (Near black)
- **Card Background**: `linear-gradient(135deg, rgba(20, 20, 20, 0.95) 0%, rgba(30, 30, 30, 0.95) 100%)`
- **Primary Gradient**: `linear-gradient(135deg, #7877c6 0%, #ff77c6 100%)` (Purple to Pink)

### Secondary Colors
- **Text Primary**: `#ffffff` (White)
- **Text Secondary**: `#999999` (Light gray)
- **Text Muted**: `#666666` (Medium gray)
- **Border Color**: `rgba(255, 255, 255, 0.1)` (10% white)
- **Border Hover**: `rgba(120, 119, 198, 0.5)` (50% purple)

### Accent Colors
- **Purple Accent**: `#7877c6`
- **Pink Accent**: `#ff77c6`
- **Success**: `#4caf50`
- **Error**: `#ff3b30`
- **Warning**: `#ff9800`

## 🎯 Design Principles

### Visual Style
- **Dark Mode Only**: All interfaces use dark backgrounds
- **Glassmorphic Effects**: Cards with backdrop blur and transparency
- **Subtle Gradients**: Professional gradient overlays
- **Minimal Shadows**: Soft, subtle shadows for depth
- **No Hero Images**: Clean, minimalist approach without stock photos

### Typography
- **Font Family**: `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', sans-serif`
- **Headers**: Bold, gradient text effect for branding
- **Labels**: Uppercase, small, tracked-out text
- **Body**: Clean, readable with proper contrast

### Component Styles

#### Cards
```css
background: linear-gradient(135deg, rgba(20, 20, 20, 0.95) 0%, rgba(30, 30, 30, 0.95) 100%);
backdrop-filter: blur(20px);
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 24px;
```

#### Buttons (Primary)
```css
background: linear-gradient(135deg, #7877c6 0%, #ff77c6 100%);
border-radius: 12px;
text-transform: uppercase;
font-weight: 600;
letter-spacing: 0.5px;
```

#### Input Fields
```css
background: rgba(255, 255, 255, 0.03);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 12px;
color: #fff;
```

#### Navigation Items
```css
color: #999;
transition: all 0.3s ease;
/* Hover state */
color: #fff;
background: rgba(120, 119, 198, 0.1);
```

## 📐 Layout Standards

### Spacing
- **Container Padding**: 48px (desktop), 24px (mobile)
- **Card Padding**: 32px
- **Element Spacing**: 24px between major elements
- **Button Padding**: 16px vertical, 24px horizontal

### Border Radius
- **Cards**: 24px
- **Buttons**: 12px
- **Input Fields**: 12px
- **Small Elements**: 8px

### Animations
- **Transition Duration**: 0.3s
- **Easing Function**: `cubic-bezier(0.4, 0, 0.2, 1)`
- **Hover Effects**: Subtle scale and glow
- **Loading States**: Smooth fade and slide animations

## 🚀 Implementation Checklist

For every new feature, ensure:
- [ ] Dark background (#0a0a0a)
- [ ] Glassmorphic cards with proper backdrop blur
- [ ] Purple-pink gradient for primary actions
- [ ] Uppercase labels with tracking
- [ ] Consistent border radius (24px cards, 12px buttons)
- [ ] Subtle hover animations
- [ ] No hero images or stock photos
- [ ] Professional, minimal aesthetic
- [ ] Consistent spacing and padding
- [ ] Proper text contrast for accessibility

## 💡 Brand Identity

**PROMURA** represents:
- **Professional**: Enterprise-grade quality
- **Modern**: Cutting-edge design and technology
- **Elegant**: Sophisticated and refined
- **Powerful**: Robust functionality
- **Minimal**: Clean, uncluttered interfaces

Every interface should feel premium, professional, and powerful while maintaining simplicity and usability.