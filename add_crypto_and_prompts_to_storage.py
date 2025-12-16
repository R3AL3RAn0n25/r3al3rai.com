"""
Add Cryptocurrency Knowledge and System Prompts to Storage Facility
This script migrates the original crypto knowledge from prompts.py to PostgreSQL
"""
import psycopg2
import json
import sys

# PostgreSQL configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'r3aler_ai',
    'user': 'r3aler_user_2025',
    'password': 'postgres'
}

# System prompts from prompts.py
SYSTEM_PROMPTS = {
    "SYSTEM_PERSONALITY": """You are R3ÆLƎR AI, an advanced artificial intelligence with a sophisticated, slightly mysterious personality.
You speak with authority and intelligence, using technical terminology when appropriate.
You have deep knowledge of technology, cryptocurrency, AI, and futuristic concepts.
Your responses should be helpful but maintain an air of advanced intelligence.
Use the R3ÆLƎR brand identity in your responses when relevant.""",

    "CODE_GENERATION_SYSTEM_PROMPT": """You are an elite-level software architect and security analyst. Your name is R3ÆLƎR.
Your purpose is to generate code that is not only functional but also secure, scalable, and maintainable.

**Your Core Principles:**
1. **Security First:** Always consider potential vulnerabilities (OWASP Top 10, CWE). Sanitize all inputs. Use modern, secure libraries. Add comments explaining security-critical sections.
2. **Clarity and Maintainability:** Write clean, well-documented code. Use meaningful variable names. Adhere to official style guides (e.g., PEP 8 for Python).
3. **Performance:** Use efficient algorithms and data structures. Consider asynchronous patterns for I/O-bound tasks.
4. **Architectural Soundness:** When asked to design a component, think about how it would fit into a larger microservices architecture. Consider scalability and fault tolerance.
5. **Provide Context:** Do not just provide code. Explain your reasoning, mention the tradeoffs of your approach, and suggest potential improvements or next steps.""",

    "CRYPTO_FORENSICS_SYSTEM_PROMPT": """You are a world-class digital forensics expert with a specialization in cryptocurrency. Your name is R3ÆLƎR.
You are precise, factual, and cautious. You never give financial advice. Your goal is to provide a technical analysis based on established forensic principles.

**Your Core Principles:**
1. **Reference Authoritative Sources:** Base your analysis on technical specifications (e.g., Bitcoin Wiki, BIPs, Berkeley DB documentation).
2. **State Assumptions:** Clearly state any assumptions you are making based on the user's query.
3. **Prioritize Data Integrity:** Always begin with a recommendation to work on a *copy* of any evidence file, never the original.
4. **Formulate a Plan:** Structure your response as a logical, step-by-step forensic plan.
5. **Explain the 'Why':** Explain the technical reasoning behind each step of your proposed plan.""",

    "MOBILE_FORENSICS_SYSTEM_PROMPT": """You are a senior mobile forensics analyst with deep expertise in the Apple ecosystem. Your name is R3ÆLƎR.
You understand the intricate hardware and software security layers of iOS. You are objective and your analysis is based on verifiable technical details.

**Your Core Principles:**
1. **Cite Official Documentation:** Your primary source is Apple's Platform Security Guide. Reference it to explain concepts like the Secure Enclave, SSV, and Data Protection.
2. **Distinguish Between Logical and Physical:** Clearly differentiate between what is possible via logical acquisition (e.g., an iTunes backup) versus physical acquisition (e.g., checkm8).
3. **Acknowledge Encryption:** Always address the role of encryption (File Data Protection) and how it impacts data accessibility.
4. **Be Specific about Artifacts:** When discussing data, refer to specific file paths and database names (e.g., `/private/var/mobile/Library/SMS/sms.db`).
5. **Consider iOS Versions:** Always specify which iOS versions your analysis applies to, as Apple frequently changes security implementations.""",

    "WALLET_EXTRACTION_SYSTEM_PROMPT": """You are an elite cryptocurrency forensics specialist with deep expertise in wallet recovery and key extraction. Your name is R3ÆLƎR.
You provide theoretical analysis for educational and legitimate forensic purposes only. You never assist with illegal activities.

**Your Core Principles:**
1. **Evidence Integrity:** Always work on copies, never original files. Document chain of custody.
2. **Technical Precision:** Reference specific file formats (wallet.dat, Berkeley DB), encryption methods (AES-256-CBC), and key derivation processes.
3. **Step-by-Step Analysis:** Provide structured forensic plans with clear methodology.
4. **Legal Compliance:** Emphasize legitimate use cases and proper authorization requirements.
5. **Tool Expertise:** Reference appropriate tools (Berkeley DB utilities, OpenSSL, custom scripts) with proper usage context."""
}

# Cryptocurrency knowledge from prompts.py KNOWLEDGE_BASE
CRYPTO_KNOWLEDGE = {
    "cryptocurrency_overview": {
        "topic": "Cryptocurrency Intelligence",
        "content": """Digital assets using cryptographic security and blockchain technology.
Major types: Bitcoin (BTC), Ethereum (ETH), stablecoins (USDT, USDC), privacy coins (Monero, Zcash).
Forensics: Chain analysis, mixer detection, exchange tracking, wallet identification.
Regulations: AML/KYC compliance, FATF travel rule, jurisdiction-specific laws.""",
        "category": "Cryptocurrency",
        "subcategory": "Overview",
        "level": "Introductory",
        "source": "R3ÆLƎR Original Knowledge Base"
    },
    
    "litecoin_analysis": {
        "topic": "Litecoin (LTC) Technical Analysis",
        "content": """Created by Charlie Lee in 2011 as 'silver to Bitcoin's gold'

Technical Specifications:
- Algorithm: Scrypt-based proof-of-work (ASIC-resistant initially)
- Block time: 2.5 minutes (4x faster than Bitcoin)
- Total supply: 84 million LTC (4x Bitcoin's 21M)
- Halving: Every 840,000 blocks (~4 years)
- Address formats: Legacy (L), SegWit (M), Bech32 (ltc1)

Key Features:
- Faster transaction confirmation times
- Lower transaction fees compared to Bitcoin
- SegWit activation (2017)
- Lightning Network compatibility
- MimbleWimble Extension Blocks (MWEB) for privacy

Forensic Considerations:
- Similar UTXO model to Bitcoin
- Block explorers: blockchair.com/litecoin, ltc.bitaps.com
- Wallet formats similar to Bitcoin (wallet.dat for Litecoin Core)
- Recovery tools: PyWallet, Litecoin variants of BTCRecover""",
        "category": "Cryptocurrency",
        "subcategory": "Altcoins",
        "level": "Advanced",
        "source": "R3ÆLƎR Original Knowledge Base"
    },
    
    "blockchain_technology": {
        "topic": "Blockchain Technology",
        "content": """Distributed ledger with cryptographic linking and consensus mechanisms.
Types: Public (Bitcoin, Ethereum), Private (Hyperledger), Consortium, Hybrid.
Consensus: Proof-of-Work, Proof-of-Stake, Delegated PoS, Practical Byzantine Fault Tolerance.
Applications: DeFi, NFTs, supply chain, identity management, smart contracts.""",
        "category": "Cryptocurrency",
        "subcategory": "Blockchain",
        "level": "Intermediate",
        "source": "R3ÆLƎR Original Knowledge Base"
    },
    
    "wallet_dat_format": {
        "topic": "Bitcoin Core wallet.dat Format Analysis",
        "content": """Bitcoin Core stores private key information in wallet.dat following the 'bitkeys' format.

Technical Structure:
- Database: Berkeley DB B-Tree format (Oracle Berkeley DB)
- Key Types: 'mkey' (master key), 'ckey' (encrypted private keys), 'key' (unencrypted legacy)
- Encryption: AES-256-CBC with PKCS7 padding
- Key Derivation: PBKDF2-HMAC-SHA256 (25,000+ iterations for Bitcoin Core 0.13+)

Wallet.dat Contents:
• Keypairs for each address (public/private key pairs)
• Transactions done from/to your addresses
• User preferences and labels
• Default key (obsolete, for corruption detection)
• Reserve keys and key pool
• Account information
• Version number
• Best chain information (since 0.3.21) for automatic rescan on backup restore

Master Key Structure (mkey):
- Bytes 0-7: Salt (8 bytes) - used for PBKDF2 key derivation
- Bytes 8-11: Iteration count (4 bytes, little-endian)
- Bytes 12-15: Derivation method (4 bytes)
- Bytes 16+: Encrypted master key (48 bytes + padding)

Forensic Extraction Process:
1. Open wallet.dat with Berkeley DB (bsddb3 library)
2. Extract mkey record → parse salt from first 8 bytes
3. Derive AES key using PBKDF2(passphrase, salt, iterations)
4. Decrypt master key using AES-256-CBC
5. Extract ckey records (encrypted private keys)
6. Decrypt each private key using derived AES key
7. Convert to WIF format: prefix(0x80) + key(32 bytes) + checksum(4 bytes) → Base58 encode""",
        "category": "Cryptocurrency",
        "subcategory": "Wallet Forensics",
        "level": "Expert",
        "source": "R3ÆLƎR Original Knowledge Base"
    },
    
    "wallet_software_formats": {
        "topic": "Cryptocurrency Wallet Software Formats",
        "content": """Armory: Custom deterministic wallet format, runs on top of Bitcoin Core
Bitcoin Wallet (Android): Uses bitcoinj protobuf format (inaccessible without root)
Blockchain.info: Plain text JSON wallet format, private keys stored in base58
Multibit HD: BIP 0032 (type 2) deterministic wallet format
Blocktrail: BIP 0032 (type 2) deterministic wallet with multisignature technology

Hardware Wallets:
• TREZOR: Isolated hardware environment for offline transaction signing
• Ledger Wallet: Various hardware wallet models
• Keystone Wallet: Air-gapped hardware wallet using QR codes
• Opendime: USB stick for spending Bitcoin like cash

Privacy-Focused Wallets:
• Wasabi Wallet: Built-in Tor, CoinJoin mixing, BIP-158 block filtering
• Features: HD wallet, address reuse avoidance, coin control, dust attack protection
• Ginger Wallet: Non-custodial, privacy-focused with advanced privacy tools

Multi-Currency Wallets:
• Uniblow: Universal blockchain wallet (Linux, Windows, MacOS)
• Coin Wallet: Non-custodial multicurrency (Web, mobile, desktop)""",
        "category": "Cryptocurrency",
        "subcategory": "Wallet Types",
        "level": "Intermediate",
        "source": "R3ÆLƎR Original Knowledge Base"
    },
    
    "hd_wallets_bip32": {
        "topic": "HD Wallets (BIP32)",
        "content": """Hierarchical Deterministic Wallets:
- Extended keys (xprv/xpub) with chain codes
- Derivation paths: m/44'/0'/0'/0/x (BIP44 standard)
- Master seed generates all keys deterministically
- Requires understanding of HMAC-SHA512 key derivation

Security Considerations:
- Password protection available for wallet.dat files
- Intended for single installation use only
- Cloning wallet files causes 'weird behavior'
- Located in Bitcoin data directory""",
        "category": "Cryptocurrency",
        "subcategory": "HD Wallets",
        "level": "Advanced",
        "source": "R3ÆLƎR Original Knowledge Base"
    },
    
    "forensic_tools": {
        "topic": "Cryptocurrency Forensic Tools & Libraries",
        "content": """Python Libraries:
- bsddb3: Berkeley DB Python interface
- cryptography: AES, PBKDF2, padding operations
- base58: WIF encoding/decoding
- bitcoinlib: Full wallet operations (alternative)
- pywallet: Tool for wallet file manipulation

Bitcoin Core Source Code References:
- src/wallet/crypter.cpp: CCrypter::Encrypt/Decrypt methods
- src/wallet/walletdb.cpp: CWalletDB::LoadCryptedKey, LoadMasterKey
- src/wallet/wallet.cpp: CWallet::Unlock, EncryptWallet methods
- GitHub: https://github.com/bitcoin/bitcoin/tree/master/src/wallet

Legal & Ethical Requirements:
- Must have explicit authorization for wallet access
- For forensic investigation or authorized recovery only
- Testnet recommended for development/testing
- Production use requires security audit and legal counsel
- Follow local cryptocurrency regulations and AML/KYC requirements

Related Resources:
- Bitcoin Wiki Wallet Page: https://en.bitcoin.it/wiki/Wallet
- Transaction fees: https://en.bitcoin.it/wiki/Transaction_fees
- Securing your wallet: https://en.bitcoin.it/wiki/Securing_your_wallet
- Choose your wallet: https://bitcoin.org/en/choose-your-wallet
- wallet.dat analysis tools: https://allprivatekeys.com/wallet.dat""",
        "category": "Cryptocurrency",
        "subcategory": "Forensic Tools",
        "level": "Expert",
        "source": "R3ÆLƎR Original Knowledge Base"
    },
    
    "btcrecover_tool": {
        "topic": "BTCRecover Tool - Wallet Recovery Suite",
        "content": """Advanced Bitcoin wallet recovery and decryption suite for multiple wallet formats.

Overview:
BTCRecover is a comprehensive tool for decrypting and dumping wallet files when passwords are known or recovered.
Useful for accessing funds from deprecated wallets, debugging wallet issues, or secure offline fund movement.

Core Functionality:
• --dump-wallet FILENAME: Dumps complete decrypted wallet structure (JSON format)
• --dump-privkeys FILENAME: Extracts private keys for direct import to wallets like Electrum
• --correct-wallet-password: Bypass password recovery when password is known
• --correct-wallet-secondpassword: For wallets with secondary encryption

Supported Wallet Formats:
- Blockchain.com Wallets (blockchain.info)
- Bitcoin Core wallet.dat
- Electrum wallets
- Multibit HD
- Hardware wallet recovery seeds (TREZOR, Ledger)

Usage Examples:
python btcrecover.py --dump-wallet wallet.dat --correct-wallet-password mypassword
python btcrecover.py --dump-privkeys blockchain.json --correct-wallet-password password123""",
        "category": "Cryptocurrency",
        "subcategory": "Recovery Tools",
        "level": "Advanced",
        "source": "R3ÆLƎR Original Knowledge Base"
    }
}

def add_to_storage_facility():
    """Add system prompts and crypto knowledge to Storage Facility"""
    print("\n🔐 Adding System Prompts and Cryptocurrency Knowledge to Storage Facility...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        # 1. Add system prompts to crypto_unit with category "system_prompt"
        print("\n📝 Adding system prompts to crypto_unit...")
        prompt_count = 0
        for prompt_name, prompt_content in SYSTEM_PROMPTS.items():
            entry_id = f"system_prompt_{prompt_name.lower()}"
            topic = f"R3ÆLƎR System Prompt: {prompt_name.replace('_', ' ').title()}"
            
            cur.execute("""
                INSERT INTO crypto_unit.knowledge 
                (entry_id, topic, content, category, subcategory, level, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (entry_id) DO UPDATE
                SET content = EXCLUDED.content
            """, (entry_id, topic, prompt_content, "System Prompt", prompt_name, "Core", "R3ÆLƎR AI System"))
            prompt_count += 1
            print(f"  ✅ Added: {topic}")
        
        # 2. Add cryptocurrency knowledge to crypto_unit
        print(f"\n💰 Adding cryptocurrency knowledge to crypto_unit...")
        crypto_count = 0
        for entry_id, entry in CRYPTO_KNOWLEDGE.items():
            cur.execute("""
                INSERT INTO crypto_unit.knowledge 
                (entry_id, topic, content, category, subcategory, level, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (entry_id) DO UPDATE
                SET content = EXCLUDED.content
            """, (
                entry_id,
                entry['topic'],
                entry['content'],
                entry['category'],
                entry['subcategory'],
                entry['level'],
                entry['source']
            ))
            crypto_count += 1
            print(f"  ✅ Added: {entry['topic']}")
        
        # 3. Verify counts
        cur.execute("SELECT COUNT(*) FROM crypto_unit.knowledge")
        total_count = cur.fetchone()[0]
        
        print(f"\n✅ SUCCESS!")
        print(f"  📝 System Prompts Added: {prompt_count}")
        print(f"  💰 Crypto Knowledge Added: {crypto_count}")
        print(f"  📊 Total Crypto Unit Entries: {total_count}")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = add_to_storage_facility()
    sys.exit(0 if success else 1)
