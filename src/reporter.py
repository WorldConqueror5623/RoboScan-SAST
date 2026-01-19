import datetime
import os
import json

class Reporter:
    def save_json(self):
        data = {
            "target": self.report_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "summary": self.get_stats(),
            "issues": self.issues
        }
        
        filename = "audit_report.json"
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            
        return filename
    
    def __init__(self, report_name, issues):
        self.report_name = report_name
        self.issues = issues

    def get_stats(self):
        # Calculate summary statistics for the dashboard
        stats = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "TOTAL": len(self.issues)}
        for issue in self.issues:
            sev = issue['severity']
            if sev in stats:
                stats[sev] += 1
        return stats

    def generate_html(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stats = self.get_stats()
        
        # HTML + CSS + JS all in one file for portability
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>RoboScan Audit Report</title>
            <style>
                :root {{
                    --bg-color: #0d1117;
                    --card-bg: #161b22;
                    --text-primary: #c9d1d9;
                    --text-secondary: #8b949e;
                    --accent: #58a6ff;
                    --critical: #da3633;
                    --high: #d29922;
                    --medium: #3fb950;
                    --border: #30363d;
                }}
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; background-color: var(--bg-color); color: var(--text-primary); margin: 0; padding: 20px; }}
                .container {{ max-width: 1000px; margin: 0 auto; }}
                
                /* HEADER */
                .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 20px; margin-bottom: 30px; }}
                h1 {{ margin: 0; font-size: 24px; color: var(--accent); }}
                .meta {{ color: var(--text-secondary); font-size: 14px; }}

                /* STATS DASHBOARD */
                .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px; }}
                .stat-card {{ background: var(--card-bg); padding: 15px; border-radius: 6px; border: 1px solid var(--border); text-align: center; }}
                .stat-value {{ font-size: 28px; font-weight: bold; display: block; }}
                .stat-label {{ font-size: 12px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; }}
                
                .c-critical {{ color: var(--critical); }}
                .c-high {{ color: var(--high); }}
                .c-medium {{ color: var(--medium); }}
                
                /* FILTERS */
                .filters {{ margin-bottom: 20px; }}
                .btn {{ background: var(--card-bg); border: 1px solid var(--border); color: var(--text-primary); padding: 8px 16px; border-radius: 6px; cursor: pointer; margin-right: 10px; transition: 0.2s; }}
                .btn:hover, .btn.active {{ background: var(--accent); color: white; border-color: var(--accent); }}

                /* VULNERABILITY CARDS */
                .issue-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 6px; padding: 20px; margin-bottom: 15px; border-left: 5px solid transparent; }}
                .issue-card.CRITICAL {{ border-left-color: var(--critical); }}
                .issue-card.HIGH {{ border-left-color: var(--high); }}
                .issue-card.MEDIUM {{ border-left-color: var(--medium); }}

                .issue-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
                .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; background: #30363d; }}
                .badge.CRITICAL {{ color: var(--critical); border: 1px solid var(--critical); }}
                .badge.HIGH {{ color: var(--high); border: 1px solid var(--high); }}
                .badge.MEDIUM {{ color: var(--medium); border: 1px solid var(--medium); }}

                .file-loc {{ color: var(--text-secondary); font-family: monospace; font-size: 13px; }}
                .desc {{ line-height: 1.5; }}
                
                .empty-state {{ text-align: center; padding: 50px; color: var(--text-secondary); }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div>
                        <h1>🛡️ RoboScan Report</h1>
                        <span class="meta">Target: {self.report_name}</span>
                    </div>
                    <div class="meta">Scanned on: {timestamp}</div>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-value c-critical">{stats['CRITICAL']}</span>
                        <span class="stat-label">Critical</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value c-high">{stats['HIGH']}</span>
                        <span class="stat-label">High</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value c-medium">{stats['MEDIUM']}</span>
                        <span class="stat-label">Medium</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">{stats['TOTAL']}</span>
                        <span class="stat-label">Total Issues</span>
                    </div>
                </div>

                <div class="filters">
                    <button class="btn active" onclick="filterIssues('ALL')">All</button>
                    <button class="btn" onclick="filterIssues('CRITICAL')">Critical</button>
                    <button class="btn" onclick="filterIssues('HIGH')">High</button>
                    <button class="btn" onclick="filterIssues('MEDIUM')">Medium</button>
                </div>

                <div id="issues-container">
        """

        if not self.issues:
            html += """
            <div class="empty-state">
                <h2>✅ Clean Code!</h2>
                <p>No security vulnerabilities were detected.</p>
            </div>
            """
        else:
            for issue in self.issues:
                html += f"""
                <div class="issue-card {issue['severity']}">
                    <div class="issue-header">
                        <h3 style="margin:0">{issue['title']}</h3>
                        <span class="badge {issue['severity']}">{issue['severity']}</span>
                    </div>
                    <div class="file-loc">📄 {issue['filename']} : Line {issue['line']}</div>
                    <p class="desc">{issue['desc']}</p>
                </div>
                """

        html += """
                </div>
            </div>

            <script>
                function filterIssues(severity) {
                    const cards = document.querySelectorAll('.issue-card');
                    const buttons = document.querySelectorAll('.btn');
                    
                    // Update buttons
                    buttons.forEach(btn => btn.classList.remove('active'));
                    event.target.classList.add('active');

                    // Filter cards
                    cards.forEach(card => {
                        if (severity === 'ALL' || card.classList.contains(severity)) {
                            card.style.display = 'block';
                        } else {
                            card.style.display = 'none';
                        }
                    });
                }
            </script>
        </body>
        </html>
        """
        
        filename = "audit_report.html"
        with open(filename, "w", encoding='utf-8') as f:
            f.write(html)
        
        return filename