# Security Notice

⚠️ **IMPORTANT: Action Required** ⚠️

1. Credential Rotation Required
   - Previous credentials and secrets have been compromised
   - ALL credentials must be rotated immediately
   - Generate new secure values for all secrets

2. Required Actions:
   - Generate new JWT secret
   - Update database passwords
   - Rotate admin credentials
   - Generate new API keys
   - Update SSL/TLS certificates

3. Environment Setup:
   ```bash
   # 1. Copy example environment file
   cp .env.example .env

   # 2. Generate new JWT secret
   node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

   # 3. Generate secure secret key
   python -c "import secrets; print(secrets.token_hex(32))"
   
   # 4. Update .env with secure values
   # DO NOT commit .env file!
   ```

4. For Production:
   - Use different credentials for each environment
   - Enable rate limiting
   - Set up monitoring
   - Use SSL/TLS
   - Regular security audits

5. Git Security:
   - Repository history contains sensitive data
   - Force push after cleaning history with:
     ```bash
     # Back up repo first!
     cp -r . ../backup-repo
     
     # Install git-filter-repo
     pip install git-filter-repo
     
     # Clean history (adjust paths as needed)
     git filter-repo --replace-text filter-repo-rules.txt
     
     # Force push changes
     git push origin --force
     ```
   - All team members must clone fresh copy after cleanup

6. Ongoing Security:
   - Monitor for unauthorized access
   - Regular credential rotation
   - Keep dependencies updated
   - Follow security best practices

For security issues, contact: [security contact info]