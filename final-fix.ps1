param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,
    [Parameter(Mandatory=$true)]
    [string]$KeyPath
)

ssh -i $KeyPath ubuntu@$ServerIP @"
sudo mkdir -p /opt/r3aler-ai/application/Backend/templates

cat > /tmp/index.html << 'EOF'
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
            <input type="text" id="username" placeholder="Username">
            <input type="password" id="password" placeholder="Password">
            <button onclick="login()">Login</button>
        </div>
        <div id="main-view" class="hidden">
            <div id="chat-messages" style="height:300px;overflow-y:auto;border:1px solid #0f0;padding:10px;"></div>
            <input type="text" id="message-input" placeholder="Message..." style="width:70%">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script>
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
        
        async function login() {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    username: document.getElementById('username').value,
                    password: document.getElementById('password').value
                })
            });
            const data = await response.json();
            if(data.success) {
                document.getElementById('login-view').classList.add('hidden');
                document.getElementById('main-view').classList.remove('hidden');
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
    </script>
</body>
</html>
EOF

sudo cp /tmp/index.html /opt/r3aler-ai/application/Backend/templates/
sudo systemctl restart r3aler-ai
echo "Fixed! Try http://3.144.216.245"
"@