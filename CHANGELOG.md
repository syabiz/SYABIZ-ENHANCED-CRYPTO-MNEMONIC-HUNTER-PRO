# Changelog

All notable changes to this project will be documented in this file.

## [6.0] - 2026-02-15

### 🎉 Major Release - Complete Rewrite

#### Added
- **Multi-Path Derivation Support**
  - Scan paths 0-19 per mnemonic
  - Configurable path range
  - MetaMask/TrustWallet compatible derivation

- **Multi-Threading Architecture**
  - ThreadPoolExecutor with 1-10 workers
  - Parallel API checking
  - Concurrent futures for better performance

- **6 New Blockchain Networks**
  - Litecoin (LTC)
  - Arbitrum (ARB)
  - Optimism (OP)
  - Avalanche (AVAX)
  - Fantom (FTM)
  - Base (BASE)

- **Enhanced UI Features**
  - Path range selector
  - Thread count adjustment
  - Multi-path toggle
  - Parallel checking toggle
  - Real-time speed monitor (checks/second)
  - Runtime timer
  - Progress bar

- **Advanced Configuration Options**
  - Configurable thread count (1-10)
  - Custom path ranges
  - Toggle parallel processing
  - Test mode with multi-path support

- **Improved Logging System**
  - Smart logging (every 100 checks)
  - Color-coded results (balance/tx/info/warning)
  - Auto-scrolling console
  - Memory-efficient log management

- **Better File Output**
  - Timestamp on every entry
  - Path information included
  - Separate files for balance and transactions
  - Structured format for easy parsing

#### Changed
- **Performance Improvements**
  - 3-6x faster than v5.0
  - Speed: 30-50 checks/second (up from 5-10)
  - Optimized API call patterns
  - Reduced memory footprint

- **Code Architecture**
  - Modular design
  - Better error handling
  - Thread-safe operations
  - Queue-based result processing

- **UI/UX Enhancements**
  - More professional appearance
  - Better status indicators
  - Comprehensive statistics display
  - Smoother operation feedback

#### Fixed
- Solana derivation path issues
- Memory leaks in long-running scans
- Console overflow problems
- Thread synchronization issues
- API rate limit handling

---

## [5.0] - 2026-01-XX

### Initial Public Release

#### Features
- Support for 8 blockchains
- Basic BIP44 derivation
- Single-path scanning
- Simple UI
- API integration for balance checking

#### Supported Chains
- Bitcoin (BTC)
- Ethereum (ETH)
- BNB Chain (BNB)
- Polygon (MATIC)
- Solana (SOL)
- Tron (TRX)
- Bitcoin Cash (BCH)
- Dogecoin (DOGE)

---

## Upcoming Features

### [6.1] - Planned
- [ ] API key rotation system
- [ ] CSV export functionality
- [ ] Statistics dashboard
- [ ] Auto-save configuration

### [6.2] - Planned
- [ ] Custom derivation path support
- [ ] Batch processing mode
- [ ] Result filtering options
- [ ] Advanced search patterns

### [7.0] - Future
- [ ] Database integration (SQLite)
- [ ] Web interface version
- [ ] REST API
- [ ] Multi-language support
- [ ] Docker containerization

---

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- MAJOR version: Incompatible API changes
- MINOR version: Backward-compatible functionality
- PATCH version: Backward-compatible bug fixes

---

## Support

For issues, feature requests, or questions:
- Open an issue: https://github.com/syabiz/ENHANCED-CRYPTO-MNEMONIC-HUNTER-PRO/issues
- Discussions: https://github.com/syabiz/ENHANCED-CRYPTO-MNEMONIC-HUNTER-PRO/discussions
