# Mode Manager Integration Guide

## 🔗 Integrating ModeSwitch Component into Dashboard

### Step 1: Locate Your Dashboard Component

Find your main dashboard or admin panel component. Common locations:
- `application/Frontend/src/pages/Dashboard.jsx`
- `application/Frontend/src/pages/Admin.jsx`
- `application/Frontend/src/App.jsx` (if single-page)

### Step 2: Import ModeSwitch Component

```jsx
// In your Dashboard/Admin component file
import ModeSwitch from '../components/ModeSwitch';
// OR
import ModeSwitch from '../components/ModeSwitch.jsx';
```

### Step 3: Add to JSX

Find the admin or settings section and add:

```jsx
function AdminDashboard() {
  return (
    <div className="admin-container">
      <h1>System Administration</h1>
      
      <section className="admin-section">
        <h2>System Configuration</h2>
        <ModeSwitch />
      </section>

      {/* Other admin features ... */}
    </div>
  );
}
```

### Step 4: Optional - Add CSS Styling

The ModeSwitch component includes inline styles, but you can customize with CSS:

```css
/* In your admin.css or dashboard.css */

.mode-switch-container {
  background: linear-gradient(135deg, #0a0e27 0%, #16213e 100%);
  border: 2px solid #00d4ff;
  padding: 20px;
  border-radius: 8px;
  margin: 20px 0;
}

.mode-switch-header {
  color: #00d4ff;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
}

.mode-buttons {
  gap: 10px;
  margin-bottom: 15px;
}

.mode-config {
  color: #00ff00;
  font-family: 'Courier New', monospace;
  font-size: 12px;
}
```

### Step 5: Test Integration

1. **Start your frontend:**
   ```bash
   cd application/Frontend
   npm start
   ```

2. **Navigate to admin panel**
   - Open http://localhost:5173 (or your Vite port)
   - Login if required
   - Go to admin/settings section

3. **Test mode switching:**
   - Click DEV button - should show development config
   - Click PROD button - should show production config
   - Click TOGGLE button - should switch between modes
   - Verify config details display correctly

4. **Check console for errors:**
   - Open DevTools (F12)
   - Look for any fetch/network errors
   - Check console tab for JavaScript errors

---

## 🔌 Using Mode Manager in Your Code

### Example 1: Conditional Behavior Based on Mode

```javascript
// In your service or utility file
async function getSystemConfig() {
  const token = localStorage.getItem('authToken');
  const response = await fetch('http://localhost:3000/api/admin/mode', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const data = await response.json();
  return data.data; // {currentMode, config}
}

// Use in your components
const config = await getSystemConfig();

if (config.currentMode === 'production') {
  console.log = () => {}; // Suppress logs
  useStrictValidation();
} else {
  console.log = console.originalLog; // Enable logs
  useRelaxedValidation();
}
```

### Example 2: Adjust API Timeouts Based on Mode

```javascript
// In your API client
const getTimeout = async () => {
  const token = localStorage.getItem('authToken');
  const response = await fetch('http://localhost:3000/api/admin/mode', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const data = await response.json();
  const mode = data.data.currentMode;
  
  // Use appropriate timeout
  return mode === 'production' ? 8000 : 12000;
};

// When making requests
const timeout = await getTimeout();
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), timeout);

fetch(url, { signal: controller.signal })
  .finally(() => clearTimeout(timeoutId));
```

### Example 3: Show Development Warnings

```jsx
// In your component
import { useState, useEffect } from 'react';

function MyComponent() {
  const [isDev, setIsDev] = useState(false);

  useEffect(() => {
    // Check if we're in dev mode
    const token = localStorage.getItem('authToken');
    fetch('http://localhost:3000/api/admin/mode', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(r => r.json())
      .then(data => setIsDev(data.data.currentMode === 'development'));
  }, []);

  return (
    <div>
      {isDev && (
        <div style={{
          background: '#ffcc00',
          color: '#000',
          padding: '10px',
          marginBottom: '10px'
        }}>
          ⚠️ Running in DEVELOPMENT mode - not for production use
        </div>
      )}
      {/* Your component content */}
    </div>
  );
}
```

---

## 🔑 API Integration Patterns

### Pattern 1: Get Current Configuration

```javascript
async function getCurrentConfig() {
  const token = localStorage.getItem('authToken');
  
  const response = await fetch(
    'http://localhost:3000/api/admin/mode',
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to get mode: ${response.status}`);
  }

  const data = await response.json();
  return {
    mode: data.data.currentMode,
    config: data.data.config
  };
}

// Usage
const { mode, config } = await getCurrentConfig();
console.log(`Current mode: ${mode}`);
console.log(`Rate limit: ${config.rateLimitRequests}`);
```

### Pattern 2: Toggle Mode

```javascript
async function toggleMode() {
  const token = localStorage.getItem('authToken');
  
  const response = await fetch(
    'http://localhost:3000/api/admin/mode/toggle',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to toggle mode: ${response.status}`);
  }

  const data = await response.json();
  return {
    message: data.message,
    newMode: data.config.currentMode || data.config // Check API response structure
  };
}

// Usage
try {
  const result = await toggleMode();
  console.log(result.message); // "Mode toggled successfully"
  console.log(`New mode: ${result.newMode}`);
} catch (error) {
  console.error('Error:', error);
}
```

### Pattern 3: Set Specific Mode

```javascript
async function setMode(mode) {
  if (!['development', 'production'].includes(mode)) {
    throw new Error("Mode must be 'development' or 'production'");
  }

  const token = localStorage.getItem('authToken');
  
  const response = await fetch(
    'http://localhost:3000/api/admin/mode/set',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ mode })
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || `Failed to set mode: ${response.status}`);
  }

  const data = await response.json();
  return data;
}

// Usage
try {
  const result = await setMode('production');
  console.log('Mode set successfully');
} catch (error) {
  console.error('Error:', error.message);
}
```

---

## 🎨 Styling and Theming

### Custom Styles for ModeSwitch

```jsx
import ModeSwitch from '../components/ModeSwitch';
import './ModeSwitch.custom.css';

// The component already has cyberpunk styling, but you can:
// 1. Override with CSS
// 2. Wrap in a custom container
// 3. Add additional styling
```

### CSS Customization

```css
/* Override cyberpunk colors */
.mode-button.dev {
  background-color: #00ffff; /* Custom cyan */
  color: #000;
}

.mode-button.prod {
  background-color: #ff0000; /* Custom red */
  color: #fff;
}

/* Add animations */
.mode-switch-container {
  animation: slideIn 0.3s ease-in;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## 🧪 Testing Integration

### Manual Testing Checklist

- [ ] Component renders without errors
- [ ] Can click DEV button
- [ ] Can click PROD button
- [ ] Can click TOGGLE button
- [ ] Configuration displays correctly
- [ ] Mode changes reflect in config display
- [ ] Error messages show if JWT missing
- [ ] Error messages show if API fails
- [ ] Loading state shows during requests
- [ ] Works with real backend (not just mock)

### Automated Testing

```javascript
// Example test using Jest + React Testing Library
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ModeSwitch from './ModeSwitch';

describe('ModeSwitch Component', () => {
  beforeEach(() => {
    localStorage.setItem('authToken', 'test-token-12345');
    global.fetch = jest.fn();
  });

  test('renders mode switch buttons', () => {
    render(<ModeSwitch />);
    expect(screen.getByText(/DEV/i)).toBeInTheDocument();
    expect(screen.getByText(/PROD/i)).toBeInTheDocument();
  });

  test('fetches and displays current mode', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        data: {
          currentMode: 'development',
          config: {
            logLevel: 'debug',
            rateLimitRequests: 1000
          }
        }
      })
    });

    render(<ModeSwitch />);

    await waitFor(() => {
      expect(screen.getByText(/development/i)).toBeInTheDocument();
    });
  });

  test('toggles mode on button click', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        message: 'Mode toggled',
        config: { currentMode: 'production' }
      })
    });

    render(<ModeSwitch />);

    const toggleBtn = screen.getByText(/TOGGLE/i);
    fireEvent.click(toggleBtn);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalled();
    });
  });
});
```

---

## 🚀 Production Deployment

### Pre-Deployment Checklist

- [ ] ModeSwitch component integrated
- [ ] Component tested in browser
- [ ] Backend endpoints verified working
- [ ] JWT authentication confirmed
- [ ] Component styled to match dashboard
- [ ] Error handling works correctly
- [ ] Loading states display properly
- [ ] Component placed in correct location
- [ ] Documentation updated
- [ ] Team trained on mode switching

### Deployment Steps

```bash
# 1. Ensure backend is running with ModeManager
cd application/Backend
npm start

# 2. Build frontend with component
cd application/Frontend
npm run build

# 3. Serve frontend
npm start

# 4. Verify mode switching works
# Navigate to admin panel and test

# 5. Set production mode
python mode_switcher.py prod

# 6. Deploy to production
# ... your deployment process ...
```

---

## 📊 Monitoring Mode Changes

### Log Mode Changes

The ModeManager logs all mode changes. You can:

1. **Watch backend logs:**
   ```bash
   # Tail logs to see mode changes
   tail -f application/Backend/logs/system.log | grep "Mode"
   ```

2. **Create audit log middleware:**
   ```javascript
   app.post('/api/admin/mode/toggle', (req, res, next) => {
     const user = req.user;
     const oldMode = modeManager.getStatus().currentMode;
     
     // Continue with toggle
     // ...
     
     console.log(`[AUDIT] ${user.email} changed mode from ${oldMode} to ${newMode}`);
   });
   ```

3. **Monitor rate limiting:**
   - When in production, verify rate limiting works
   - When in development, verify relaxed limits

---

## 🐛 Common Integration Issues

### Issue 1: Component Not Rendering

**Symptom:** ModeSwitch component doesn't appear

**Solution:**
```jsx
// Check import path
import ModeSwitch from './components/ModeSwitch'; // Correct
// import ModeSwitch from './ModeSwitch'; // Wrong if in different folder

// Verify component file exists
// application/Frontend/src/components/ModeSwitch.jsx

// Check for console errors (F12)
```

### Issue 2: API Calls Failing with 401

**Symptom:** "Unauthorized" errors in console

**Solution:**
```javascript
// Check JWT token
console.log(localStorage.getItem('authToken'));

// If empty, user needs to login first
// If expired, user needs new token

// Verify token in browser DevTools:
// F12 → Application → Local Storage → authToken
```

### Issue 3: CSS Not Applying

**Symptom:** Component appears but styling is wrong

**Solution:**
```javascript
// Component has inline styles - they should work
// If not, check for CSS conflicts:

// 1. Check if other CSS overrides styles
// 2. Use CSS specificity: .mode-switch-container { ... }
// 3. Use !important if needed: background: cyan !important;
```

### Issue 4: Mode Not Changing

**Symptom:** Clicking buttons doesn't change mode

**Solution:**
```javascript
// Check backend is running
netstat -ano | Select-String "3000"

// Check JWT token is valid
curl -H "Authorization: Bearer $token" http://localhost:3000/api/health

// Check logs for errors
// Verify .env.mode file permissions

// Try direct API call
curl -X POST \
  -H "Authorization: Bearer $token" \
  http://localhost:3000/api/admin/mode/toggle
```

---

## 📚 Related Documentation

- **Full Mode Manager Doc:** `MODE_MANAGER_README.md`
- **Quick Start Guide:** `MODE_MANAGER_QUICKSTART.md`
- **System Summary:** `MODE_MANAGER_SUMMARY.md`
- **API Reference:** See MODE_MANAGER_README.md
- **Component Code:** `application/Frontend/src/components/ModeSwitch.jsx`
- **Backend Code:** `application/Backend/modeManager.js` + `backendserver.js`

---

**Last Updated:** November 29, 2024
**Version:** 1.0.0
**Status:** Integration Ready ✓
