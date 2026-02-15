import threading
import time
import requests
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from mnemonic import Mnemonic
from bip_utils import (
    Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
)
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import json

# --- KONFIGURASI API KEY ---
ETH_API_KEY = "YOUR_API_KEY"
BSC_API_KEY = "YOUR_API_KEY"
POLY_API_KEY = "YOUR_API_KEY"
ARBITRUM_API_KEY = "YOUR_API_KEY"
OPTIMISM_API_KEY = "YOUR_API_KEY"
FANTOM_API_KEY = "YOUR_API_KEY"
AVALANCHE_API_KEY = "YOUR_API_KEY"

class MnemonicHunterEnhanced:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Multi-Chain Mnemonic Hunter v6.0")
        self.root.geometry("1100x700")
        self.root.configure(bg="#0a0a0a")
        
        self.running = False
        self.paused = False
        self.found_count = 0
        self.tx_count = 0
        self.checked_count = 0
        self.start_time = None
        
        # Queue untuk hasil dari thread pool
        self.result_queue = Queue()
        
        # Thread pool untuk parallel checking
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#0a0a0a")
        header.pack(fill="x", pady=10)
        tk.Label(header, text="⚡ SYABIZ ENHANCED CRYPTO MNEMONIC HUNTER PRO v1.0 ⚡", 
                 font=("Consolas", 16, "bold"), fg="#00ffcc", bg="#0a0a0a").pack()

        # Control Frame
        ctrl_frame = tk.Frame(self.root, bg="#161616", padx=10, pady=10, 
                              highlightbackground="#333", highlightthickness=1)
        ctrl_frame.pack(fill="x", padx=15)

        # Row 1: Coin dan Words
        tk.Label(ctrl_frame, text="Coin:", fg="#aaa", bg="#161616").grid(row=0, column=0, padx=2, sticky="e")
        self.coin_var = tk.StringVar(value="ETH")
        coins_list = [
            "BTC", "ETH", "BNB", "SOL", "TRX", "POLYGON", "BCH", "DOGE",
            "LTC", "ARBITRUM", "OPTIMISM", "AVALANCHE", "FANTOM", "BASE"
        ]
        cb_coin = ttk.Combobox(ctrl_frame, textvariable=self.coin_var, values=coins_list, width=10)
        cb_coin.grid(row=0, column=1, padx=5)

        tk.Label(ctrl_frame, text="Words:", fg="#aaa", bg="#161616").grid(row=0, column=2, padx=2, sticky="e")
        self.word_var = tk.StringVar(value="12")
        cb_word = ttk.Combobox(ctrl_frame, textvariable=self.word_var, values=["12", "24"], width=4)
        cb_word.grid(row=0, column=3, padx=5)

        # Row 1: Path Range
        tk.Label(ctrl_frame, text="Path Range:", fg="#aaa", bg="#161616").grid(row=0, column=4, padx=5, sticky="e")
        self.path_start = tk.StringVar(value="0")
        self.path_end = tk.StringVar(value="9")
        
        path_frame = tk.Frame(ctrl_frame, bg="#161616")
        path_frame.grid(row=0, column=5, padx=2)
        tk.Entry(path_frame, textvariable=self.path_start, width=3, bg="#222", fg="white").pack(side="left")
        tk.Label(path_frame, text="to", fg="#aaa", bg="#161616").pack(side="left", padx=2)
        tk.Entry(path_frame, textvariable=self.path_end, width=3, bg="#222", fg="white").pack(side="left")

        # Row 1: Threads
        tk.Label(ctrl_frame, text="Threads:", fg="#aaa", bg="#161616").grid(row=0, column=6, padx=5, sticky="e")
        self.thread_var = tk.StringVar(value="3")
        cb_thread = ttk.Combobox(ctrl_frame, textvariable=self.thread_var, 
                                 values=["1", "2", "3", "5", "8", "10"], width=4)
        cb_thread.grid(row=0, column=7, padx=5)

        # Row 2: Checkboxes
        check_frame = tk.Frame(ctrl_frame, bg="#161616")
        check_frame.grid(row=1, column=0, columnspan=4, sticky="w", pady=5)
        
        self.test_var = tk.BooleanVar()
        tk.Checkbutton(check_frame, text="TEST MODE", variable=self.test_var, bg="#161616", 
                       fg="#00ffcc", selectcolor="black", activebackground="#161616").pack(side="left", padx=5)
        
        self.multi_path_var = tk.BooleanVar(value=True)
        tk.Checkbutton(check_frame, text="MULTI-PATH SCAN", variable=self.multi_path_var, bg="#161616", 
                       fg="#ffcc00", selectcolor="black", activebackground="#161616").pack(side="left", padx=5)
        
        self.parallel_var = tk.BooleanVar(value=True)
        tk.Checkbutton(check_frame, text="PARALLEL CHECKING", variable=self.parallel_var, bg="#161616", 
                       fg="#ff6600", selectcolor="black", activebackground="#161616").pack(side="left", padx=5)

        # Row 2: Control Buttons
        btn_frame = tk.Frame(ctrl_frame, bg="#161616")
        btn_frame.grid(row=1, column=4, columnspan=4, sticky="e", pady=5)

        self.btn_start = tk.Button(btn_frame, text="▶ START", command=self.start_scan, 
                                   bg="#0066ff", fg="white", width=8, font=("Arial", 8, "bold"), relief="flat")
        self.btn_start.pack(side="left", padx=2)

        self.btn_pause = tk.Button(btn_frame, text="⏸ PAUSE", command=self.pause_scan, 
                                   bg="#ff9900", fg="black", width=8, font=("Arial", 8, "bold"), relief="flat")
        self.btn_pause.pack(side="left", padx=2)

        self.btn_stop = tk.Button(btn_frame, text="⏹ STOP", command=self.stop_scan, 
                                  bg="#cc0000", fg="white", width=8, font=("Arial", 8, "bold"), relief="flat")
        self.btn_stop.pack(side="left", padx=2)

        self.btn_close = tk.Button(btn_frame, text="✖ EXIT", command=self.close_app, 
                                   bg="#333", fg="white", width=8, font=("Arial", 8, "bold"), relief="flat")
        self.btn_close.pack(side="left", padx=2)

        # Status Frame
        status_frame = tk.Frame(self.root, bg="#222", padx=10, pady=5)
        status_frame.pack(fill="x", padx=15, pady=5)
        
        status_left = tk.Frame(status_frame, bg="#222")
        status_left.pack(side="left", fill="x", expand=True)
        
        self.lbl_status = tk.Label(status_left, text="STATUS: IDLE", fg="#00ff00", 
                                   bg="#222", font=("Consolas", 10, "bold"))
        self.lbl_status.pack(anchor="w")
        
        self.lbl_stats = tk.Label(status_left, text="Checked: 0 | Found: 0 | TX: 0 | Speed: 0/s", 
                                  fg="#aaa", bg="#222", font=("Consolas", 9))
        self.lbl_stats.pack(anchor="w")
        
        self.lbl_time = tk.Label(status_left, text="Runtime: 00:00:00", 
                                fg="#aaa", bg="#222", font=("Consolas", 9))
        self.lbl_time.pack(anchor="w")

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill="x", padx=15, pady=2)

        # Console Output
        console_frame = tk.Frame(self.root, bg="#000")
        console_frame.pack(expand=True, fill="both", padx=15, pady=5)
        
        scrollbar = tk.Scrollbar(console_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.txt_console = tk.Text(console_frame, bg="#000", fg="#00ff00", 
                                   font=("Consolas", 9), borderwidth=0, padx=10, pady=10,
                                   yscrollcommand=scrollbar.set)
        self.txt_console.pack(side="left", expand=True, fill="both")
        scrollbar.config(command=self.txt_console.yview)
        
        # Tags untuk highlighting
        self.txt_console.tag_config("found_bal", background="#006400", foreground="white")
        self.txt_console.tag_config("found_tx", background="#8b8000", foreground="white")
        self.txt_console.tag_config("sys", foreground="#00ffff")
        self.txt_console.tag_config("warn", foreground="#ff6600")
        self.txt_console.tag_config("info", foreground="#6699ff")

    def update_status(self, text, stats=None):
        self.lbl_status.config(text=f"STATUS: {text}")
        if stats:
            self.lbl_stats.config(text=stats)

    def update_runtime(self):
        """Update runtime display"""
        if self.running and self.start_time and not self.paused:
            elapsed = int(time.time() - self.start_time)
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            self.lbl_time.config(text=f"Runtime: {hours:02d}:{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_runtime)

    def log_to_gui(self, msg, tag=None):
        self.txt_console.insert(tk.END, msg + "\n", tag)
        self.txt_console.see(tk.END)
        # Keep only last 1000 lines
        if float(self.txt_console.index('end-1c')) > 1000:
            self.txt_console.delete('1.0', '100.0')

    def start_scan(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.checked_count = 0
            self.found_count = 0
            self.tx_count = 0
            self.start_time = time.time()
            
            self.btn_start.config(state="disabled")
            self.progress.start(10)
            self.update_status("RUNNING...")
            self.update_runtime()
            
            # Update thread pool size
            max_workers = int(self.thread_var.get())
            self.executor = ThreadPoolExecutor(max_workers=max_workers)
            
            threading.Thread(target=self.main_loop, daemon=True).start()
            self.log_to_gui(f"[SYSTEM] Scan started with {max_workers} threads", "sys")

    def pause_scan(self):
        if self.running:
            self.paused = not self.paused
            self.btn_pause.config(text="▶ RESUME" if self.paused else "⏸ PAUSE")
            state = "PAUSED" if self.paused else "RUNNING..."
            self.update_status(state)
            self.log_to_gui(f"[SYSTEM] {state}", "sys")

    def stop_scan(self):
        self.running = False
        self.paused = False
        self.btn_start.config(state="normal")
        self.progress.stop()
        self.update_status("STOPPED")
        self.log_to_gui("[SYSTEM] Scan Stopped.", "sys")

    def close_app(self):
        if messagebox.askokcancel("Exit", "Close and stop all processes?"):
            self.running = False
            self.executor.shutdown(wait=False)
            self.root.destroy()
            sys.exit()

    def get_coin_config(self, coin_symbol):
        """Return coin configuration for API checking"""
        config = {
            "BTC": {
                "type": "blockcypher",
                "coin": Bip44Coins.BITCOIN,
                "code": "btc",
                "divisor": 10**8
            },
            "ETH": {
                "type": "etherscan",
                "coin": Bip44Coins.ETHEREUM,
                "api_key": ETH_API_KEY,
                "base_url": "https://api.etherscan.io/api",
                "divisor": 10**18
            },
            "BNB": {
                "type": "etherscan",
                "coin": Bip44Coins.BINANCE_SMART_CHAIN,
                "api_key": BSC_API_KEY,
                "base_url": "https://api.bscscan.com/api",
                "divisor": 10**18
            },
            "POLYGON": {
                "type": "etherscan",
                "coin": Bip44Coins.ETHEREUM,  # Uses ETH derivation
                "api_key": POLY_API_KEY,
                "base_url": "https://api.polygonscan.com/api",
                "divisor": 10**18
            },
            "ARBITRUM": {
                "type": "etherscan",
                "coin": Bip44Coins.ETHEREUM,
                "api_key": ARBITRUM_API_KEY,
                "base_url": "https://api.arbiscan.io/api",
                "divisor": 10**18
            },
            "OPTIMISM": {
                "type": "etherscan",
                "coin": Bip44Coins.ETHEREUM,
                "api_key": OPTIMISM_API_KEY,
                "base_url": "https://api-optimistic.etherscan.io/api",
                "divisor": 10**18
            },
            "AVALANCHE": {
                "type": "etherscan",
                "coin": Bip44Coins.AVAX_C_CHAIN,
                "api_key": AVALANCHE_API_KEY,
                "base_url": "https://api.snowtrace.io/api",
                "divisor": 10**18
            },
            "FANTOM": {
                "type": "etherscan",
                "coin": Bip44Coins.FANTOM_OPERA,
                "api_key": FANTOM_API_KEY,
                "base_url": "https://api.ftmscan.com/api",
                "divisor": 10**18
            },
            "BASE": {
                "type": "etherscan",
                "coin": Bip44Coins.ETHEREUM,
                "api_key": ETH_API_KEY,
                "base_url": "https://api.basescan.org/api",
                "divisor": 10**18
            },
            "SOL": {
                "type": "solana",
                "coin": Bip44Coins.SOLANA,
                "divisor": 10**9
            },
            "TRX": {
                "type": "tron",
                "coin": Bip44Coins.TRON,
                "divisor": 10**6
            },
            "BCH": {
                "type": "blockcypher",
                "coin": Bip44Coins.BITCOIN_CASH,
                "code": "bcy",
                "divisor": 10**8
            },
            "DOGE": {
                "type": "blockcypher",
                "coin": Bip44Coins.DOGECOIN,
                "code": "doge",
                "divisor": 10**8
            },
            "LTC": {
                "type": "blockcypher",
                "coin": Bip44Coins.LITECOIN,
                "code": "ltc",
                "divisor": 10**8
            }
        }
        return config.get(coin_symbol, config["ETH"])

    def check_api(self, address, coin_config):
        """Check balance and transactions via API"""
        if self.test_var.get():
            return 0, 0
        
        try:
            api_type = coin_config.get("type")
            
            if api_type == "blockcypher":
                code = coin_config.get("code")
                url = f"https://api.blockcypher.com/v1/{code}/main/addrs/{address}/balance"
                res = requests.get(url, timeout=5).json()
                bal = res.get("balance", 0) / coin_config["divisor"]
                tx = res.get("n_tx", 0)
                return bal, tx
            
            elif api_type == "etherscan":
                base_url = coin_config.get("base_url")
                api_key = coin_config.get("api_key")
                
                # Balance check
                bal_url = f"{base_url}?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
                bal_res = requests.get(bal_url, timeout=5).json()
                bal = int(bal_res.get('result', 0)) / coin_config["divisor"]
                
                # TX check
                tx_url = f"{base_url}?module=account&action=txlist&address={address}&page=1&offset=1&apikey={api_key}"
                tx_res = requests.get(tx_url, timeout=5).json()
                tx = len(tx_res.get('result', [])) if tx_res.get('status') == '1' else 0
                
                return bal, tx
            
            elif api_type == "solana":
                # Solana RPC check (simplified)
                url = "https://api.mainnet-beta.solana.com"
                payload = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getBalance",
                    "params": [address]
                }
                res = requests.post(url, json=payload, timeout=5).json()
                bal = res.get("result", {}).get("value", 0) / coin_config["divisor"]
                return bal, 1 if bal > 0 else 0
            
            elif api_type == "tron":
                # Tron API check
                url = f"https://api.trongrid.io/v1/accounts/{address}"
                res = requests.get(url, timeout=5).json()
                bal = res.get("data", [{}])[0].get("balance", 0) / coin_config["divisor"]
                return bal, 1 if bal > 0 else 0
                
        except Exception as e:
            # Silent fail untuk rate limits / network errors
            pass
        
        return 0, 0

    def derive_address(self, seed_bytes, coin_config, path_index):
        """Derive address for specific path index"""
        try:
            coin_type = coin_config["coin"]
            bip44_mst = Bip44.FromSeed(seed_bytes, coin_type)
            
            # Standard derivation: m/44'/coin'/0'/0/path_index
            bip44_addr = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(path_index)
            address = bip44_addr.PublicKey().ToAddress()
            
            return address
        except Exception as e:
            return None

    def check_address_wrapper(self, args):
        """Wrapper for parallel execution"""
        address, coin_config, coin_symbol, path_index = args
        if address:
            bal, tx = self.check_api(address, coin_config)
            return (address, bal, tx, coin_symbol, path_index)
        return None

    def main_loop(self):
        mnemo = Mnemonic("english")
        test_count = 0
        
        path_start = int(self.path_start.get())
        path_end = int(self.path_end.get())
        
        last_update_time = time.time()
        check_speed = 0

        while self.running:
            if self.paused:
                time.sleep(0.5)
                continue
            
            try:
                # Generate Mnemonic
                strength = 128 if self.word_var.get() == "12" else 256
                words = mnemo.generate(strength=strength)
                seed_bytes = Bip39SeedGenerator(words).Generate()
                
                coin_symbol = self.coin_var.get()
                coin_config = self.get_coin_config(coin_symbol)
                
                if self.multi_path_var.get():
                    # Multi-path scanning
                    addresses = []
                    for path_idx in range(path_start, path_end + 1):
                        addr = self.derive_address(seed_bytes, coin_config, path_idx)
                        if addr:
                            addresses.append((addr, coin_config, coin_symbol, path_idx))
                    
                    if self.parallel_var.get():
                        # Parallel checking
                        futures = [self.executor.submit(self.check_address_wrapper, args) for args in addresses]
                        
                        for future in as_completed(futures):
                            if not self.running or self.paused:
                                break
                            
                            result = future.result()
                            if result:
                                address, bal, tx, coin_sym, path_idx = result
                                self.checked_count += 1
                                
                                # Process results
                                self.process_result(words, address, bal, tx, coin_sym, path_idx)
                    else:
                        # Sequential checking
                        for args in addresses:
                            if not self.running or self.paused:
                                break
                            
                            result = self.check_address_wrapper(args)
                            if result:
                                address, bal, tx, coin_sym, path_idx = result
                                self.checked_count += 1
                                self.process_result(words, address, bal, tx, coin_sym, path_idx)
                else:
                    # Single path (path 0)
                    address = self.derive_address(seed_bytes, coin_config, 0)
                    if address:
                        bal, tx = self.check_api(address, coin_config)
                        self.checked_count += 1
                        self.process_result(words, address, bal, tx, coin_symbol, 0)
                
                # Update stats periodically
                current_time = time.time()
                if current_time - last_update_time >= 1.0:
                    elapsed = current_time - self.start_time if self.start_time else 1
                    check_speed = self.checked_count / elapsed if elapsed > 0 else 0
                    
                    stats = f"Checked: {self.checked_count} | Found: {self.found_count} | TX: {self.tx_count} | Speed: {check_speed:.1f}/s"
                    self.root.after(0, self.update_status, "RUNNING...", stats)
                    last_update_time = current_time
                
                # Test mode
                if self.test_var.get():
                    test_count += 1
                    for path_idx in range(path_start, path_end + 1):
                        addr = self.derive_address(seed_bytes, coin_config, path_idx)
                        if addr:
                            self.save_to_file("Test_Mnemonic.txt", 
                                            f"{words} | Path:{path_idx} | {addr}")
                    
                    self.root.after(0, lambda tc=test_count: self.update_status(
                        "TESTING...", f"Saved: {tc}/100"))
                    
                    if test_count >= 100:
                        self.running = False
                        self.root.after(0, lambda: self.btn_start.config(state="normal"))
                        self.root.after(0, lambda: self.progress.stop())
                        self.root.after(0, lambda: messagebox.showinfo(
                            "Done", f"100 Mnemonics with {path_end - path_start + 1} paths each saved!"))
                        break
                
                # Rate limiting
                time.sleep(0.05 if self.parallel_var.get() else 0.1)
                
            except Exception as e:
                self.root.after(0, self.log_to_gui, f"[ERROR] {str(e)}", "warn")
                time.sleep(1)

    def process_result(self, words, address, bal, tx, coin_symbol, path_index):
        """Process and log check results"""
        tag = None
        
        if bal > 0:
            tag = "found_bal"
            self.found_count += 1
            data = f"{words} | Path:{path_index} | {address} | Balance:{bal} | {coin_symbol}"
            self.save_to_file("Saldo_Found.txt", data)
            msg = f"💰 [{coin_symbol}] Path:{path_index} | {address[:16]}... | BAL: {bal:.8f}"
            self.root.after(0, self.log_to_gui, msg, tag)
            
        elif tx > 0:
            tag = "found_tx"
            self.tx_count += 1
            data = f"{words} | Path:{path_index} | {address} | TX:{tx} | {coin_symbol}"
            self.save_to_file("Transaksi_Found.txt", data)
            msg = f"📊 [{coin_symbol}] Path:{path_index} | {address[:16]}... | TX: {tx}"
            self.root.after(0, self.log_to_gui, msg, tag)
        
        else:
            # Log only every 100th check untuk mengurangi spam
            if self.checked_count % 100 == 0:
                msg = f"[{coin_symbol}] Checked {self.checked_count} addresses..."
                self.root.after(0, self.log_to_gui, msg, "info")

    def save_to_file(self, filename, content):
        """Save results to file"""
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {content}\n")
        except Exception as e:
            print(f"Error saving to file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MnemonicHunterEnhanced(root)
    root.mainloop()
