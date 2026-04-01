# Tailwind CSS Configuration Guide

## Overview
This project now has a complete Tailwind CSS configuration with:
- ✅ **tailwind.config.js** - Tailwind customization
- ✅ **postcss.config.js** - PostCSS setup
- ✅ **package.json** - Node.js dependencies and scripts
- ✅ **static/css/tailwind.css** - Tailwind directives
- ✅ **static/css/custom.css** - Additional custom styles
- ✅ **static/css/output.css** - Compiled CSS (generated after build)

---

## Setup Options

### Option 1: Using CDN (Quick Development) ✨ Default

**Best for**: Quick development, no build process needed

**Steps**:
1. No installation needed
2. The `base.html` is already configured to use CDN
3. Just run the Django server:
   ```bash
   python manage.py runserver
   ```

**File**: `templates/base.html` already has:
```html
<script src="https://cdn.tailwindcss.com"></script>
```

---

### Option 2: Using Build Process (Recommended for Production) 🚀

**Best for**: Production deployment, optimized CSS, custom theme

#### Step 1: Install Node.js & npm
- Download from: https://nodejs.org/ (LTS version)
- Verify installation:
  ```bash
  node --version
  npm --version
  ```

#### Step 2: Install Dependencies
```bash
npm install
```

This installs:
- tailwindcss
- postcss
- autoprefixer
- @tailwindcss/forms
- @tailwindcss/typography
- @tailwindcss/aspect-ratio

#### Step 3: Build Tailwind CSS

**Development Mode** (watch for changes):
```bash
npm run dev
```

**Production Build** (minified):
```bash
npm run build:prod
```

**One-time Build**:
```bash
npm run build
```

#### Step 4: Update base.html

The `base.html` is already configured. To use compiled CSS instead of CDN:

```html
<!-- This is the default - uses compiled CSS -->
<link rel="stylesheet" href="{% static 'css/output.css' %}">

<!-- Uncomment this for CDN fallback -->
<!-- <script src="https://cdn.tailwindcss.com"></script> -->
```

#### Step 5: Collect Static Files
```bash
python manage.py collectstatic
```

#### Step 6: Run Django with Tailwind watch (in separate terminal):
Terminal 1 - Watch Tailwind:
```bash
npm run dev
```

Terminal 2 - Django server:
```bash
python manage.py runserver
```

---

## Configuration Files Explained

### 1. **tailwind.config.js**
Main Tailwind configuration with:

**Custom Theme Colors**:
```javascript
colors: {
  primary: { /* Blue color palette */ },
  secondary: { /* Teal color palette */ }
}
```

**Content Paths** (files scanned for Tailwind classes):
```javascript
content: [
  './templates/**/*.html',
  './students/templates/**/*.html',
  './static/js/**/*.js',
]
```

**Plugins**:
- @tailwindcss/forms - Better form styling
- @tailwindcss/typography - Article styling
- @tailwindcss/aspect-ratio - Aspect ratio utilities

### 2. **postcss.config.js**
Processes CSS through:
- Tailwind - Generates utility classes
- Autoprefixer - Adds browser prefixes

### 3. **static/css/tailwind.css**
Entry point with directives:
```css
@tailwind base;      /* Reset & base styles */
@tailwind components; /* Component classes */
@tailwind utilities;  /* Utility classes */
```

Plus custom component definitions using `@layer`.

### 4. **static/css/output.css**
Generated file (created after running build). This is the actual CSS file served to browsers.

### 5. **static/css/custom.css**
Additional custom styles that complement Tailwind.

---

## Available NPM Scripts

```bash
# Development mode - watches for changes
npm run dev

# One-time build
npm run build

# Optimized production build (minified)
npm run build:prod
```

---

## Custom Components Available

All components are defined using Tailwind's `@layer` directive.

### Form Components
```html
<!-- Text input -->
<input type="text" class="form-input">

<!-- Select dropdown -->
<select class="form-select">
  <option>Option 1</option>
</select>

<!-- Textarea -->
<textarea class="form-textarea"></textarea>

<!-- Label -->
<label class="form-label">Field Label</label>

<!-- Checkbox -->
<input type="checkbox" class="form-checkbox">
```

### Button Styles
```html
<button class="btn btn-primary">Primary Button</button>
<button class="btn btn-secondary">Secondary Button</button>
<button class="btn btn-danger">Delete Button</button>
<button class="btn btn-success">Success Button</button>
<button class="btn btn-warning">Warning Button</button>
<button class="btn btn-outline">Outline Button</button>

<!-- Button Sizes -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary btn-lg">Large</button>
```

### Card Components
```html
<div class="card">
  <div class="card-header">Header</div>
  <div class="card-body">Body Content</div>
  <div class="card-footer">Footer</div>
</div>
```

### Badge Styles
```html
<span class="badge badge-success">Success</span>
<span class="badge badge-danger">Danger</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-info">Info</span>
```

### Alert Boxes
```html
<div class="alert alert-success">Success message</div>
<div class="alert alert-danger">Error message</div>
<div class="alert alert-warning">Warning message</div>
<div class="alert alert-info">Info message</div>
```

### Tables
```html
<table class="table">
  <thead>
    <tr>
      <th>Header 1</th>
      <th>Header 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cell 1</td>
      <td>Cell 2</td>
    </tr>
  </tbody>
</table>
```

### Stat Cards
```html
<div class="stat-card">
  <div class="stat-label">Total Students</div>
  <div class="stat-value">250</div>
</div>
```

---

## Customization Guide

### Adding Custom Colors

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      'brand': '#FF6B22',
      'brand-dark': '#FF5500',
    }
  }
}
```

Usage in HTML:
```html
<div class="bg-brand text-brand-dark">Custom Color</div>
```

### Adding Custom Fonts

```javascript
// In tailwind.config.js
fontFamily: {
  sans: ['Poppins', 'system-ui', 'sans-serif'],
  serif: ['Georgia', 'serif'],
}
```

### Creating Custom Utilities

In `static/css/tailwind.css`:

```css
@layer utilities {
  .custom-utility {
    @apply px-4 py-2 bg-indigo-600 text-white rounded;
  }
}
```

### Extending Breakpoints

```javascript
// In tailwind.config.js
screens: {
  'xs': '320px',
  'sm': '640px',
  'md': '768px',
  'lg': '1024px',
  'xl': '1280px',
  '2xl': '1536px',
}
```

---

## Safe List Configuration

The `tailwind.config.js` includes a safelist to prevent unused class purging:

```javascript
safelist: [
  {
    pattern: /(bg|text|border)-(red|green|blue|...|gray)-(50|100|...900)/,
    variants: ['hover', 'focus', 'active'],
  },
]
```

This ensures dynamic color classes are always included.

---

## Best Practices

### 1. **Use Component Classes**
Instead of:
```html
<div class="px-4 py-2 bg-indigo-600 text-white rounded">Button</div>
```

Use:
```html
<button class="btn btn-primary">Button</button>
```

### 2. **Responsive Design**
```html
<!-- Different styles on mobile and desktop -->
<div class="text-sm md:text-lg lg:text-xl">
  Responsive Text
</div>

<!-- Show/hide on breakpoints -->
<div class="hidden md:block">Visible on desktop</div>
<div class="md:hidden">Visible on mobile</div>
```

### 3. **Dark Mode** (if enabled)
```html
<div class="bg-white dark:bg-gray-800">Light/Dark Background</div>
```

### 4. **Combine with Django Templates**
```html
{% if student.status == 'active' %}
  <span class="badge badge-success">Active</span>
{% else %}
  <span class="badge badge-danger">Inactive</span>
{% endif %}
```

---

## Production Checklist

- [ ] Run `npm run build:prod` to generate optimized CSS
- [ ] Verify `output.css` is generated in `static/css/`
- [ ] Update `settings.py` with `STATIC_ROOT` and `STATIC_URL`
- [ ] Run `python manage.py collectstatic`
- [ ] Test all pages for styling
- [ ] Compress images and assets
- [ ] Test on different browsers
- [ ] Test on mobile devices

---

## Troubleshooting

### Issue: Styles not loading
**Solution**: 
1. Clear browser cache (Ctrl+Shift+Delete)
2. Run `python manage.py collectstatic --clear`
3. Verify CSS file exists in `static/css/output.css`

### Issue: npm not found
**Solution**: Install Node.js from nodejs.org

### Issue: CDN styles work but compiled CSS doesn't
**Solution**: 
1. Run `npm run build`
2. Verify `output.css` exists
3. Clear Django cache: `python manage.py clearall` (if django-extensions installed)

### Issue: Build process slow
**Solution**: This is normal for first build. Subsequent builds are faster with `npm run dev` in watch mode.

---

## File Structure After Setup

```
SNAPSERVICE/
├── node_modules/          # Node dependencies (created after npm install)
├── package.json           # Node configuration ✨ NEW
├── package-lock.json      # Dependency lock file (created after npm install)
├── postcss.config.js      # PostCSS config ✨ NEW
├── tailwind.config.js     # Tailwind config ✨ NEW
├── static/
│   └── css/
│       ├── custom.css     # Custom styles
│       ├── output.css     # Compiled CSS (generated after build)
│       ├── tailwind.css   # Tailwind directives ✨ NEW
│       └── main.js
├── templates/
│   └── base.html          # Updated to use output.css
└── ... (other files)
```

---

## Next Steps

1. **For Development**: Use `npm run dev` to watch for changes
2. **For Production**: Use `npm run build:prod` to generate optimized CSS
3. **Customize**: Edit `tailwind.config.js` to match your brand colors
4. **Learn Tailwind**: Visit https://tailwindcss.com/docs

---

## Resources

- **Tailwind CSS Docs**: https://tailwindcss.com/docs
- **Tailwind Components**: https://tailwindui.com/
- **Tailwind Play**: https://play.tailwindcss.com/ (playground)
- **PostCSS**: https://postcss.org/

---

**Happy Styling!** 🎨
