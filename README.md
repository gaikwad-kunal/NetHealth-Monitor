# ⚡ DNS Latency Optimizer

A simple Python tool to check which DNS server is fastest for your internet.

---

## 📖 What This Tool Does

When you open a website, your system first asks a DNS server to get the IP address.

Some DNS servers are slow. This tool:
- Checks many DNS servers
- Measures their speed (latency)
- Shows which one is fastest for you

---

## 🚀 Features

- ⚡ Fast checking using multithreading  
- 🌐 Real network test using TCP (port 53)  
- 📊 Clean and easy-to-read output  
- 🏆 Shows fastest DNS automatically  
- 📁 Saves results in CSV file  

---

## 🛠️ Requirements

- Python 3 installed  
- No extra libraries needed  

---

## ▶️ How to Run

### Step 1: Download the code
```bash
git clone https://github.com/YourUsername/DNS-Optimizer.git
### Step 2: Go to folder
```bash
cd DNS-Optimizer
### Step 3: Run the script
```bash
python network_monitor.py
```bash

## 📊 Sample Output

Below is how the output looks:

### 🏆 Final Result
After running, you will see something like:

> **🏆 Fastest DNS: Quad9 (9.9.9.9) → 2.17 ms**

**This means:**
* Quad9 is the fastest for your network.
* You can use this DNS in your system/router.

### 📁 Output File
The tool also saves results like this: 
`dns_results_YYYYMMDD_HHMMSS.csv`

*You can open it in Excel.*
## 💡 How to Use Fast DNS
After finding the fastest DNS:
1. Open Network Settings
2. Change DNS manually
3. Add the fastest IP (example: `9.9.9.9`)

## 🧠 Use Cases
* Faster website loading
* Better gaming ping
* Network testing
* Learning networking

## 📬 Note
* Speed depends on your location
* Run the tool multiple times for accuracy
* Fastest DNS may change

