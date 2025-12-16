# BitXtractor Integration with R3AL3R AI - Complete

## Status: ✅ FULLY INTEGRATED

Date: November 9, 2025

---

## Overview

BitXtractor is now fully integrated with the R3AL3R AI system, providing cryptocurrency wallet extraction and analysis capabilities through a RESTful API.

## Integration Components

### 1. Backend Service (`application/Backend/app.py`)

**Endpoints:**
- `POST /api/bitxtractor/start` - Start wallet extraction job
- `GET /api/bitxtractor/status/<job_id>` - Check job status and get logs
- `GET /api/bitxtractor/download/<job_id>` - Download extraction results

**Features:**
- Asynchronous job processing with threading
- JSON output format
- Real-time log streaming
- Support for multiple extraction modes (dry-run, pipeline, etc.)
- Automatic path conversion for WSL compatibility

### 2. Service Launcher (`start_bitxtractor_service.ps1`)

**Modes:**
- **Windows Mode** (default): Runs on Windows with base dependencies
  - Uses `.venv\Scripts\python.exe`
  - Installs: flask, flask-cors, base58, cryptography
  - Note: bsddb3 not available (optional feature)

- **WSL Mode** (`-WSL` flag): Runs in Ubuntu WSL2 with full support
  - Uses `python3` in WSL
  - Includes bsddb3 for Berkeley DB wallet.dat support
  - Auto-installs all dependencies in WSL

**Usage:**
```powershell
# Windows mode (basic features)
.\start_bitxtractor_service.ps1

# WSL mode (full features including bsddb3)
.\start_bitxtractor_service.ps1 -WSL

# Custom port
.\start_bitxtractor_service.ps1 -Port 3002
```

### 3. Wallet Extractor Tool (`Tools/tools/wallet_extractor.py`)

**Core Features:**
- Multiple extraction modes (dry-run, intelligent recovery, unencrypted-only)
- BIP38 password recovery
- BTCRecover integration
- Balance checking
- WIF format conversion
- JSON output mode for API integration

**Extraction Modes:**
- `--dry-run` - Analyze wallet structure without decryption
- `--unencrypted-only` - Extract unencrypted keys only
- `--intelligent-recovery` - Smart cascading workflow (tries all methods)
- `--ask-pass` - Interactive passphrase input
- `--btcrecover-*` - BTCRecover tool integration
- `--bip38-recover` - BIP38 encrypted key recovery

### 4. Integration Test (`test_bitxtractor_integration.py`)

**Test Coverage:**
- API availability check
- Job creation and submission
- Status polling
- Log retrieval
- Real wallet file processing

**Usage:**
```bash
# Basic test (dry-run)
python test_bitxtractor_integration.py

# Test with real wallet
python test_bitxtractor_integration.py --wallet path/to/wallet.dat
```

---

## Quick Start

### 1. Start the BitXtractor Service

```powershell
# Option A: Windows mode
.\start_bitxtractor_service.ps1

# Option B: WSL mode (recommended for full features)
.\start_bitxtractor_service.ps1 -WSL
```

### 2. Test the Integration

```powershell
# Run integration tests
python test_bitxtractor_integration.py
```

### 3. Use the API

```powershell
# Start a wallet extraction job
$body = @{
    wallet_path = "C:\path\to\wallet.dat"
    mode = "dry"
} | ConvertTo-Json

$result = Invoke-RestMethod -Method Post `
    -Uri "http://localhost:3002/api/bitxtractor/start" `
    -Body $body `
    -ContentType "application/json"

# Get job status
$jobId = $result.job_id
Invoke-RestMethod -Uri "http://localhost:3002/api/bitxtractor/status/$jobId"
```

---

## API Reference

### POST /api/bitxtractor/start

**Request Body:**
```json
{
  "wallet_path": "C:\\path\\to\\wallet.dat",
  "mode": "dry",
  "passphrase": "optional_passphrase",
  "iterations": 10000,
  "kdf": "pbkdf2",
  "pbkdf2_hash": "sha256",
  "cipher": "aes-256-cbc",
  "extra_args": "--check-balances --json"
}
```

**Response:**
```json
{
  "success": true,
  "job_id": "e7f9343042cd423b87a4bbde8f947fcc"
}
```

### GET /api/bitxtractor/status/<job_id>

**Response (Running):**
```json
{
  "success": true,
  "status": "running",
  "log": "...extraction logs..."
}
```

**Response (Completed):**
```json
{
  "success": true,
  "status": "completed",
  "log": "...full extraction logs...",
  "output_ready": true,
  "download_url": "/api/bitxtractor/download/e7f9343042cd423b87a4bbde8f947fcc"
}
```

**Response (Failed):**
```json
{
  "success": true,
  "status": "failed",
  "error": "Error message",
  "log": "...error logs..."
}
```

### GET /api/bitxtractor/download/<job_id>

Downloads the extraction results as JSON or log file.

---

## Architecture

```
R3AL3R AI System
├── application/Backend/app.py (Flask API - Port 3002)
│   ├── /api/bitxtractor/start     (Job submission)
│   ├── /api/bitxtractor/status    (Status polling)
│   └── /api/bitxtractor/download  (Result retrieval)
│
├── Tools/tools/wallet_extractor.py (Core extraction engine)
│   ├── Berkeley DB support (bsddb3)
│   ├── Cryptography (AES, PBKDF2)
│   ├── BIP38 recovery
│   └── BTCRecover integration
│
└── Job Management System
    ├── Threading (async job execution)
    ├── File-based logging
    └── JSON output capture
```

---

## Deployment

### Production Environment

**Option 1: Windows Server**
```powershell
# Install dependencies
pip install flask flask-cors base58 cryptography

# Start service
.\start_bitxtractor_service.ps1

# Set up as Windows Service (optional)
# Use NSSM or Windows Task Scheduler
```

**Option 2: WSL/Linux (Recommended)**
```bash
# Install dependencies
sudo apt install python3 python3-pip libdb-dev
pip3 install flask flask-cors base58 cryptography bsddb3

# Start service
cd application/Backend
export FLASK_RUN_PORT=3002
python3 app.py
```

**Option 3: Docker**
```bash
# Use BitXtractorDockerfile
cd Tools/tools/BitXtractorMain
docker build -f BitXtractorDockerfile -t r3aler-bitxtractor .
docker run -p 3002:3002 r3aler-bitxtractor
```

---

## Integration with Other R3AL3R Services

### Knowledge API (Port 5001)
BitXtractor can be integrated with the Knowledge API to store extraction results and build a forensic knowledge base.

### AI Core Worker (Port 5002)
The AI can trigger wallet extractions based on user commands and analyze results.

### Backend (Port 5000)
The main backend can proxy BitXtractor requests and provide authentication/authorization.

---

## Security Considerations

⚠️ **IMPORTANT SECURITY NOTES:**

1. **Authentication**: Current implementation does NOT include authentication. Add JWT or API key authentication before production deployment.

2. **Rate Limiting**: Implement rate limiting to prevent abuse:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["10 per minute"])
   ```

3. **File Access**: Validate and sanitize all file paths to prevent directory traversal attacks.

4. **Passphrase Handling**: Passphrases are written to temp files. Use secure memory handling or encrypted pipes.

5. **Result Storage**: Extraction results contain sensitive data. Implement:
   - Encrypted storage
   - Automatic cleanup after retrieval
   - Access logging

6. **Network Security**:
   - Use HTTPS in production
   - Bind to localhost only if not exposing externally
   - Configure firewall rules

---

## Testing Results

✅ **All tests passed:**
- API root endpoint responding (404 with help message)
- Job creation successful
- Job status polling functional
- Log retrieval working
- Dry-run extraction completed
- JSON output format correct

**Sample Test Output:**
```
============================================================
R3AL3R AI - BitXtractor Integration Test
============================================================

[TEST 1] Testing API root endpoint...
  Status: 404
  Response: {"error":"Missing endpoint..."...}

[TEST 2] Testing BitXtractor start (dry-run mode)...
  Status: 200
  Response: {
    "job_id": "e7f9343042cd423b87a4bbde8f947fcc",
    "success": true
  }

[TEST 3] Testing BitXtractor status...
  Status: 200
  Job Status: completed
  Log Preview: ...wallet extraction logs...

============================================================
Test Summary:
============================================================
✓ API Root: Responding
✓ BitXtractor Start: Job ID e7f9343042cd423b87a4bbde8f947fcc
✓ BitXtractor Status: completed

BitXtractor is integrated and functional!
```

---

## Troubleshooting

### Issue: "bsddb3 not installed"
**Solution:** Use WSL mode or install pre-compiled wheel on Windows
```powershell
.\start_bitxtractor_service.ps1 -WSL
```

### Issue: Port 3002 already in use
**Solution:** Kill existing process or use different port
```powershell
# Find process on port 3002
Get-NetTCPConnection -LocalPort 3002 | Select-Object OwningProcess
Stop-Process -Id <PID>

# Or use different port
.\start_bitxtractor_service.ps1 -Port 3003
```

### Issue: Wallet file not found
**Solution:** Use absolute paths and check WSL path conversion
```json
{
  "wallet_path": "C:\\Users\\user\\wallet.dat"  // Windows
  "wallet_path": "/mnt/c/Users/user/wallet.dat"  // WSL auto-converts
}
```

---

## Next Steps

### Recommended Enhancements:

1. **Authentication Layer**
   - Add JWT authentication
   - Implement API keys
   - Role-based access control

2. **Frontend Integration**
   - Create React component for BitXtractor UI
   - Real-time job progress updates via WebSocket
   - Download interface for results

3. **Knowledge Base Integration**
   - Store extraction results in PostgreSQL Storage Facility
   - Index by wallet address, timestamp, recovery method
   - Build forensic analysis reports

4. **AI Integration**
   - Natural language commands: "Extract keys from wallet.dat"
   - Automatic method selection based on wallet analysis
   - Pattern recognition for recovery strategy optimization

5. **Monitoring & Logging**
   - Prometheus metrics
   - ELK stack integration
   - Job performance analytics

---

## References

- **Backend Implementation**: `application/Backend/app.py` (lines 370-560)
- **Wallet Extractor**: `Tools/tools/wallet_extractor.py`
- **Documentation**: `docs/BITXTRACTOR_SETUP_GUIDE.md`
- **R&D Blueprints**: `R&D Blueprints/WALLET_EXTRACTOR_README.md`

---

## License & Legal

⚠️ **For authorized forensic use and testnet only!**

Unauthorized access to cryptocurrency wallets is illegal. This tool is provided for:
- Educational purposes
- Legitimate wallet recovery
- Authorized forensic investigations
- Testnet development

Users are responsible for compliance with local laws and regulations.

---

**R3AL3R AI © 2025 - Crypto Forensics & Security**
