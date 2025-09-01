#!/usr/bin/env python3
"""
MARE Web Demo Server

Simple HTTP server for demonstrating MARE Protocol capabilities via web interface.
"""
import json
import time
from typing import Dict, Any
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import logging

from mare import MARESystem, TaskStatus

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MAREWebDemo:
    """Web demonstration interface for MARE Protocol."""
    
    def __init__(self):
        """Initialize web demo."""
        try:
            self.system = MARESystem()
            logger.info("MARE system initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MARE system: {e}")
            self.system = None
        
        self.demo_scenarios = [
            {
                "id": "architecture_ecommerce",
                "name": "E-commerce Architecture",
                "description": "Design scalable e-commerce platform architecture",
                "task": "Design a scalable microservices architecture for an e-commerce platform with user management, product catalog, shopping cart, payment processing, and order fulfillment",
                "output": "Complete system architecture with service boundaries, API contracts, database design, and deployment strategy"
            },
            {
                "id": "implementation_api",
                "name": "REST API Implementation",
                "description": "Implement production-ready REST API",
                "task": "Implement a production-ready REST API for user authentication and management with JWT tokens, rate limiting, input validation, error handling, and comprehensive logging",
                "output": "Working Python FastAPI code with middleware, security features, and unit tests"
            },
            {
                "id": "testing_performance",
                "name": "Performance Testing Suite",
                "description": "Create comprehensive performance testing framework",
                "task": "Design and implement a comprehensive performance testing suite for REST APIs with load testing, stress testing, endurance testing, and automated performance regression detection",
                "output": "Complete test framework with automated load generation, performance metrics collection, and reporting dashboard"
            }
        ]
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        if not self.system:
            return {"status": "error", "message": "MARE system not initialized"}
        
        try:
            health = self.system.get_system_health()
            metrics = self.system.get_performance_metrics()
            reps = self.system.list_available_reps()
            
            return {
                "status": "healthy",
                "health": health,
                "metrics": metrics,
                "reps": [{"name": rep.name, "version": rep.version, "description": rep.description} for rep in reps],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"status": "error", "message": str(e)}
    
    def execute_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """Execute a demo scenario."""
        if not self.system:
            return {"status": "error", "message": "MARE system not initialized"}
        
        # Find the scenario
        scenario = next((s for s in self.demo_scenarios if s["id"] == scenario_id), None)
        if not scenario:
            return {"status": "error", "message": "Scenario not found"}
        
        try:
            start_time = time.time()
            result = self.system.execute_task(scenario["task"], scenario["output"])
            execution_time = time.time() - start_time
            
            return {
                "status": "success",
                "scenario": scenario,
                "result": {
                    "status": result.status.value,
                    "rep_used": result.rep_used,
                    "confidence": result.confidence,
                    "execution_time": execution_time,
                    "output": str(result.result) if result.result else "No output generated",
                    "error": result.error_message
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error executing scenario {scenario_id}: {e}")
            return {"status": "error", "message": str(e)}
    
    def execute_custom_task(self, task_description: str, required_output: str) -> Dict[str, Any]:
        """Execute a custom task."""
        if not self.system:
            return {"status": "error", "message": "MARE system not initialized"}
        
        if not task_description.strip():
            return {"status": "error", "message": "Task description cannot be empty"}
        
        try:
            start_time = time.time()
            result = self.system.execute_task(task_description, required_output)
            execution_time = time.time() - start_time
            
            return {
                "status": "success",
                "task": {
                    "description": task_description,
                    "required_output": required_output
                },
                "result": {
                    "status": result.status.value,
                    "rep_used": result.rep_used,
                    "confidence": result.confidence,
                    "execution_time": execution_time,
                    "output": str(result.result) if result.result else "No output generated",
                    "error": result.error_message
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error executing custom task: {e}")
            return {"status": "error", "message": str(e)}


class MAREWebHandler(BaseHTTPRequestHandler):
    """HTTP request handler for MARE web demo."""
    
    def __init__(self, *args, demo: MAREWebDemo = None, **kwargs):
        self.demo = demo
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            self.serve_html()
        elif self.path == '/status':
            self.serve_json(self.demo.get_system_status())
        elif self.path == '/scenarios':
            self.serve_json({"scenarios": self.demo.demo_scenarios})
        else:
            self.send_error(404, "Not found")
    
    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == '/execute':
            try:
                data = json.loads(post_data.decode('utf-8'))
                if 'scenario_id' in data:
                    result = self.demo.execute_scenario(data['scenario_id'])
                elif 'task_description' in data:
                    result = self.demo.execute_custom_task(
                        data['task_description'], 
                        data.get('required_output', '')
                    )
                else:
                    result = {"status": "error", "message": "Invalid request"}
                
                self.serve_json(result)
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
            except Exception as e:
                self.serve_json({"status": "error", "message": str(e)})
        else:
            self.send_error(404, "Not found")
    
    def serve_html(self):
        """Serve the HTML interface."""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>MARE Protocol - Live Demo</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; text-align: center; margin-bottom: 10px; }
                .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; }
                .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
                .status { display: flex; justify-content: space-between; flex-wrap: wrap; }
                .status-item { margin: 10px; padding: 15px; background: #ecf0f1; border-radius: 5px; flex: 1; min-width: 200px; }
                .scenario { margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; border-left: 4px solid #3498db; }
                button { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; }
                button:hover { background: #2980b9; }
                button:disabled { background: #bdc3c7; cursor: not-allowed; }
                input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin: 5px 0; box-sizing: border-box; }
                textarea { min-height: 100px; resize: vertical; }
                .result { margin: 15px 0; padding: 15px; background: #e8f5e8; border: 1px solid #27ae60; border-radius: 5px; }
                .error { background: #ffe6e6; border-color: #e74c3c; }
                .loading { color: #f39c12; font-weight: bold; }
                pre { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 MARE Protocol - Live Demo</h1>
                <p class="subtitle">Modular Agent Role Embodiment Protocol</p>
                
                <div class="section">
                    <h2>System Status</h2>
                    <div id="status" class="status">
                        <div class="status-item">Status: <span id="system-status">Loading...</span></div>
                        <div class="status-item">REPs: <span id="rep-count">-</span></div>
                        <div class="status-item">Uptime: <span id="uptime">-</span></div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Demo Scenarios</h2>
                    <div id="scenarios">Loading scenarios...</div>
                </div>
                
                <div class="section">
                    <h2>Custom Task</h2>
                    <textarea id="task-description" placeholder="Enter your task description..."></textarea>
                    <input type="text" id="required-output" placeholder="Required output (optional)">
                    <button onclick="executeCustomTask()">Execute Custom Task</button>
                </div>
                
                <div id="results"></div>
            </div>
            
            <script>
                let resultCount = 0;
                
                function loadStatus() {
                    fetch('/status')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('system-status').textContent = data.status;
                            document.getElementById('rep-count').textContent = data.reps ? data.reps.length : '0';
                            document.getElementById('uptime').textContent = data.metrics ? data.metrics.uptime_seconds + 's' : '0s';
                        })
                        .catch(error => console.error('Error loading status:', error));
                }
                
                function loadScenarios() {
                    fetch('/scenarios')
                        .then(response => response.json())
                        .then(data => {
                            const container = document.getElementById('scenarios');
                            container.innerHTML = '';
                            data.scenarios.forEach(scenario => {
                                const div = document.createElement('div');
                                div.className = 'scenario';
                                div.innerHTML = `
                                    <h3>${scenario.name}</h3>
                                    <p>${scenario.description}</p>
                                    <button onclick="executeScenario('${scenario.id}')">Execute</button>
                                `;
                                container.appendChild(div);
                            });
                        })
                        .catch(error => console.error('Error loading scenarios:', error));
                }
                
                function executeScenario(scenarioId) {
                    showLoading();
                    fetch('/execute', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({scenario_id: scenarioId})
                    })
                    .then(response => response.json())
                    .then(data => showResult(data))
                    .catch(error => showError(error));
                }
                
                function executeCustomTask() {
                    const description = document.getElementById('task-description').value;
                    const output = document.getElementById('required-output').value;
                    
                    if (!description.trim()) {
                        alert('Please enter a task description');
                        return;
                    }
                    
                    showLoading();
                    fetch('/execute', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            task_description: description,
                            required_output: output
                        })
                    })
                    .then(response => response.json())
                    .then(data => showResult(data))
                    .catch(error => showError(error));
                }
                
                function showLoading() {
                    const results = document.getElementById('results');
                    const div = document.createElement('div');
                    div.className = 'result loading';
                    div.innerHTML = '<h3>⚡ Executing...</h3><p>MARE Protocol is processing your request...</p>';
                    results.insertBefore(div, results.firstChild);
                }
                
                function showResult(data) {
                    const loadingEl = document.querySelector('.loading');
                    if (loadingEl) loadingEl.remove();
                    
                    const results = document.getElementById('results');
                    const div = document.createElement('div');
                    div.className = data.status === 'success' ? 'result' : 'result error';
                    
                    if (data.status === 'success') {
                        div.innerHTML = `
                            <h3>✅ Execution Complete</h3>
                            <p><strong>REP Used:</strong> ${data.result.rep_used}</p>
                            <p><strong>Confidence:</strong> ${data.result.confidence.toFixed(2)}</p>
                            <p><strong>Execution Time:</strong> ${data.result.execution_time.toFixed(2)}s</p>
                            <p><strong>Status:</strong> ${data.result.status}</p>
                            <pre>${data.result.output}</pre>
                        `;
                    } else {
                        div.innerHTML = `
                            <h3>❌ Execution Failed</h3>
                            <p><strong>Error:</strong> ${data.message}</p>
                        `;
                    }
                    
                    results.insertBefore(div, results.firstChild);
                }
                
                function showError(error) {
                    const loadingEl = document.querySelector('.loading');
                    if (loadingEl) loadingEl.remove();
                    
                    const results = document.getElementById('results');
                    const div = document.createElement('div');
                    div.className = 'result error';
                    div.innerHTML = `
                        <h3>❌ Network Error</h3>
                        <p><strong>Error:</strong> ${error.message}</p>
                    `;
                    results.insertBefore(div, results.firstChild);
                }
                
                // Load initial data
                loadStatus();
                loadScenarios();
                
                // Refresh status every 30 seconds
                setInterval(loadStatus, 30000);
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-length', len(html_content))
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_json(self, data):
        """Serve JSON response."""
        json_data = json.dumps(data, indent=2)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-length', len(json_data))
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to use logger."""
        logger.info(f"{self.address_string()} - {format % args}")


def create_handler(demo):
    """Create a handler with the demo instance."""
    def handler(*args, **kwargs):
        return MAREWebHandler(*args, demo=demo, **kwargs)
    return handler


def main():
    """Main web server execution."""
    print("🚀 MARE Protocol Web Demo")
    print("=" * 50)
    
    # Initialize MARE demo
    demo = MAREWebDemo()
    
    # Create HTTP server
    port = 8080
    handler = create_handler(demo)
    server = HTTPServer(('0.0.0.0', port), handler)
    
    print(f"Starting web server on port {port}")
    print(f"Access the demo at: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n⚠️ Server interrupted by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        server.shutdown()
        if demo.system:
            demo.system.shutdown()
        print("👋 Server stopped")


if __name__ == "__main__":
    main()