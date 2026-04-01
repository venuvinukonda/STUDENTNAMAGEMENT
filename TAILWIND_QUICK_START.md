# Tailwind CSS Quick Setup

## 🚀 Quick Start (2 Options)

### Option A: Development with CDN (No Setup Required) ✨

**Best for**: Quick testing, no build tools needed

1. Project is already configured to use Tailwind CDN
2. Just run:
   ```bash
   python manage.py runserver
   ```
3. Visit: http://127.0.0.1:8000/

✅ That's it! Tailwind is ready to use.

---

### Option B: Production Build (Recommended) 🚀

**Best for**: Production deployment, optimized CSS

#### Step 1: Install Node.js
- Download: https://nodejs.org/ (Choose LTS)
- Verify: `node --version` and `npm --version`

#### Step 2: Install Tailwind & Dependencies
```bash
cd SNAPSERVICE
npm install
```

#### Step 3: Build Tailwind CSS

**For Development** (auto-rebuild on file changes):
```bash
npm run dev
```

**For Production** (optimized & minified):
```bash
npm run build:prod
```

#### Step 4: Run Django
In a new terminal:
```bash
python manage.py runserver
```

✅ Done! Now your styles are compiled and optimized.

---

## 📋 Configuration Files Created

| File | Purpose |
|------|---------|
| `tailwind.config.js` | Tailwind customization & theme |
| `postcss.config.js` | CSS processing configuration |
| `package.json` | Node.js dependencies & scripts |
| `static/css/tailwind.css` | Tailwind directives (input) |
| `static/css/output.css` | Compiled CSS (generated, output) |
| `static/css/custom.css` | Additional custom styles |

---

## 🎨 Available NPM Commands

```bash
npm run dev        # Watch mode (rebuild on changes)
npm run build      # One-time build
npm run build:prod # Production build (minified)
```

---

## 💡 Development Workflow

### In Separate Terminals:

**Terminal 1** - Watch Tailwind for changes:
```bash
npm run dev
```

**Terminal 2** - Run Django:
```bash
python manage.py runserver
```

Now:
- Edit any HTML file
- Tailwind automatically rebuilds
- Refresh browser to see changes

---

## 🎯 Pre-configured Components

Use these in your templates:

### Buttons
```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-danger">Delete</button>
<button class="btn btn-success">Save</button>
```

### Forms
```html
<input type="text" class="form-input">
<select class="form-select">
  <option>Option 1</option>
</select>
<textarea class="form-textarea"></textarea>
```

### Cards
```html
<div class="card">
  <div class="card-header">Title</div>
  <div class="card-body">Content</div>
  <div class="card-footer">Footer</div>
</div>
```

### Badges
```html
<span class="badge badge-success">Active</span>
<span class="badge badge-danger">Inactive</span>
```

### Alerts
```html
<div class="alert alert-success">Success!</div>
<div class="alert alert-danger">Error!</div>
```

---

## 🔧 Customizing Theme

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      'brand': '#FF6B22',
    }
  }
}
```

Then use: `<div class="text-brand">Custom Color</div>`

---

## 🚨 Troubleshooting

### Styles not showing
```bash
# Clear cache and rebuild
python manage.py collectstatic --clear
npm run build
```

### npm not found
- Install Node.js: https://nodejs.org/
- Restart terminal
- Run `npm install` again

### CSS not updating
- Kill `npm run dev` and restart it
- Clear browser cache (Ctrl+Shift+Delete)

---

## 📚 Learn More

- **Tailwind Docs**: https://tailwindcss.com/docs
- **Full Guide**: See `TAILWIND_SETUP.md`
- **Tailwind Play**: https://play.tailwindcss.com/

---

**Ready to go!** Start building beautiful UIs with Tailwind CSS 🎨
