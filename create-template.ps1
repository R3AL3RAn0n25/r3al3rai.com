param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,
    [Parameter(Mandatory=$true)]
    [string]$KeyPath
)

ssh -i $KeyPath ubuntu@$ServerIP @"
# Check if template exists
ls -la /opt/r3aler-ai/application/Frontend/templates/

# Create template directory and copy
mkdir -p /opt/r3aler-ai/application/Backend/templates
mkdir -p /opt/r3aler-ai/application/Backend/static

# Copy from Frontend to Backend
cp -r /opt/r3aler-ai/application/Frontend/templates/* /opt/r3aler-ai/application/Backend/templates/ 2>/dev/null || echo "No templates to copy"
cp -r /opt/r3aler-ai/application/Frontend/static/* /opt/r3aler-ai/application/Backend/static/ 2>/dev/null || echo "No static files to copy"

# If still missing, create basic template
if [ ! -f /opt/r3aler-ai/application/Backend/templates/index.html ]; then
cat > /opt/r3aler-ai/application/Backend/templates/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>R3ÆLƎR AI</title>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; }
        .container { max-width: 800px; margin: 50px auto; padding: 20px; }
        input, button { background: #111; color: #0f0; border: 1px solid #0f0; padding: 10px; margin: 5px; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <canvas id="matrix-canvas" style="position:fixed;top:0;left:0;z-index:-1;"></canvas>
    <div class="container">
        <h1>R3ÆLƎR AI</h1>
        <div id="login-view">
            <h2>System Access</h2>
            <input type="text" id="username" placeholder="Username">
            <input type="password" id="password" placeholder="Password">
            <button onclick="login()">Login</button>
            <button onclick="showRegister()">Register</button>
        </div>
        <div id="register-view" class="hidden">
            <h2>Register</h2>
            <input type="text" id="full-name" placeholder="Full Name">
            <input type="date" id="date-of-birth">
            <input type="email" id="email" placeholder="Email">
            <input type="text" id="reg-username" placeholder="Username">
            <input type="password" id="reg-password" placeholder="Password">
            <button onclick="register()">Register</button>
            <button onclick="showLogin()">Back</button>
        </div>
        <div id="main-view" class="hidden">
            <h2>AI Terminal</h2>
            <div id="chat-messages" style="height:300px;overflow-y:auto;border:1px solid #0f0;padding:10px;margin:10px 0;"></div>
            <input type="text" id="message-input" placeholder="Type message..." style="width:70%;">
            <button onclick="sendMessage()">Send</button>
            <button onclick="logout()">Logout</button>
        </div>
    </div>
    <script>
        // Matrix rain
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        const drops = [];
        for(let i = 0; i < canvas.width/20; i++) drops[i] = 1;
        
        function draw() {
            ctx.fillStyle = 'rgba(0,0,0,0.05)';
            ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#0f0';
            ctx.font = '15px monospace';
            for(let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random()*chars.length)];
                ctx.fillText(text, i*20, drops[i]*20);
                if(drops[i]*20 > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(draw, 33);
        
        // App functions
        let token = localStorage.getItem('token');
        if(token) showMain();
        
        function showLogin() {
            document.getElementById('login-view').classList.remove('hidden');
            document.getElementById('register-view').classList.add('hidden');
            document.getElementById('main-view').classList.add('hidden');
        }
        
        function showRegister() {
            document.getElementById('login-view').classList.add('hidden');
            document.getElementById('register-view').classList.remove('hidden');
        }
        
        function showMain() {
            document.getElementById('login-view').classList.add('hidden');
            document.getElementById('register-view').classList.add('hidden');
            document.getElementById('main-view').classList.remove('hidden');
        }
        
        async function login() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password})
            });
            
            const data = await response.json();
            if(data.success) {
                localStorage.setItem('token', data.token);
                showMain();
            } else {
                alert(data.error);
            }
        }
        
        async function register() {
            const data = {
                full_name: document.getElementById('full-name').value,
                date_of_birth: document.getElementById('date-of-birth').value,
                email: document.getElementById('email').value,
                username: document.getElementById('reg-username').value,
                password: document.getElementById('reg-password').value
            };
            
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            if(result.success) {
                alert('Registration successful!');
                showLogin();
            } else {
                alert(result.error);
            }
        }
        
        async function sendMessage() {
            const message = document.getElementById('message-input').value;
            if(!message) return;
            
            addMessage('You', message);
            document.getElementById('message-input').value = '';
            
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message})
            });
            
            const data = await response.json();
            addMessage('AI', data.response || data.error);
        }
        
        function addMessage(sender, message) {
            const div = document.createElement('div');
            div.innerHTML = '<strong>' + sender + ':</strong> ' + message;
            document.getElementById('chat-messages').appendChild(div);
            document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
        }
        
        function logout() {
            localStorage.removeItem('token');
            showLogin();
        }
        
        document.getElementById('message-input').addEventListener('keypress', function(e) {
            if(e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
EOF
fi

sudo systemctl restart r3aler-ai
echo "Template created and service restarted!"
"@