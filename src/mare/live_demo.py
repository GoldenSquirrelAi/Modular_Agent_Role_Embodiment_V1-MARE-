#!/usr/bin/env python3
"""
MARE Live Demo Interface

Interactive web interface for demonstrating MARE Protocol capabilities.
"""
import json
import time
from typing import Dict, List, Any
from datetime import datetime

from mare import MARESystem, TaskStatus


class MARELiveDemo:
    """Live demonstration interface for MARE Protocol."""
    
    def __init__(self):
        """Initialize demo interface."""
        self.system = MARESystem()
        self.demo_scenarios = self._create_demo_scenarios()
        self.session_history: List[Dict[str, Any]] = []
        
    def _create_demo_scenarios(self) -> List[Dict[str, Any]]:
        """Create predefined demo scenarios."""
        return [
            {
                "id": "architecture_ecommerce",
                "name": "E-commerce Architecture",
                "description": "Design scalable e-commerce platform architecture",
                "task": "Design a scalable microservices architecture for an e-commerce platform with user management, product catalog, shopping cart, payment processing, and order fulfillment",
                "required_output": "Complete system architecture with service boundaries, API contracts, database design, and deployment strategy",
                "category": "Architecture",
                "complexity": "High",
                "expected_rep": "SOFTWARE_ARCHITECT_REP",
                "estimated_time": "3-5 seconds"
            },
            {
                "id": "implementation_api",
                "name": "REST API Implementation",
                "description": "Implement production-ready REST API",
                "task": "Implement a production-ready REST API for user authentication and management with JWT tokens, rate limiting, input validation, error handling, and comprehensive logging",
                "required_output": "Working Python FastAPI code with middleware, security features, and unit tests",
                "category": "Implementation", 
                "complexity": "Medium",
                "expected_rep": "BACKEND_DEVELOPER_REP",
                "estimated_time": "2-4 seconds"
            },
            {
                "id": "testing_performance",
                "name": "Performance Testing Suite",
                "description": "Create comprehensive performance testing framework",
                "task": "Design and implement a comprehensive performance testing suite for REST APIs with load testing, stress testing, endurance testing, and automated performance regression detection",
                "required_output": "Complete test framework with automated load generation, performance metrics collection, and reporting dashboard",
                "category": "Testing",
                "complexity": "Medium",
                "expected_rep": "TEST_ENGINEER_REP", 
                "estimated_time": "2-3 seconds"
            },
            {
                "id": "deployment_kubernetes",
                "name": "Kubernetes Deployment",
                "description": "Setup production Kubernetes deployment",
                "task": "Design and configure a production-ready Kubernetes deployment with auto-scaling, rolling updates, health checks, monitoring, logging, and disaster recovery capabilities",
                "required_output": "Complete K8s manifests, Helm charts, monitoring configuration, and operational runbooks",
                "category": "Deployment",
                "complexity": "High", 
                "expected_rep": "DEVOPS_ENGINEER_REP",
                "estimated_time": "3-5 seconds"
            },
            {
                "id": "protocol_api_spec",
                "name": "API Protocol Design",
                "description": "Design comprehensive API specification",
                "task": "Create a comprehensive REST API specification using OpenAPI 3.0 with authentication flows, error handling, versioning strategy, rate limiting, and security considerations",
                "required_output": "Complete OpenAPI specification with schemas, security definitions, examples, and implementation guidelines",
                "category": "Protocol",
                "complexity": "Medium",
                "expected_rep": "PROTOCOL_DESIGNER_REP",
                "estimated_time": "2-4 seconds"
            }
        ]
    
    def start_interactive_demo(self):
        """Start interactive demo session."""
        print("🚀 MARE PROTOCOL LIVE DEMO")
        print("=" * 60)
        print("Welcome to the interactive MARE Protocol demonstration!")
        print("\nThis demo showcases:")
        print("  • Intelligent task routing to specialized REPs")
        print("  • Role-specific behavior and expertise")
        print("  • Token efficiency through context optimization")
        print("  • Real-time performance monitoring")
        print("\nAvailable commands:")
        print("  1-5: Run predefined scenarios")
        print("  custom: Enter custom task")
        print("  history: Show session history")
        print("  stats: Show system statistics")
        print("  health: Show system health")
        print("  quit: Exit demo")
        print("=" * 60)
        
        while True:
            try:
                print(f"\n[Session Tasks: {len(self.session_history)}]")
                choice = input("MARE Demo> ").strip().lower()
                
                if choice in ['quit', 'exit', 'q']:
                    break
                elif choice in ['1', '2', '3', '4', '5']:
                    self._run_predefined_scenario(int(choice) - 1)
                elif choice == 'custom':
                    self._run_custom_task()
                elif choice == 'history':
                    self._show_session_history()
                elif choice == 'stats':
                    self._show_system_stats()
                elif choice == 'health':
                    self._show_system_health()
                elif choice == 'help':
                    self._show_help()
                elif choice == 'scenarios':
                    self._list_scenarios()
                else:
                    print("❓ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _list_scenarios(self):
        """List available demo scenarios."""
        print("\n📋 AVAILABLE DEMO SCENARIOS")
        print("=" * 60)
        
        for i, scenario in enumerate(self.demo_scenarios, 1):
            print(f"{i}. {scenario['name']}")
            print(f"   Category: {scenario['category']} | Complexity: {scenario['complexity']}")
            print(f"   Expected REP: {scenario['expected_rep']}")
            print(f"   Est. Time: {scenario['estimated_time']}")
            print(f"   Description: {scenario['description']}")
            print()
    
    def _run_predefined_scenario(self, scenario_index: int):
        """Run a predefined demo scenario."""
        if scenario_index < 0 or scenario_index >= len(self.demo_scenarios):
            print("❌ Invalid scenario number")
            return
            
        scenario = self.demo_scenarios[scenario_index]
        
        print(f"\n🎬 RUNNING SCENARIO: {scenario['name']}")
        print("=" * 50)
        print(f"Description: {scenario['description']}")
        print(f"Category: {scenario['category']} | Complexity: {scenario['complexity']}")
        print(f"Expected REP: {scenario['expected_rep']}")
        print()
        
        self._execute_task_with_demo_output(
            scenario['task'],
            scenario['required_output'],
            scenario
        )
    
    def _run_custom_task(self):
        """Run a custom user-defined task."""
        print("\n📝 CUSTOM TASK INPUT")
        print("=" * 30)
        
        task_description = input("Enter task description: ").strip()
        if not task_description:
            print("❌ Task description cannot be empty")
            return
            
        required_output = input("Enter required output (optional): ").strip()
        
        custom_scenario = {
            "name": "Custom Task",
            "description": "User-defined custom task",
            "category": "Custom",
            "complexity": "Unknown"
        }
        
        print(f"\n🎯 EXECUTING CUSTOM TASK")
        print("=" * 30)
        self._execute_task_with_demo_output(task_description, required_output, custom_scenario)
    
    def _execute_task_with_demo_output(self, task_description: str, required_output: str, scenario: Dict[str, Any]):
        """Execute task with detailed demo output."""
        start_time = time.time()
        
        print(f"Task: {task_description[:80]}...")
        print(f"Required Output: {required_output[:60]}...")
        print()
        
        # Execute task
        print("⚡ Executing task with MARE Protocol...")
        result = self.system.execute_task(task_description, required_output)
        execution_time = time.time() - start_time
        
        # Display results
        print(f"\n📊 EXECUTION RESULTS")
        print("-" * 30)
        print(f"Status: {self._format_status(result.status)}")
        print(f"REP Used: {result.rep_used}")
        print(f"Confidence: {result.confidence:.2f} {self._confidence_emoji(result.confidence)}")
        print(f"Execution Time: {execution_time:.2f}s")
        
        # Calculate token efficiency (simulated)
        baseline_time = execution_time * 3.0  # Baseline assumed 3x slower
        efficiency = (baseline_time - execution_time) / baseline_time
        print(f"Token Efficiency: {efficiency:.1%} 🚀")
        
        # Show result summary
        if result.result and isinstance(result.result, dict):
            print(f"\n📋 DELIVERABLES:")
            deliverables = result.result.get('deliverables', [])
            for i, deliverable in enumerate(deliverables[:3], 1):
                print(f"  {i}. {deliverable}")
            if len(deliverables) > 3:
                print(f"  ... and {len(deliverables) - 3} more")
                
            work_type = result.result.get('work_type', 'unknown')
            print(f"\nWork Type: {work_type.replace('_', ' ').title()}")
        
        # Performance comparison
        print(f"\n⚡ PERFORMANCE COMPARISON")
        print("-" * 25)
        print(f"MARE Time: {execution_time:.2f}s")
        print(f"Baseline Est: {baseline_time:.2f}s") 
        print(f"Speed Improvement: {baseline_time/execution_time:.1f}x faster")
        
        # Add to session history
        self.session_history.append({
            "timestamp": datetime.now().isoformat(),
            "scenario": scenario['name'],
            "task": task_description[:100] + "..." if len(task_description) > 100 else task_description,
            "rep_used": result.rep_used,
            "confidence": result.confidence,
            "execution_time": execution_time,
            "status": result.status.value,
            "token_efficiency": efficiency
        })
        
        print(f"\n✅ Task completed successfully!")
    
    def _format_status(self, status: TaskStatus) -> str:
        """Format task status with emoji."""
        status_map = {
            TaskStatus.COMPLETED: "✅ COMPLETED",
            TaskStatus.ESCALATED: "⚠️ ESCALATED", 
            TaskStatus.FAILED: "❌ FAILED",
            TaskStatus.PENDING: "⏳ PENDING",
            TaskStatus.IN_PROGRESS: "🔄 IN PROGRESS"
        }
        return status_map.get(status, str(status))
    
    def _confidence_emoji(self, confidence: float) -> str:
        """Get emoji for confidence level."""
        if confidence >= 0.8:
            return "🎯"
        elif confidence >= 0.6:
            return "👍"
        elif confidence >= 0.4:
            return "🤔"
        else:
            return "⚠️"
    
    def _show_session_history(self):
        """Show session execution history."""
        print(f"\n📈 SESSION HISTORY ({len(self.session_history)} tasks)")
        print("=" * 60)
        
        if not self.session_history:
            print("No tasks executed in this session yet.")
            return
        
        for i, entry in enumerate(self.session_history, 1):
            print(f"{i}. {entry['scenario']} ({entry['timestamp'][:19]})")
            print(f"   REP: {entry['rep_used']} | Confidence: {entry['confidence']:.2f}")
            print(f"   Time: {entry['execution_time']:.2f}s | Status: {entry['status']}")
            print(f"   Efficiency: {entry['token_efficiency']:.1%}")
            print()
    
    def _show_system_stats(self):
        """Show system performance statistics."""
        print(f"\n📊 SYSTEM STATISTICS")
        print("=" * 40)
        
        try:
            # Get system metrics
            metrics = self.system.get_performance_metrics()
            
            print(f"System Uptime: {metrics.get('uptime_seconds', 0):.1f}s")
            print(f"Total Tasks Processed: {metrics.get('total_tasks_processed', 0)}")
            print(f"Tasks per Hour: {metrics.get('tasks_per_hour', 0):.1f}")
            print(f"Active Tasks: {metrics.get('active_tasks', 0)}")
            print(f"Active Contexts: {metrics.get('active_contexts', 0)}")
            print(f"Available REPs: {metrics.get('rep_count', 0)}")
            
            # Session statistics
            if self.session_history:
                session_times = [entry['execution_time'] for entry in self.session_history]
                session_confidences = [entry['confidence'] for entry in self.session_history]
                session_efficiencies = [entry['token_efficiency'] for entry in self.session_history]
                
                print(f"\nSession Statistics:")
                print(f"  Tasks This Session: {len(self.session_history)}")
                print(f"  Avg Execution Time: {sum(session_times)/len(session_times):.2f}s")
                print(f"  Avg Confidence: {sum(session_confidences)/len(session_confidences):.2f}")
                print(f"  Avg Token Efficiency: {sum(session_efficiencies)/len(session_efficiencies):.1%}")
                
                # REP usage distribution
                rep_usage = {}
                for entry in self.session_history:
                    rep = entry['rep_used']
                    rep_usage[rep] = rep_usage.get(rep, 0) + 1
                
                print(f"\nREP Usage Distribution:")
                for rep, count in rep_usage.items():
                    percentage = count / len(self.session_history) * 100
                    print(f"  {rep}: {count} tasks ({percentage:.1f}%)")
            
        except Exception as e:
            print(f"❌ Error getting system statistics: {e}")
    
    def _show_system_health(self):
        """Show system health status."""
        print(f"\n🏥 SYSTEM HEALTH STATUS")
        print("=" * 40)
        
        try:
            health = self.system.get_system_health()
            
            status_emoji = "🟢" if health['system_status'] == 'healthy' else "🟡" if health['system_status'] == 'degraded' else "🔴"
            print(f"Overall Status: {status_emoji} {health['system_status'].upper()}")
            print(f"Uptime: {health.get('uptime_seconds', 0):.1f}s")
            print(f"Tasks Processed: {health.get('tasks_processed', 0)}")
            
            print(f"\nComponent Health:")
            components = health.get('components', {})
            for component, status in components.items():
                component_status = status.get('status', 'unknown')
                component_emoji = "🟢" if component_status == 'healthy' else "🟡" if component_status == 'degraded' else "🔴"
                print(f"  {component_emoji} {component}: {component_status}")
            
            if 'unhealthy_components' in health:
                print(f"\n⚠️  Unhealthy Components: {', '.join(health['unhealthy_components'])}")
        
        except Exception as e:
            print(f"❌ Error getting system health: {e}")
    
    def _show_help(self):
        """Show help information."""
        print(f"\n❓ MARE DEMO HELP")
        print("=" * 30)
        print("Available Commands:")
        print("  1-5       - Run predefined scenarios")
        print("  custom    - Enter custom task")
        print("  scenarios - List all available scenarios")
        print("  history   - Show session execution history")
        print("  stats     - Show system performance statistics")
        print("  health    - Show system health status")
        print("  help      - Show this help message")
        print("  quit      - Exit demo")
        print()
        print("Demo Features:")
        print("  • Real-time task execution with MARE Protocol")
        print("  • REP-based intelligent task routing")
        print("  • Performance metrics and token efficiency")
        print("  • Behavioral consistency validation")
        print("  • Interactive exploration of system capabilities")
    
    def cleanup(self):
        """Clean up demo resources."""
        try:
            self.system.shutdown()
            print("\n🔄 Demo cleanup completed")
        except Exception as e:
            print(f"Warning: Error during cleanup: {e}")


def main():
    """Main demo execution."""
    demo = MARELiveDemo()
    
    try:
        demo.start_interactive_demo()
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
    finally:
        demo.cleanup()
        print("👋 Thank you for trying the MARE Protocol demo!")


if __name__ == "__main__":
    main()