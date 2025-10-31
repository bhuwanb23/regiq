#!/usr/bin/env python3
"""
Simple HTTP server to preview generated reports.
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

def start_preview_server():
    """Start a simple HTTP server to preview reports."""
    
    # Change to the generated_outputs directory
    os.chdir(Path(__file__).parent / "generated_outputs")
    
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    
    print(f"🌐 Starting preview server on http://localhost:{PORT}")
    print("📄 Available reports:")
    print("   • http://localhost:8080/executive_report.html")
    print("   • http://localhost:8080/technical_report.html") 
    print("   • http://localhost:8080/regulatory_report.html")
    print("   • http://localhost:8080/frontend_data.json")
    print("\n🔗 Opening executive report in browser...")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"✅ Server running at http://localhost:{PORT}")
        
        # Open browser
        webbrowser.open(f"http://localhost:{PORT}/executive_report.html")
        
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    start_preview_server()
