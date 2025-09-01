#!/usr/bin/env python3
"""
MARE Bootstrap Router - Routes tasks to appropriate REPs for self-construction
"""
import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass 
class Task:
    id: str
    description: str
    input_context: str
    required_output: str
    assigned_rep: Optional[str] = None

@dataclass
class REPDefinition:
    name: str
    filepath: str
    domain_expertise: Dict
    archetype: str

class MARERouter:
    def __init__(self, rep_directory: str = "."):
        self.rep_directory = Path(rep_directory)
        self.reps = self._load_reps()
        self.routing_rules = self._build_routing_rules()
    
    def _load_reps(self) -> Dict[str, REPDefinition]:
        """Load all REP definitions from directory"""
        reps = {}
        for rep_file in self.rep_directory.glob("*_rep.json"):
            with open(rep_file, 'r') as f:
                rep_data = json.load(f)
                reps[rep_data['name']] = REPDefinition(
                    name=rep_data['name'],
                    filepath=str(rep_file),
                    domain_expertise=rep_data.get('domain_expertise', {}),
                    archetype=rep_data['archetype']
                )
        return reps
    
    def _build_routing_rules(self) -> Dict[str, str]:
        """Define routing patterns for MARE self-construction tasks"""
        return {
            # Architecture and Design
            r".*architecture.*|.*design.*|.*component.*|.*system.*": "SOFTWARE_ARCHITECT_REP",
            r".*spec.*|.*diagram.*|.*interface.*": "SOFTWARE_ARCHITECT_REP",
            
            # Implementation
            r".*implement.*|.*code.*|.*develop.*|.*build.*": "BACKEND_DEVELOPER_REP", 
            r".*router.*|.*runner.*|.*injector.*": "BACKEND_DEVELOPER_REP",
            r".*mcp.*|.*integration.*": "BACKEND_DEVELOPER_REP",
            
            # Protocol Compliance
            r".*protocol.*|.*compliance.*|.*rfc.*|.*standard.*": "PROTOCOL_DESIGNER_REP",
            r".*validate.*|.*specification.*|.*schema.*": "PROTOCOL_DESIGNER_REP",
            
            # Testing and Validation  
            r".*test.*|.*demo.*|.*validation.*|.*proof.*": "TEST_ENGINEER_REP",
            r".*scenario.*|.*metric.*|.*measure.*": "TEST_ENGINEER_REP",
            
            # Deployment and Operations
            r".*deploy.*|.*setup.*|.*run.*|.*demo.*ready.*": "DEVOPS_ENGINEER_REP",
            r".*performance.*|.*monitoring.*|.*operational.*": "DEVOPS_ENGINEER_REP"
        }
    
    def route_task(self, task: Task) -> str:
        """Route a task to the appropriate REP based on content analysis"""
        task_text = f"{task.description} {task.required_output}".lower()
        
        for pattern, rep_name in self.routing_rules.items():
            if re.search(pattern, task_text):
                task.assigned_rep = rep_name
                return rep_name
                
        # Default fallback
        return "SOFTWARE_ARCHITECT_REP"
    
    def decompose_project(self, project_description: str) -> List[Task]:
        """Decompose the MARE bootstrap project into specific tasks"""
        tasks = [
            Task(
                id="arch_design",
                description="Design MARE system architecture with component specifications",
                input_context="MARE RFC specification + MVP requirements",
                required_output="Complete system architecture, component specs, data flow diagrams"
            ),
            Task(
                id="core_implementation", 
                description="Implement and build MARE core components: router, REP injector, runner agent",
                input_context="Architecture specifications + REP schema definitions",
                required_output="Working Python implementation with MCP integrations"
            ),
            Task(
                id="protocol_validation",
                description="Validate protocol compliance with MARE RFC specification", 
                input_context="MARE RFC + implemented system code",
                required_output="Compliance checklist, gap analysis, recommendations"
            ),
            Task(
                id="test_scenarios",
                description="Create demo scenarios and validation tests for token efficiency",
                input_context="Working MARE system + performance requirements", 
                required_output="Test scenarios, validation scripts, metrics dashboard"
            ),
            Task(
                id="deployment_setup",
                description="Deploy and setup system with live demo capability",
                input_context="Tested MARE implementation + demo requirements",
                required_output="Running system, demo script, performance metrics"
            )
        ]
        
        # Route each task
        for task in tasks:
            self.route_task(task)
            
        return tasks
    
    def generate_execution_plan(self, tasks: List[Task]) -> Dict[str, List[Task]]:
        """Generate execution plan grouped by REP"""
        execution_plan = {}
        for task in tasks:
            rep = task.assigned_rep
            if rep not in execution_plan:
                execution_plan[rep] = []
            execution_plan[rep].append(task)
            
        return execution_plan

# Bootstrap execution
if __name__ == "__main__":
    router = MARERouter()
    project_tasks = router.decompose_project("Build MARE MVP with self-construction proof")
    execution_plan = router.generate_execution_plan(project_tasks)
    
    print("MARE Bootstrap Execution Plan:")
    print("=" * 50)
    for rep, tasks in execution_plan.items():
        print(f"\n{rep}:")
        for task in tasks:
            print(f"  - {task.id}: {task.description}")
            print(f"    Output: {task.required_output}")
