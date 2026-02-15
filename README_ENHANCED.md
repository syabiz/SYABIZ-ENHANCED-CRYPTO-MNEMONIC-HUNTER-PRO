# Enhanced Multi-Chain Mnemonic Hunter v6.0

## 🚀 Peningkatan Utama

### 1. **Multi-Path Derivation (Path 0-10)**
- Support scanning multiple derivation paths sesuai standar MetaMask/TrustWallet
- Path range dapat dikustomisasi (default: 0-9)
- Format: `m/44'/coin_type'/0'/0/path_index`
- Setiap mnemonic akan dicek hingga 10 addresses berbeda

### 2. **Performa Enhancement**

#### a. **Parallel Processing**
- ThreadPoolExecutor untuk concurrent API checks
- Configurable thread count (1-10 threads)
- Significant speed improvement pada multi-path scanning

#### b. **Optimized API Calls**
- Batch processing untuk multiple addresses
- Better error handling dan retry logic
- Reduced memory footprint

#### c. **Smart Logging**
- Hanya log setiap 100 checks untuk mengurangi I/O
- Queue-based result processing
- Automatic console cleanup (last 1000 lines)

### 3. **Extended Coin/Chain Support**

#### Newly Added:
- **LTC** (Litecoin) - via BlockCypher
- **ARBITRUM** - Layer 2 Ethereum
- **OPTIMISM** - Layer 2 Ethereum  
- **AVALANCHE** (AVAX) - C-Chain
- **FANTOM** (FTM) - Opera Chain
- **BASE** - Coinbase L2

#### Existing (Improved):
- BTC, ETH, BNB, POLYGON, BCH, DOGE, SOL, TRX

### 4. **Enhanced UI Features**

#### New Controls:
- **Path Range Selector**: Set custom path range untuk scanning
- **Thread Count**: Adjust parallelism (1-10 threads)
- **Multi-Path Toggle**: Enable/disable multi-path scanning
- **Parallel Checking**: Enable/disable concurrent checks

#### New Status Display:
- **Real-time Speed**: Checks per second metric
- **Runtime Timer**: Total elapsed time
- **Detailed Stats**: Checked count, Found count, TX count
- **Progress Bar**: Visual feedback

### 5. **Better Data Management**

#### Structured Output:
```
Timestamp | Mnemonic | Path:X | Address | Balance/TX | Coin
```

#### Separate Files:
- `Saldo_Found.txt` - Wallets dengan balance > 0
- `Transaksi_Found.txt` - Wallets dengan transaction history
- `Test_Mnemonic.txt` - Test mode output dengan multi-path

### 6. **Improved Error Handling**
- Graceful API failure handling
- Network timeout protection (5 seconds)
- Silent fail untuk rate limits
- Thread-safe operations

## 📊 Performance Comparison

| Feature | Old Version | Enhanced v6.0 |
|---------|-------------|---------------|
| Paths per Mnemonic | 1 | 1-10 (configurable) |
| Threads | Single | 1-10 (parallel) |
| Speed (ETH) | ~5-10 checks/s | ~30-50 checks/s |
| Coins Supported | 8 | 14 |
| Memory Usage | High (log spam) | Optimized |
| API Rate Limit Handling | Basic | Advanced |

## 🎯 Use Cases

### 1. **Quick Single-Path Scan**
```
- Multi-Path: OFF
- Parallel: OFF  
- Threads: 1
- Path: 0-0
```

### 2. **Comprehensive Multi-Path Scan**
```
- Multi-Path: ON
- Parallel: ON
- Threads: 5
- Path: 0-9
```

### 3. **Deep Scan (Extended Paths)**
```
- Multi-Path: ON
- Parallel: ON
- Threads: 10
- Path: 0-19
```

### 4. **Test Mode (Generate Samples)**
```
- TEST MODE: ON
- Multi-Path: ON
- Generate 100 mnemonics dengan semua paths
```

## ⚙️ Configuration

### API Keys Required:
```python
ETH_API_KEY = "your_etherscan_key"
BSC_API_KEY = "your_bscscan_key"
POLY_API_KEY = "your_polygonscan_key"
ARBITRUM_API_KEY = "your_arbiscan_key"
OPTIMISM_API_KEY = "your_optimistic_etherscan_key"
FANTOM_API_KEY = "your_ftmscan_key"
AVALANCHE_API_KEY = "your_snowtrace_key"
```

### Cara Mendapatkan API Keys (GRATIS):
1. **Etherscan Family** (ETH, ARBITRUM, OPTIMISM, BASE):
   - https://etherscan.io/myapikey

2. **BSCScan** (BNB):
   - https://bscscan.com/myapikey

3. **PolygonScan** (POLYGON):
   - https://polygonscan.com/myapikey

4. **FTMScan** (FANTOM):
   - https://ftmscan.com/myapikey

5. **Snowtrace** (AVALANCHE):
   - https://snowtrace.io/myapikey

### Tidak Perlu API Keys:
- BTC, LTC, BCH, DOGE (BlockCypher free tier)
- SOL (Public RPC)
- TRX (TronGrid free tier)

## 🔧 Coin Derivation Paths

### Standard (BIP44):
```
Bitcoin (BTC):       m/44'/0'/0'/0/x
Ethereum (ETH):      m/44'/60'/0'/0/x
Binance (BNB):       m/44'/714'/0'/0/x
Polygon (MATIC):     m/44'/60'/0'/0/x (sama dengan ETH)
Litecoin (LTC):      m/44'/2'/0'/0/x
Bitcoin Cash (BCH):  m/44'/145'/0'/0/x
Dogecoin (DOGE):     m/44'/3'/0'/0/x
Solana (SOL):        m/44'/501'/0'/0'
Tron (TRX):          m/44'/195'/0'/0/x
```

### Layer 2 & Sidechains:
```
Arbitrum:            m/44'/60'/0'/0/x (ETH derivation)
Optimism:            m/44'/60'/0'/0/x (ETH derivation)
Base:                m/44'/60'/0'/0/x (ETH derivation)
Avalanche C-Chain:   m/44'/60'/0'/0/x (ETH derivation)
Fantom Opera:        m/44'/60'/0'/0/x (ETH derivation)
```

## 📈 Speed Optimization Tips

1. **Increase Thread Count** (untuk multi-path):
   - Single-path: 1-3 threads optimal
   - Multi-path (10 paths): 5-8 threads optimal

2. **Use Parallel Checking**:
   - ON untuk multi-path scanning
   - OFF jika hitting rate limits

3. **Adjust Path Range**:
   - Path 0-4: Most commonly used
   - Path 5-9: Occasionally used
   - Path 10+: Rarely used

4. **Rate Limit Management**:
   - Free tier: ~5 requests/second per API
   - Adjust sleep time jika sering timeout

## 🎨 UI Color Codes

- 🟢 **Green Background**: Wallet dengan Balance > 0
- 🟡 **Yellow Background**: Wallet dengan Transaction History
- 🔵 **Cyan Text**: System messages
- 🟠 **Orange Text**: Warnings
- 🔷 **Blue Text**: Info messages

## 📝 Output File Format

### Saldo_Found.txt:
```
2025-02-15 14:30:22 | abandon ability able... | Path:0 | 0x1234... | Balance:0.05 | ETH
2025-02-15 14:31:45 | another mnemonic here... | Path:3 | 0x5678... | Balance:1.2 | BNB
```

### Transaksi_Found.txt:
```
2025-02-15 14:32:10 | word word word... | Path:0 | 0xabcd... | TX:5 | POLYGON
2025-02-15 14:33:05 | seed phrase here... | Path:7 | 0xefgh... | TX:12 | ETH
```

## ⚠️ Important Notes

1. **API Rate Limits**:
   - Free tiers have limits (typically 5 req/s)
   - Use multiple API keys untuk best performance
   - Monitor untuk 429 errors

2. **Parallel Processing**:
   - More threads ≠ always faster
   - Optimal: 3-5 threads untuk free APIs
   - 8-10 threads untuk paid/unlimited APIs

3. **Multi-Path Scanning**:
   - 10 paths = 10x API calls per mnemonic
   - Balance speed vs thoroughness
   - Consider path usage patterns

4. **Memory Management**:
   - Console auto-cleans after 1000 lines
   - Files append indefinitely (monitor size)
   - Close app properly untuk thread cleanup

## 🔒 Ethical Considerations

⚠️ **DISCLAIMER**: Tool ini untuk educational/recovery purposes only.

- ✅ Legal: Recovering your own lost wallets
- ✅ Legal: Testing entropy/randomness
- ✅ Legal: Educational research
- ❌ Illegal: Attempting to access others' funds
- ❌ Illegal: Brute-forcing existing wallets

**Remember**: Probabilitas menemukan wallet aktif secara random mendekati nol (1 in 2^256 untuk private key).

## 📚 Dependencies

```bash
pip install mnemonic bip-utils requests tkinter
```

## 🚀 Usage

1. Install dependencies
2. Edit API keys di script
3. Run: `python mnemonic_hunter_enhanced.py`
4. Configure settings dalam UI
5. Click START

## 💡 Tips untuk Maksimal Efficiency

1. **Priority Coins**: Focus pada ETH, BNB, POLYGON (paling banyak used)
2. **Path Priority**: Start dengan Path 0-4 dulu
3. **Test Mode First**: Generate samples untuk verify setup
4. **Monitor Logs**: Check untuk API errors
5. **Balance Resources**: Don't max out all settings simultaneously

---

**Version**: 6.0  
**Last Updated**: February 2025  
**Compatibility**: MetaMask, TrustWallet, dan BIP44-compliant wallets
