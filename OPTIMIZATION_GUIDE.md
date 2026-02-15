# 📊 Configuration Guide & Optimization

## Scenario-Based Configuration

### 🎯 Scenario 1: Quick Test / Development
**Goal**: Test functionality, generate samples
```
Coin: ETH
Words: 12
Path Range: 0 - 2
Threads: 1
Multi-Path: ON
Parallel: OFF
TEST MODE: ON
```
**Expected**: ~100 mnemonics dalam 2-3 menit
**Output**: 300 addresses total (100 mnemonics × 3 paths)

---

### 🚀 Scenario 2: Fast Single-Path Scan
**Goal**: Maximum speed, check hanya path 0 (paling umum)
```
Coin: ETH
Words: 12
Path Range: 0 - 0
Threads: 3
Multi-Path: OFF
Parallel: OFF
TEST MODE: OFF
```
**Expected Speed**: 15-20 checks/second
**Best For**: Quick scanning, targeting path 0 only

---

### 💪 Scenario 3: Comprehensive Multi-Path (RECOMMENDED)
**Goal**: Balance antara speed dan coverage
```
Coin: ETH / BNB / POLYGON
Words: 12
Path Range: 0 - 9
Threads: 5
Multi-Path: ON
Parallel: ON
TEST MODE: OFF
```
**Expected Speed**: 30-50 checks/second
**Coverage**: 10 paths per mnemonic
**Best For**: Serious scanning dengan good coverage

---

### 🔥 Scenario 4: Maximum Throughput (Premium APIs)
**Goal**: Maksimal speed dengan unlimited API
```
Coin: ETH
Words: 12
Path Range: 0 - 9
Threads: 10
Multi-Path: ON
Parallel: ON
TEST MODE: OFF
```
**Expected Speed**: 60-100 checks/second
**Requirements**: Paid API plans atau multiple keys
**Best For**: When you have unlimited API access

---

### 🎣 Scenario 5: Deep Scan (Extended Paths)
**Goal**: Cover uncommon derivation paths
```
Coin: ETH
Words: 12
Path Range: 0 - 19
Threads: 8
Multi-Path: ON
Parallel: ON
TEST MODE: OFF
```
**Expected Speed**: 40-60 checks/second
**Coverage**: 20 paths per mnemonic
**Best For**: Recovery scenarios, unusual wallet configs

---

## ⚡ Performance Tuning Matrix

| Threads | Paths | Parallel | Speed (checks/s) | API Calls/s | Best For |
|---------|-------|----------|------------------|-------------|----------|
| 1 | 1 | OFF | 5-8 | 5-8 | Conservative, Free APIs |
| 3 | 1 | OFF | 15-20 | 15-20 | Single-path fast |
| 3 | 10 | ON | 20-30 | 20-30 | Balanced multi-path |
| 5 | 10 | ON | 30-50 | 30-50 | Recommended setup |
| 8 | 10 | ON | 50-70 | 50-70 | Paid APIs |
| 10 | 10 | ON | 60-100 | 60-100 | Maximum (requires paid) |
| 5 | 20 | ON | 30-40 | 30-40 | Deep scan |

---

## 🌐 Coin-Specific Recommendations

### 💎 Ethereum & EVM Chains (ETH, BNB, POLYGON, ARBITRUM, etc.)
```
Recommended Paths: 0-9
API Requirements: Medium (need API keys)
Best Threads: 5-8
Expected Hit Rate: Low but valuable
Priority: HIGH (most valuable finds)
```

### 🟠 Bitcoin & Forks (BTC, BCH, LTC, DOGE)
```
Recommended Paths: 0-4
API Requirements: Low (BlockCypher free tier)
Best Threads: 3-5
Expected Hit Rate: Very low
Priority: MEDIUM
```

### ☀️ Solana (SOL)
```
Recommended Paths: 0-2 (different derivation)
API Requirements: Low (public RPC)
Best Threads: 2-3
Expected Hit Rate: Very low
Priority: LOW (newer ecosystem)
```

---

## 🎨 Multi-Coin Strategy

### Strategy A: Sequential Coin Scanning
**Approach**: Scan satu coin secara mendalam sebelum pindah
```
Day 1: ETH (paths 0-9)
Day 2: BNB (paths 0-9)
Day 3: POLYGON (paths 0-9)
Day 4: ARBITRUM (paths 0-9)
```
**Pros**: Deep coverage per coin
**Cons**: Slower untuk cover semua coins

### Strategy B: Round-Robin
**Approach**: Rotate coins setiap X mnemonics
```
Batch 1 (100 mnemonics): ETH
Batch 2 (100 mnemonics): BNB
Batch 3 (100 mnemonics): POLYGON
Repeat...
```
**Pros**: Balanced coverage
**Cons**: May miss patterns

### Strategy C: Priority Focus (RECOMMENDED)
**Approach**: Focus pada high-value chains
```
80% time: ETH, BNB, POLYGON (most active)
15% time: ARBITRUM, OPTIMISM, BASE (L2s)
5% time: Others (BTC, DOGE, etc.)
```
**Pros**: Best ROI untuk effort
**Cons**: Miss opportunities di smaller chains

---

## 📈 Expected Results & Statistics

### Probability Analysis (untuk random 12-word mnemonic):
```
Total possible combinations: 2^128 ≈ 3.4 × 10^38
Active wallets (estimated): ~100 million
Chance per check: ~1 in 3.4 × 10^30

Realistic expectations:
- Finding ANY wallet: Extremely unlikely
- Finding ACTIVE wallet: Virtually impossible via pure random
- Best use case: RECOVERY of your own lost seeds
```

### If Scanning 1 Million Addresses:
```
At 50 checks/second:
- Time: ~5.5 hours
- Total paths checked: 10 million (if multi-path x10)
- Expected finds: 0 (statistically)
- Purpose: Testing, research, recovery
```

---

## 🛠️ Troubleshooting Performance Issues

### Issue: Slow Speed (<10 checks/s)
**Causes**:
- Too many threads causing bottleneck
- API rate limiting
- Network latency

**Solutions**:
1. Reduce threads ke 3-5
2. Check API key validity
3. Verify internet connection
4. Disable parallel if hitting limits

### Issue: Frequent API Errors
**Causes**:
- Invalid API keys
- Rate limit exceeded
- API service down

**Solutions**:
1. Verify API keys valid
2. Reduce thread count
3. Increase sleep time in code
4. Use multiple API keys rotation
5. Check API service status

### Issue: High CPU Usage
**Causes**:
- Too many threads
- Logging too much

**Solutions**:
1. Reduce threads
2. Increase log interval
3. Disable verbose logging
4. Close other applications

### Issue: Memory Leak
**Causes**:
- Console not clearing
- File handles not closing

**Solutions**:
1. Restart app periodically
2. Clear output files
3. Monitor with Task Manager
4. Check code for resource leaks

---

## 💰 API Cost Analysis

### Free Tier Limitations:
```
Etherscan Family:
- Rate: 5 calls/second
- Daily: ~100,000 calls
- Cost: FREE

BlockCypher:
- Rate: 3 calls/second  
- Daily: ~200 hits (then slower)
- Cost: FREE

Optimization:
- 5 threads = stay under limit
- Mix different chains
- Use test mode untuk development
```

### Paid Tier Benefits:
```
Etherscan Standard ($150/month):
- Rate: 30 calls/second
- Daily: Unlimited
- ROI: If serious about scanning

Recommendation:
- Start with free tier
- Upgrade jika bottlenecked
- Consider multiple free accounts
```

---

## 🔐 Security Best Practices

1. **Never Share API Keys**: Keep private
2. **Rotate Keys**: Change periodically
3. **Monitor Usage**: Watch for anomalies
4. **Secure Storage**: Encrypt found seeds
5. **Local Only**: Don't upload results to cloud
6. **Clean Up**: Delete test files regularly

---

## 📊 Monitoring Dashboard (Manual)

Track these metrics:
```
✓ Checks per second (target: 30-50)
✓ API error rate (target: <5%)
✓ CPU usage (target: <70%)
✓ Memory usage (target: <2GB)
✓ Finds per 1000 checks (expected: 0)
✓ Runtime stability (target: 24h+)
```

---

## 🎯 Success Criteria

**For Testing:**
- ✓ Generates valid mnemonics
- ✓ Derives correct addresses
- ✓ API calls working
- ✓ Multi-path scanning functional

**For Production:**
- ✓ Stable 24h+ runtime
- ✓ Consistent 30-50 checks/s
- ✓ No crashes or freezes
- ✓ Proper logging dan file output

**For Recovery:**
- ✓ Can check your known patterns
- ✓ Verifies with test wallets
- ✓ Accurate balance reporting
- ✓ All paths covered

---

## 🚦 Quick Start Checklist

- [ ] Install Python dependencies
- [ ] Get free API keys (Etherscan, BSCScan, etc.)
- [ ] Edit script with your API keys
- [ ] Run in TEST MODE first
- [ ] Verify 100 samples generated
- [ ] Check Test_Mnemonic.txt output
- [ ] Disable TEST MODE
- [ ] Configure your preferred settings
- [ ] Monitor first 10 minutes
- [ ] Adjust based on performance
- [ ] Set up untuk long-term run

---

**Remember**: Ini adalah tool untuk education dan recovery purposes. Scanning random untuk find active wallets adalah statistically futile. Best use adalah untuk recover your OWN lost seeds dengan partial information.
