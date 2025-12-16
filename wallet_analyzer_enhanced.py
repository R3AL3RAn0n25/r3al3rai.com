#!/usr/bin/env python3
"""
Enhanced Wallet.dat Analysis Tool
Analyzes cryptocurrency wallet files to detect encryption and file format.
This tool is for educational and legitimate recovery purposes only.
"""

import os
import math
import struct
from collections import Counter
from typing import Dict, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class WalletAnalyzer:
    """Enhanced wallet file analyzer with improved detection methods."""
    
    # Known magic bytes for various wallet formats
    MAGIC_BYTES = {
        b'\x00\x06\x15\x61': 'Berkeley DB (Bitcoin Core, Litecoin, etc.)',
        b'\x62\x31\x05\x00': 'Berkeley DB (v1)',
        b'SQLite format 3': 'SQLite Database (Electrum, some modern wallets)',
        b'{\x00\x00\x00': 'JSON-based wallet (possible)',
        b'PK\x03\x04': 'ZIP Archive (possible backup)',
        b'\x1f\x8b\x08': 'GZIP compressed file',
    }
    
    # Entropy thresholds (based on statistical analysis)
    ENTROPY_HIGH = 7.5      # Likely encrypted or compressed
    ENTROPY_MODERATE = 5.0   # Mixed content
    ENTROPY_LOW = 3.0       # Likely plaintext
    
    def __init__(self, wallet_path: str):
        """Initialize analyzer with wallet file path."""
        self.wallet_path = wallet_path
        self.file_data = None
        self.file_size = 0
        
    def read_file(self) -> bool:
        """Read and validate wallet file."""
        if not os.path.exists(self.wallet_path):
            logger.error(f"File not found: {self.wallet_path}")
            return False
            
        if not os.path.isfile(self.wallet_path):
            logger.error(f"Path is not a file: {self.wallet_path}")
            return False
            
        try:
            with open(self.wallet_path, 'rb') as f:
                self.file_data = f.read()
                self.file_size = len(self.file_data)
            logger.info(f"Successfully read {self.file_size} bytes")
            return True
        except PermissionError:
            logger.error(f"Permission denied: {self.wallet_path}")
            return False
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return False
    
    def detect_file_format(self) -> Optional[str]:
        """Detect file format using magic bytes."""
        if not self.file_data:
            return None
            
        # Check against known magic bytes
        for magic, description in self.MAGIC_BYTES.items():
            if self.file_data.startswith(magic):
                return description
        
        # Additional heuristics for Berkeley DB
        if len(self.file_data) >= 512:
            # BDB has page size at offset 20-21 (big-endian)
            try:
                page_size = struct.unpack('>H', self.file_data[20:22])[0]
                if page_size in [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]:
                    return f"Possible Berkeley DB (page size: {page_size})"
            except:
                pass
        
        return "Unknown format"
    
    def calculate_entropy(self) -> float:
        """Calculate Shannon entropy efficiently using Counter."""
        if not self.file_data or self.file_size == 0:
            return 0.0
        
        # Use Counter for O(n) performance instead of O(n²)
        byte_counts = Counter(self.file_data)
        entropy = 0.0
        
        for count in byte_counts.values():
            probability = count / self.file_size
            entropy -= probability * math.log2(probability)
        
        return entropy
    
    def analyze_byte_distribution(self) -> Dict[str, float]:
        """Analyze byte value distribution patterns."""
        if not self.file_data:
            return {}
        
        byte_counts = Counter(self.file_data)
        
        # Calculate various distribution metrics
        zero_count = byte_counts.get(0, 0)
        printable_count = sum(byte_counts.get(i, 0) for i in range(32, 127))
        high_byte_count = sum(byte_counts.get(i, 0) for i in range(128, 256))
        
        return {
            'zero_byte_ratio': zero_count / self.file_size,
            'printable_ratio': printable_count / self.file_size,
            'high_byte_ratio': high_byte_count / self.file_size,
            'unique_bytes': len(byte_counts)
        }
    
    def chi_square_test(self) -> Tuple[float, str]:
        """
        Perform chi-square test for randomness.
        Random/encrypted data should have uniform distribution.
        """
        if not self.file_data or self.file_size < 256:
            return 0.0, "Insufficient data"
        
        byte_counts = Counter(self.file_data)
        expected_freq = self.file_size / 256
        
        chi_square = 0.0
        for i in range(256):
            observed = byte_counts.get(i, 0)
            chi_square += ((observed - expected_freq) ** 2) / expected_freq
        
        # Interpret results (simplified)
        # For truly random data, chi-square should be around 255
        # Higher values indicate non-uniform distribution
        if chi_square < 200:
            interpretation = "Highly uniform (likely encrypted/random)"
        elif chi_square < 400:
            interpretation = "Moderately uniform (possibly encrypted)"
        elif chi_square < 1000:
            interpretation = "Non-uniform (possibly compressed or structured)"
        else:
            interpretation = "Highly non-uniform (likely plaintext or corrupted)"
        
        return chi_square, interpretation
    
    def detect_encryption_indicators(self) -> Dict[str, any]:
        """Look for legitimate encryption indicators in headers/metadata."""
        indicators = {
            'has_encryption_metadata': False,
            'possible_cipher': 'Unknown',
            'evidence': []
        }
        
        if not self.file_data:
            return indicators
        
        # Search in first 4KB for metadata (not plaintext algorithm names)
        header = self.file_data[:4096]
        
        # Look for actual encryption metadata patterns
        # AES uses 16-byte blocks, look for block padding patterns
        if len(self.file_data) % 16 == 0 and self.file_size > 1024:
            indicators['evidence'].append("File size is multiple of 16 (AES block size)")
        
        # Check for PKCS#5/PKCS#7 padding (last byte indicates padding length)
        if self.file_size >= 16:
            last_byte = self.file_data[-1]
            if 1 <= last_byte <= 16:
                # Verify padding pattern
                padding_valid = all(b == last_byte for b in self.file_data[-last_byte:])
                if padding_valid:
                    indicators['evidence'].append(f"Valid PKCS padding detected (length: {last_byte})")
                    indicators['possible_cipher'] = "Block cipher (likely AES)"
        
        # Look for key derivation metadata (not plaintext "salt")
        # Real encrypted wallets often have structured headers
        if b'\x00\x00\x00' in header[:100]:
            indicators['evidence'].append("Structured header detected")
        
        if indicators['evidence']:
            indicators['has_encryption_metadata'] = True
        
        return indicators
    
    def analyze(self) -> Dict[str, any]:
        """Perform comprehensive wallet analysis."""
        if not self.read_file():
            return {'error': 'Failed to read file'}
        
        logger.info("Starting comprehensive analysis...")
        
        # Gather all analysis results
        analysis = {
            'file_path': self.wallet_path,
            'file_size': self.file_size,
            'file_format': self.detect_file_format(),
        }
        
        # Entropy analysis
        entropy = self.calculate_entropy()
        analysis['entropy'] = {
            'value': round(entropy, 4),
            'max_possible': 8.0,
            'interpretation': self._interpret_entropy(entropy)
        }
        
        # Byte distribution
        distribution = self.analyze_byte_distribution()
        analysis['byte_distribution'] = {
            'zero_bytes': f"{distribution['zero_byte_ratio']:.2%}",
            'printable_chars': f"{distribution['printable_ratio']:.2%}",
            'high_bytes': f"{distribution['high_byte_ratio']:.2%}",
            'unique_byte_values': distribution['unique_bytes']
        }
        
        # Chi-square randomness test
        chi_sq, chi_interp = self.chi_square_test()
        analysis['randomness_test'] = {
            'chi_square_value': round(chi_sq, 2),
            'interpretation': chi_interp
        }
        
        # Encryption detection
        analysis['encryption_analysis'] = self.detect_encryption_indicators()
        
        # Overall assessment
        analysis['likely_encrypted'] = self._assess_encryption(entropy, chi_sq, distribution)
        
        return analysis
    
    def _interpret_entropy(self, entropy: float) -> str:
        """Interpret entropy value."""
        if entropy >= self.ENTROPY_HIGH:
            return "Very high entropy - likely encrypted or compressed"
        elif entropy >= self.ENTROPY_MODERATE:
            return "Moderate entropy - mixed or structured data"
        elif entropy >= self.ENTROPY_LOW:
            return "Low entropy - likely plaintext or repetitive data"
        else:
            return "Very low entropy - highly repetitive or corrupted"
    
    def _assess_encryption(self, entropy: float, chi_sq: float, distribution: Dict) -> str:
        """Provide overall encryption assessment."""
        confidence_score = 0
        
        # High entropy indicates encryption
        if entropy >= self.ENTROPY_HIGH:
            confidence_score += 3
        elif entropy >= 6.5:
            confidence_score += 2
        
        # Uniform distribution indicates encryption
        if chi_sq < 300:
            confidence_score += 2
        elif chi_sq < 500:
            confidence_score += 1
        
        # Low printable ratio indicates binary/encrypted
        if distribution['printable_ratio'] < 0.3:
            confidence_score += 1
        
        # Uniform byte usage
        if distribution['unique_bytes'] >= 240:
            confidence_score += 1
        
        if confidence_score >= 6:
            return "VERY LIKELY encrypted (high confidence)"
        elif confidence_score >= 4:
            return "LIKELY encrypted (moderate confidence)"
        elif confidence_score >= 2:
            return "POSSIBLY encrypted (low confidence)"
        else:
            return "UNLIKELY to be encrypted"
    
    def print_report(self, analysis: Dict):
        """Print formatted analysis report."""
        print("\n" + "=" * 70)
        print("WALLET FILE ANALYSIS REPORT")
        print("=" * 70)
        
        if 'error' in analysis:
            print(f"\nERROR: {analysis['error']}")
            return
        
        print(f"\nFile: {analysis['file_path']}")
        print(f"Size: {analysis['file_size']:,} bytes")
        print(f"Format: {analysis['file_format']}")
        
        print("\n--- ENTROPY ANALYSIS ---")
        ent = analysis['entropy']
        print(f"Shannon Entropy: {ent['value']} / {ent['max_possible']}")
        print(f"Assessment: {ent['interpretation']}")
        
        print("\n--- BYTE DISTRIBUTION ---")
        dist = analysis['byte_distribution']
        print(f"Zero bytes: {dist['zero_bytes']}")
        print(f"Printable characters: {dist['printable_chars']}")
        print(f"High bytes (128-255): {dist['high_bytes']}")
        print(f"Unique byte values: {dist['unique_byte_values']}/256")
        
        print("\n--- RANDOMNESS TEST ---")
        rand = analysis['randomness_test']
        print(f"Chi-Square: {rand['chi_square_value']}")
        print(f"Result: {rand['interpretation']}")
        
        print("\n--- ENCRYPTION INDICATORS ---")
        enc = analysis['encryption_analysis']
        print(f"Encryption metadata detected: {enc['has_encryption_metadata']}")
        if enc['evidence']:
            print("Evidence found:")
            for evidence in enc['evidence']:
                print(f"  • {evidence}")
        print(f"Possible cipher: {enc['possible_cipher']}")
        
        print("\n--- OVERALL ASSESSMENT ---")
        print(f"Encryption Status: {analysis['likely_encrypted']}")
        
        print("\n" + "=" * 70)
        print("Note: This is a heuristic analysis. Definitive determination")
        print("requires examining the wallet software's source code or documentation.")
        print("=" * 70 + "\n")


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Analyze cryptocurrency wallet files for encryption detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python wallet_analyzer_enhanced.py wallet.dat
  python wallet_analyzer_enhanced.py --verbose ~/bitcoin/wallet.dat

Note: This tool is for educational and legitimate recovery purposes only.
        """
    )
    parser.add_argument('wallet_file', help='Path to wallet.dat file')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose logging')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output results in JSON format')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create analyzer and run analysis
    analyzer = WalletAnalyzer(args.wallet_file)
    results = analyzer.analyze()
    
    if args.json:
        import json
        print(json.dumps(results, indent=2))
    else:
        analyzer.print_report(results)


if __name__ == '__main__':
    main()
