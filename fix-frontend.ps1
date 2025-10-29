param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,
    [Parameter(Mandatory=$true)]
    [string]$KeyPath
)

ssh -i $KeyPath ubuntu@$ServerIP @"
# Create working app.js with all functions
cat > /home/ubuntu/r3aler-ai/application/Backend/static/js/app.js << 'EOF'
// Matrix Rain Animation
class MatrixRain {
    constructor() {
        this.canvas = document.getElementById('matrix-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#\$%^&*()';
        this.drops = [];
        this.init();
    }
    
    init() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        const columns = this.canvas.width / 20;
        for (let i = 0; i < columns; i++) { 
            this.drops[i] = 1; 
        }
        this.animate();
    }
    
    animate() {
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.fillStyle = '#0f0';
        this.ctx.font = '15px monospace';
        
        for (let i = 0; i < this.drops.length; i++) {
            const text = this.chars[Math.floor(Math.random() * this.chars.length)];
            this.ctx.fillText(text, i * 20, this.drops[i] * 20);
            
            if (this.drops[i] * 20 > this.canvas.height && Math.random() > 0.975) {
                this.drops[i] = 0;
            }
            this.drops[i] += 0.8;
        }
        
        setTimeout(() => requestAnimationFrame(() => this.animate()), 30);
    }
}

// Main App Object
const app = {
    API_URL: "/api",
    token: null,
    elements: {},

    init() {
        console.log('App initializing...');
        this.elements = {
            loginView: document.getElementById("login-view"),
            registerView: document.getElementById("register-view"),
            mainView: document.getElementById("main-view"),
            usernameInput: document.getElementById("username"),
            passwordInput: document.getElementById("password"),
            chatMessages: document.getElementById("chat-messages"),
            messageInput: document.getElementById("message-input")
        };
        
        this.setupEventListeners();
        this.token = localStorage.getItem("authToken");
        
        if (this.token) {
            this.showMainView();
        } else {
            this.showLoginView();
        }
        
        console.log('App initialized');
    },

    setupEventListeners() {
        if (this.elements.messageInput) {
            this.elements.messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.sendMessage();
            });
        }
    },

    showLoginView() {
        console.log('Showing login view');
        this.elements.loginView.classList.remove("hidden");
        this.elements.mainView.classList.add("hidden");
        if (this.elements.registerView) this.elements.registerView.classList.add("hidden");
    },

    showRegisterView() {
        console.log('Showing register view');
        this.elements.loginView.classList.add("hidden");
        if (this.elements.registerView) this.elements.registerView.classList.remove("hidden");
    },

    showMainView() {
        console.log('Showing main view');
        this.elements.loginView.classList.add("hidden");
        this.elements.mainView.classList.remove("hidden");
        if (this.elements.registerView) this.elements.registerView.classList.add("hidden");
        this.addMessage("System", "R3ÆLƎR TƎCH™ Authorization complete. Welcome to R3ÆLƎR AI.");
        
        // Trigger AI face animation
        setTimeout(() => {
            if (typeof onLoginSuccess === 'function') {
                onLoginSuccess();
            }
        }, 1000);
    },

    addMessage(sender, message) {
        if (this.elements.chatMessages) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message';
            messageDiv.innerHTML = \`<span class="sender">[\${sender}]:</span> \${message}\`;
            this.elements.chatMessages.appendChild(messageDiv);
            this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
        }
    },

    async apiRequest(endpoint, options = {}) {
        try {
            console.log(\`Making API request to \${endpoint}\`);
            const headers = {
                "Content-Type": "application/json",
                ...options.headers
            };
            
            if (this.token) {
                headers.Authorization = \`Bearer \${this.token}\`;
            }
            
            const response = await fetch(\`\${this.API_URL}\${endpoint}\`, {
                ...options,
                headers
            });
            
            const data = await response.json();
            console.log(\`API response from \${endpoint}:\`, data);
            
            if (!response.ok) {
                throw new Error(data.message || data.error || "API request failed");
            }
            
            return data;
        } catch (error) {
            console.error(\`API Error for \${endpoint}:\`, error);
            this.addMessage("System", \`Error: \${error.message}\`);
            return null;
        }
    },

    async login() {
        console.log('Login attempt');
        const username = this.elements.usernameInput.value;
        const password = this.elements.passwordInput.value;
        
        if (!username || !password) {
            this.addMessage("System", "Please enter username and password");
            return;
        }
        
        const data = await this.apiRequest("/auth/login", {
            method: "POST",
            body: JSON.stringify({ username, password })
        });
        
        if (data && data.success) {
            this.token = data.token;
            localStorage.setItem("authToken", this.token);
            this.showMainView();
        }
    },

    async register() {
        console.log('Register attempt');
        const fullName = document.getElementById("full-name").value;
        const dateOfBirth = document.getElementById("date-of-birth").value;
        const email = document.getElementById("email").value;
        const username = document.getElementById("reg-username").value;
        const password = document.getElementById("reg-password").value;
        
        if (!fullName || !dateOfBirth || !email || !username || !password) {
            this.addMessage("System", "Please fill in all fields");
            return;
        }
        
        const data = await this.apiRequest("/auth/register", {
            method: "POST",
            body: JSON.stringify({
                full_name: fullName,
                date_of_birth: dateOfBirth,
                email: email,
                username: username,
                password: password
            })
        });
        
        if (data && data.success) {
            this.addMessage("System", \`Registration successful! Username: \${data.username}\`);
            setTimeout(() => this.showLoginView(), 2000);
        }
    },

    async sendMessage() {
        const message = this.elements.messageInput.value.trim();
        if (!message) return;

        this.addMessage("You", message);
        this.elements.messageInput.value = '';

        const data = await this.apiRequest('/chat', {
            method: 'POST',
            body: JSON.stringify({ message: message })
        });

        if (data && data.response) {
            this.addMessage("AI", data.response);
        }
    },

    logout() {
        this.token = null;
        localStorage.removeItem("authToken");
        this.showLoginView();
    }
};

// Initialize when DOM loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, starting app...');
    new MatrixRain();
    app.init();
});

// Make app globally available
window.app = app;
EOF

# Create matrix face script
cat > /home/ubuntu/r3aler-ai/application/Backend/static/js/matrix_face.js << 'EOF'
// Matrix AI Face Animation
class MatrixFace {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.zIndex = '1000';
        this.canvas.style.pointerEvents = 'none';
        document.body.appendChild(this.canvas);
        
        this.resize();
        this.mouseX = 0;
        this.mouseY = 0;
        this.faceVisible = false;
        
        window.addEventListener('resize', () => this.resize());
        document.addEventListener('mousemove', (e) => {
            this.mouseX = e.clientX;
            this.mouseY = e.clientY;
        });
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    showFace() {
        this.faceVisible = true;
        this.animate();
        setTimeout(() => {
            this.faceVisible = false;
            document.body.removeChild(this.canvas);
        }, 5000);
    }
    
    animate() {
        if (!this.faceVisible) return;
        
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw matrix rain
        this.ctx.fillStyle = '#00ff00';
        this.ctx.font = '12px monospace';
        for (let i = 0; i < 50; i++) {
            const x = Math.random() * this.canvas.width;
            const y = Math.random() * this.canvas.height;
            this.ctx.fillText(String.fromCharCode(0x30A0 + Math.random() * 96), x, y);
        }
        
        // Draw AI face
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        
        // Face outline
        this.ctx.strokeStyle = '#00ff00';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, 100, 0, Math.PI * 2);
        this.ctx.stroke();
        
        // Eyes that follow cursor
        const eyeOffset = 20;
        const eyeRadius = 8;
        
        // Calculate eye direction
        const dx = this.mouseX - centerX;
        const dy = this.mouseY - centerY;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const maxLook = 10;
        const lookX = distance > 0 ? (dx / distance) * Math.min(maxLook, distance / 10) : 0;
        const lookY = distance > 0 ? (dy / distance) * Math.min(maxLook, distance / 10) : 0;
        
        // Left eye
        this.ctx.fillStyle = '#00ff00';
        this.ctx.beginPath();
        this.ctx.arc(centerX - eyeOffset + lookX, centerY - 20 + lookY, eyeRadius, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Right eye
        this.ctx.beginPath();
        this.ctx.arc(centerX + eyeOffset + lookX, centerY - 20 + lookY, eyeRadius, 0, Math.PI * 2);
        this.ctx.fill();
        
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize on login success
function onLoginSuccess() {
    try {
        console.log('Login success - showing AI face');
        const matrixFace = new MatrixFace();
        setTimeout(() => matrixFace.showFace(), 1000);
    } catch (error) {
        console.error('Failed to initialize matrix face:', error);
    }
}
EOF

# Create basic CSS
mkdir -p /home/ubuntu/r3aler-ai/application/Backend/static/css
cat > /home/ubuntu/r3aler-ai/application/Backend/static/css/style.css << 'EOF'
body {
    margin: 0;
    padding: 0;
    background: #000;
    color: #0f0;
    font-family: 'Courier New', monospace;
    overflow-x: hidden;
}

#matrix-canvas {
    position: fixed;
    top: 0;
    left: 0;
    z-index: -1;
}

.container {
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    background: rgba(0, 0, 0, 0.8);
    border: 1px solid #0f0;
    border-radius: 10px;
}

h1, h2, h3 {
    text-align: center;
    text-shadow: 0 0 10px #0f0;
}

.form-section {
    margin: 20px 0;
}

input, button {
    background: #111;
    color: #0f0;
    border: 1px solid #0f0;
    padding: 10px;
    margin: 5px;
    font-family: inherit;
    border-radius: 3px;
}

input:focus {
    outline: none;
    box-shadow: 0 0 5px #0f0;
}

button {
    cursor: pointer;
    transition: all 0.3s;
}

button:hover {
    background: #0f0;
    color: #000;
    box-shadow: 0 0 10px #0f0;
}

.hidden {
    display: none;
}

#chat-messages {
    background: rgba(0, 20, 0, 0.8);
    border: 1px solid #0f0;
    border-radius: 5px;
    max-height: 300px;
    overflow-y: auto;
    padding: 10px;
    margin: 10px 0;
}

.message {
    margin: 5px 0;
    padding: 5px;
    border-left: 3px solid #0f0;
    padding-left: 10px;
}

.sender {
    font-weight: bold;
    color: #0a0;
}

#message-input {
    width: 70%;
}

.fading-out {
    opacity: 0;
    transition: opacity 1s;
}
EOF

sudo systemctl restart r3aler-ai
echo "Frontend fixed! All buttons should work now."
"@