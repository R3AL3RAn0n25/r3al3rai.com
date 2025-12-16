# BitXtractor Wallet Analyzer - Quick Start Guide

## 🚀 Quick Start

### 1. Start the BitXtractor Service

```bash
# Windows
start_bitxtractor_service.ps1

# Or manually
python application/Backend/app.py
```

The service will start on `http://localhost:3002`

---

## 📊 Analyze a Wallet File

### Method 1: Python

```python
import requests

response = requests.post(
    'http://localhost:3002/api/bitxtractor/analyze',
    json={'wallet_path': 'C:\\Users\\YourName\\wallet.dat'}
)

result = response.json()
if result['success']:
    print(f"Format: {result['analysis']['file_format']}")
    print(f"Encrypted: {result['analysis']['likely_encrypted']}")
    print(f"Entropy: {result['analysis']['entropy']['value']}")
```

### Method 2: cURL

```bash
curl -X POST http://localhost:3002/api/bitxtractor/analyze \
  -H "Content-Type: application/json" \
  -d "{\"wallet_path\": \"C:\\\\Users\\\\YourName\\\\wallet.dat\"}"
```

### Method 3: PowerShell

```powershell
$body = @{
    wallet_path = "C:\Users\YourName\wallet.dat"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "http://localhost:3002/api/bitxtractor/analyze" `
  -ContentType "application/json" `
  -Body $body
```

---

## 📖 Understanding Results

### Entropy Value
- **7.5-8.0** = Very likely encrypted
- **5.0-7.5** = Possibly encrypted or compressed
- **3.0-5.0** = Mixed content
- **0-3.0** = Likely plaintext

### File Formats Detected
- **Berkeley DB** → Bitcoin Core, Litecoin, Dogecoin
- **SQLite** → Electrum, modern wallets
- **ZIP/GZIP** → Compressed backups

### Confidence Levels
- **VERY LIKELY encrypted (high confidence)** → Score ≥ 6
- **LIKELY encrypted (moderate confidence)** → Score ≥ 4
- **POSSIBLY encrypted (low confidence)** → Score ≥ 2
- **UNLIKELY to be encrypted** → Score < 2

---

## 🧪 Run Tests

### Test the API Integration
```bash
python test_bitxtractor_analyzer.py
```

### Test the Analyzer Directly
```bash
python test_wallet_analyzer.py
```

---

## 📁 Example Response

```json
{
  "success": true,
  "analysis": {
    "file_format": "Berkeley DB (Bitcoin Core, Litecoin, etc.)",
    "file_size": 4096,
    "entropy": {
      "value": 7.96,
      "interpretation": "Very high entropy - likely encrypted"
    },
    "encryption_analysis": {
      "has_encryption_metadata": true,
      "possible_cipher": "Block cipher (likely AES)",
      "evidence": [
        "File size is multiple of 16 (AES block size)",
        "Valid PKCS padding detected (length: 16)"
      ]
    },
    "likely_encrypted": "VERY LIKELY encrypted (high confidence)"
  }
}
```

---

## ⚠️ Troubleshooting

### "Cannot connect to BitXtractor API"
**Solution:** Start the backend service
```bash
python application/Backend/app.py
```

### "wallet_path required"
**Solution:** Include wallet_path in request body
```json
{"wallet_path": "/path/to/wallet.dat"}
```

### "File not found"
**Solution:** 
- Check path is correct
- Use absolute path
- Windows paths auto-convert to WSL: `C:\` → `/mnt/c/`

---

## 📚 Full Documentation

See [BITXTRACTOR_ANALYZER_INTEGRATION.md](BITXTRACTOR_ANALYZER_INTEGRATION.md) for complete API documentation.

---

## 🔒 Security Notice

This tool is for **legitimate recovery purposes only**. Use responsibly and legally.

---

**Last Updated:** November 10, 2025
