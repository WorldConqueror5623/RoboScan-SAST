# 🛡️ RoboScan: Automated Smart Contract Security Scanner

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Security](https://img.shields.io/badge/Security-SAST-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)

**RoboScan** is an enterprise-grade Static Application Security Testing (SAST) tool designed to detect critical financial vulnerabilities in Solidity smart contracts. It features "Smart Parsing" to ignore comments, a dark-mode HTML dashboard, and full CI/CD integration for automated auditing.

---

## 🚀 Key Features

* **🔍 Smart Parsing Engine:** Uses regex with pre-processing to strip comments (`//` and `/* */`) before analysis, eliminating false positives.
* **📊 Dual Reporting:** Generates interactive **HTML Dashboards** for humans and **JSON** logs for machine integration.
* **🤖 DevSecOps Ready:** Includes a GitHub Actions workflow that automatically scans code on every push and blocks deployments if Critical bugs are found.
* **⚡ Zero-Dependency:** Runs on standard Python without requiring the Solidity compiler (`solc`) installation.

## 🛡️ Vulnerability Coverage

| Severity | Vulnerability | Description |
| :--- | :--- | :--- |
| 🔴 **CRITICAL** | **Broken Access Control** | Detects public functions handling funds (`.transfer`) without `onlyOwner`. |
| 🟠 **HIGH** | **Reentrancy Risk** | Identifies unsafe low-level calls (`.call{value:}`) violating the Checks-Effects-Interactions pattern. |
| 🟡 **MEDIUM** | **Phishing Vectors** | Flags the use of `tx.origin` for authentication. |

---

## 🛠️ Installation & Usage

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/RoboScan-SAST.git](https://github.com/YOUR_USERNAME/RoboScan-SAST.git)
cd RoboScan-SAST
```

### 2. Run a Standard Scan
Scans all `.sol` files in the target folder and generates an HTML report.
```bash
python main.py contracts/
```

### 3. Run in CI/CD Mode (Strict)
Generates a JSON report and returns Exit Code 1 if critical bugs are found (stopping the pipeline).
```bash
python main.py contracts/ --json --fail-on-critical
```

---

## 📂 Project Structure
```bash
RoboScan-SAST/
├── .github/workflows/   # CI/CD Automation (GitHub Actions)
├── contracts/           # Target Smart Contracts (Vulnerable & Secure)
├── src/                 # Source Code
│   ├── analyzer.py      # Core Security Logic & Rules
│   ├── reporter.py      # HTML/JSON Report Generator
│   └── utils.py         # Helper functions (Smart Cleaner)
├── main.py              # CLI Entry Point
└── README.md            # Documentation
```

---

## ⚙️ CI/CD Integration
This repository includes a pre-configured GitHub Actions workflow (.github/workflows/audit.yml). To enable it:

1. Push this code to GitHub.

2. Navigate to the "Actions" tab.

3. You will see the "RoboScan Security Audit" workflow running automatically on every commit.

---

Disclaimer: This tool is for educational and testing purposes. Always rely on professional audits for production smart contracts.