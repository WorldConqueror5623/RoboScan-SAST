import re
from src.utils import remove_comments

class Analyzer:
    def __init__(self, file_content, filename):
        # 1. Clean the code (Remove comments but keep line numbers)
        self.clean_content = remove_comments(file_content)
        
        # 2. Split into lines for analysis
        self.lines = self.clean_content.splitlines()
        
        self.filename = filename
        self.issues = []

    def scan(self):
        """
        Runs all security checks on the cleaned code.
        """
        self._check_access_control()
        self._check_reentrancy()
        self._check_phishing()
        return self.issues

    def _add_issue(self, severity, title, line_num, desc):
        self.issues.append({
            "filename": self.filename,
            "severity": severity,
            "title": title,
            "line": line_num,
            "desc": desc
        })

    # RULE 1: Broken Access Control
    # Finds public functions that handle money but lack 'onlyOwner'
    def _check_access_control(self):
        for i, line in enumerate(self.lines):
            # strict check for function definition
            if "function" in line and ("external" in line or "public" in line):
                # If it's not a view/pure function and lacks protection
                if "onlyOwner" not in line and "view" not in line and "pure" not in line:
                    
                    # Look ahead 5 lines for dangerous ops
                    for j in range(1, 6):
                        if i + j < len(self.lines):
                            next_line = self.lines[i + j]
                            if ".transfer(" in next_line or "selfdestruct" in next_line:
                                self._add_issue(
                                    "CRITICAL", 
                                    "Missing Access Control", 
                                    i + 1, 
                                    f"Function '{line.strip()}' performs critical actions but lacks 'onlyOwner'."
                                )
                                break

    # RULE 2: Reentrancy
    # Finds low-level calls that might be unsafe
    def _check_reentrancy(self):
        for i, line in enumerate(self.lines):
            if ".call{value:" in line:
                self._add_issue(
                    "HIGH", 
                    "Reentrancy Risk", 
                    i + 1, 
                    "Low-level call detected. Ensure 'Check-Effects-Interactions' pattern is used."
                )

    # RULE 3: Phishing
    # Finds use of tx.origin
    def _check_phishing(self):
        for i, line in enumerate(self.lines):
            if "tx.origin" in line:
                self._add_issue(
                    "MEDIUM", 
                    "Phishing Risk", 
                    i + 1, 
                    "Avoid 'tx.origin' for authorization. Use 'msg.sender' instead."
                )