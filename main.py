import sys
import os
import argparse  # <--- NEW: Professional Argument Parsing
from src.analyzer import Analyzer
from src.reporter import Reporter
from src.utils import log, Colors

def main():
    # 1. SETUP ARGUMENTS
    parser = argparse.ArgumentParser(description="RoboScan v3: Static Analysis Security Tool")
    parser.add_argument("target", help="File or Folder to scan")
    parser.add_argument("--json", action="store_true", help="Generate a JSON report alongside HTML")
    parser.add_argument("--fail-on-critical", action="store_true", help="Return exit code 1 if Critical issues are found (for CI/CD)")
    
    args = parser.parse_args()

    # 2. COLLECT FILES
    files_to_scan = []
    target_path = args.target

    if os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(".sol"):
                    files_to_scan.append(os.path.join(root, file))
    elif os.path.isfile(target_path):
        files_to_scan.append(target_path)

    if not files_to_scan:
        log("❌ No .sol files found!", Colors.RED)
        sys.exit(1)

    # 3. RUN ANALYSIS
    all_issues = []
    log(f"🚀 Starting RoboScan on {len(files_to_scan)} files...", Colors.BLUE)
    
    for file_path in files_to_scan:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analyzer = Analyzer(content, os.path.basename(file_path))
            issues = analyzer.scan()
            all_issues.extend(issues)
        except Exception as e:
            log(f"⚠️  Error reading {file_path}: {e}", Colors.YELLOW)

    # 4. REPORTING
    reporter = Reporter(target_path, all_issues)
    html_file = reporter.generate_html()
    log(f"\n📄 HTML Report: {os.path.abspath(html_file)}", Colors.GREEN)

    if args.json:
        json_file = reporter.save_json()
        log(f"📊 JSON Report: {os.path.abspath(json_file)}", Colors.GREEN)

    # 5. EXIT CODES (CI/CD INTEGRATION)
    critical_count = sum(1 for i in all_issues if i['severity'] == 'CRITICAL')
    
    if critical_count > 0:
        log(f"\n❌ FAILED: Found {critical_count} CRITICAL vulnerabilities.", Colors.RED)
        if args.fail_on_critical:
            sys.exit(1) # This stops the GitHub Pipeline
    else:
        log("\n✅ PASSED: No critical issues found.", Colors.GREEN)
        sys.exit(0)

if __name__ == "__main__":
    main()