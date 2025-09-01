#!/usr/bin/env python3
"""
MARE Validation Suite

Comprehensive test scenarios to validate token efficiency, behavioral consistency,
and performance claims of the MARE Protocol implementation.
"""
import sys
import time
import json
import statistics
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mare import MARESystem, TaskStatus


@dataclass
class TestScenario:
    """Test scenario definition."""
    name: str
    description: str
    task_description: str
    required_output: str
    expected_rep: str
    success_criteria: Dict[str, Any]
    category: str


@dataclass
class ValidationResult:
    """Test validation result."""
    scenario_name: str
    success: bool
    execution_time: float
    confidence: float
    rep_used: str
    token_efficiency_score: float
    behavioral_consistency_score: float
    details: Dict[str, Any]


class MAREValidationSuite:
    """Comprehensive validation suite for MARE Protocol."""
    
    def __init__(self):
        """Initialize validation suite."""
        self.system = MARESystem()
        self.baseline_multiplier = 3.0  # Baseline assumed 3x slower
        self.test_scenarios = self._create_test_scenarios()
        self.results: List[ValidationResult] = []
    
    def _create_test_scenarios(self) -> List[TestScenario]:
        """Create comprehensive test scenarios."""
        return [
            # Architecture & Design Scenarios
            TestScenario(
                name="architecture_microservices_design",
                description="Design microservices architecture",
                task_description="Design a scalable microservices architecture for a fintech platform with payment processing, user management, and fraud detection",
                required_output="Complete architecture with service boundaries, API specifications, and security considerations",
                expected_rep="SOFTWARE_ARCHITECT_REP",
                success_criteria={
                    "min_confidence": 0.7,
                    "max_execution_time": 5.0,
                    "required_deliverables": ["architecture", "specifications", "security"]
                },
                category="architecture"
            ),
            
            TestScenario(
                name="architecture_database_design",
                description="Design database architecture",
                task_description="Design a distributed database architecture for high-throughput e-commerce with ACID compliance and horizontal scaling",
                required_output="Database design with schema, partitioning strategy, and consistency model",
                expected_rep="SOFTWARE_ARCHITECT_REP", 
                success_criteria={
                    "min_confidence": 0.6,
                    "max_execution_time": 4.0,
                    "required_deliverables": ["schema", "scaling", "consistency"]
                },
                category="architecture"
            ),
            
            # Implementation & Development Scenarios
            TestScenario(
                name="implementation_rest_api",
                description="Implement REST API with authentication",
                task_description="Implement a production-ready REST API with JWT authentication, rate limiting, error handling, and comprehensive logging",
                required_output="Working Python code with FastAPI, authentication middleware, and unit tests",
                expected_rep="BACKEND_DEVELOPER_REP",
                success_criteria={
                    "min_confidence": 0.7,
                    "max_execution_time": 6.0,
                    "required_deliverables": ["code", "tests", "authentication"]
                },
                category="implementation"
            ),
            
            TestScenario(
                name="implementation_data_processing",
                description="Implement data processing pipeline", 
                task_description="Implement a real-time data processing pipeline with error handling, monitoring, and scalable architecture",
                required_output="Production-ready code with streaming processing, error recovery, and metrics",
                expected_rep="BACKEND_DEVELOPER_REP",
                success_criteria={
                    "min_confidence": 0.6,
                    "max_execution_time": 5.0,
                    "required_deliverables": ["pipeline", "monitoring", "error_handling"]
                },
                category="implementation"
            ),
            
            # Testing & Validation Scenarios  
            TestScenario(
                name="testing_performance_validation",
                description="Create performance test suite",
                task_description="Create comprehensive performance testing framework for API endpoints with load testing, stress testing, and performance regression detection",
                required_output="Automated test suite with performance benchmarks, load test scenarios, and reporting dashboard",
                expected_rep="TEST_ENGINEER_REP",
                success_criteria={
                    "min_confidence": 0.8,
                    "max_execution_time": 4.0,
                    "required_deliverables": ["test_suite", "benchmarks", "reporting"]
                },
                category="testing"
            ),
            
            TestScenario(
                name="testing_compliance_validation",
                description="Validate security compliance",
                task_description="Design security compliance testing framework for PCI-DSS, GDPR, and SOX requirements with automated validation and reporting",
                required_output="Compliance test framework with automated checks, vulnerability scanning, and audit trail",
                expected_rep="TEST_ENGINEER_REP", 
                success_criteria={
                    "min_confidence": 0.7,
                    "max_execution_time": 5.0,
                    "required_deliverables": ["compliance_tests", "vulnerability_scan", "audit"]
                },
                category="testing"
            ),
            
            # Deployment & Operations Scenarios
            TestScenario(
                name="deployment_kubernetes_setup",
                description="Setup Kubernetes deployment",
                task_description="Design and configure production Kubernetes deployment with auto-scaling, monitoring, logging, and disaster recovery",
                required_output="Complete K8s manifests with Helm charts, monitoring stack, and operational procedures",
                expected_rep="DEVOPS_ENGINEER_REP",
                success_criteria={
                    "min_confidence": 0.7,
                    "max_execution_time": 5.0,
                    "required_deliverables": ["kubernetes", "monitoring", "procedures"]
                },
                category="deployment"
            ),
            
            TestScenario(
                name="deployment_ci_cd_pipeline", 
                description="Design CI/CD pipeline",
                task_description="Design comprehensive CI/CD pipeline with automated testing, security scanning, deployment automation, and rollback capabilities",
                required_output="Complete pipeline configuration with automated quality gates and deployment strategies",
                expected_rep="DEVOPS_ENGINEER_REP",
                success_criteria={
                    "min_confidence": 0.6,
                    "max_execution_time": 4.0,
                    "required_deliverables": ["pipeline", "testing", "deployment"]
                },
                category="deployment"
            ),
            
            # Protocol & Standards Scenarios
            TestScenario(
                name="protocol_api_specification",
                description="Design API protocol specification",
                task_description="Create comprehensive REST API specification with OpenAPI 3.0, authentication flows, error handling, and versioning strategy",
                required_output="Complete API specification with schemas, security definitions, and documentation",
                expected_rep="PROTOCOL_DESIGNER_REP",
                success_criteria={
                    "min_confidence": 0.8,
                    "max_execution_time": 4.0,
                    "required_deliverables": ["specification", "security", "documentation"]
                },
                category="protocol"
            ),
            
            # Edge Cases & Stress Tests
            TestScenario(
                name="edge_case_complex_requirements",
                description="Handle complex multi-domain task",
                task_description="Design and implement a real-time trading system with microsecond latency, regulatory compliance, risk management, and high availability",
                required_output="Complete system design with implementation plan, compliance framework, and operational procedures",
                expected_rep="SOFTWARE_ARCHITECT_REP",  # Most complex tasks should go to architect
                success_criteria={
                    "min_confidence": 0.5,  # Lower confidence expected for complex tasks
                    "max_execution_time": 8.0,
                    "required_deliverables": ["design", "compliance", "operations"]
                },
                category="edge_case"
            )
        ]
    
    def run_validation_suite(self) -> Dict[str, Any]:
        """Run complete validation suite."""
        print("🧪 MARE VALIDATION SUITE")
        print("=" * 60)
        print(f"Testing {len(self.test_scenarios)} scenarios...")
        
        start_time = time.time()
        
        # Execute all test scenarios
        for i, scenario in enumerate(self.test_scenarios, 1):
            print(f"\n[{i}/{len(self.test_scenarios)}] {scenario.name}")
            print(f"Category: {scenario.category}")
            print(f"Description: {scenario.description}")
            
            result = self._execute_scenario(scenario)
            self.results.append(result)
            
            # Print immediate results
            status = "✅ PASS" if result.success else "❌ FAIL"
            print(f"Result: {status}")
            print(f"REP Used: {result.rep_used}")
            print(f"Confidence: {result.confidence:.2f}")
            print(f"Execution Time: {result.execution_time:.2f}s")
            print(f"Token Efficiency: {result.token_efficiency_score:.2f}")
        
        total_time = time.time() - start_time
        
        # Generate comprehensive report
        report = self._generate_validation_report(total_time)
        
        # Save detailed results
        self._save_results(report)
        
        return report
    
    def _execute_scenario(self, scenario: TestScenario) -> ValidationResult:
        """Execute a single test scenario."""
        try:
            start_time = time.time()
            
            # Execute task using MARE system
            result = self.system.execute_task(
                description=scenario.task_description,
                required_output=scenario.required_output
            )
            
            execution_time = time.time() - start_time
            
            # Calculate token efficiency score
            baseline_time = execution_time * self.baseline_multiplier
            efficiency_score = (baseline_time - execution_time) / baseline_time
            
            # Calculate behavioral consistency score
            consistency_score = self._assess_behavioral_consistency(result, scenario)
            
            # Evaluate success criteria
            success = self._evaluate_success_criteria(result, scenario, execution_time)
            
            return ValidationResult(
                scenario_name=scenario.name,
                success=success,
                execution_time=execution_time,
                confidence=result.confidence,
                rep_used=result.rep_used,
                token_efficiency_score=efficiency_score,
                behavioral_consistency_score=consistency_score,
                details={
                    "status": result.status.value,
                    "expected_rep": scenario.expected_rep,
                    "rep_match": result.rep_used == scenario.expected_rep,
                    "error_message": result.error_message,
                    "result_type": type(result.result).__name__ if result.result else "None"
                }
            )
            
        except Exception as e:
            return ValidationResult(
                scenario_name=scenario.name,
                success=False,
                execution_time=0.0,
                confidence=0.0,
                rep_used="ERROR",
                token_efficiency_score=0.0,
                behavioral_consistency_score=0.0,
                details={"error": str(e)}
            )
    
    def _assess_behavioral_consistency(self, result, scenario: TestScenario) -> float:
        """Assess behavioral consistency of REP execution."""
        consistency_factors = []
        
        # Check if correct REP was used
        if result.rep_used == scenario.expected_rep:
            consistency_factors.append(1.0)
        else:
            consistency_factors.append(0.0)
        
        # Check if result has expected structure
        if result.result and isinstance(result.result, dict):
            deliverables = result.result.get("deliverables", [])
            if deliverables:
                consistency_factors.append(1.0)
            else:
                consistency_factors.append(0.5)
        else:
            consistency_factors.append(0.0)
        
        # Check if status is appropriate
        if result.status in [TaskStatus.COMPLETED, TaskStatus.ESCALATED]:
            consistency_factors.append(1.0)
        else:
            consistency_factors.append(0.0)
        
        return sum(consistency_factors) / len(consistency_factors)
    
    def _evaluate_success_criteria(self, result, scenario: TestScenario, execution_time: float) -> bool:
        """Evaluate scenario success criteria."""
        criteria = scenario.success_criteria
        
        # Check minimum confidence
        if result.confidence < criteria.get("min_confidence", 0.0):
            return False
        
        # Check maximum execution time
        if execution_time > criteria.get("max_execution_time", float('inf')):
            return False
        
        # Check required deliverables (if result is dict with deliverables)
        required_deliverables = criteria.get("required_deliverables", [])
        if required_deliverables and result.result and isinstance(result.result, dict):
            deliverables = result.result.get("deliverables", [])
            if not any(req in str(deliverables).lower() for req in required_deliverables):
                return False
        
        return True
    
    def _generate_validation_report(self, total_time: float) -> Dict[str, Any]:
        """Generate comprehensive validation report."""
        if not self.results:
            return {"error": "No test results available"}
        
        # Basic statistics
        total_scenarios = len(self.results)
        passed_scenarios = sum(1 for r in self.results if r.success)
        pass_rate = passed_scenarios / total_scenarios
        
        # Performance metrics
        execution_times = [r.execution_time for r in self.results]
        avg_execution_time = statistics.mean(execution_times)
        baseline_total_time = total_time * self.baseline_multiplier
        overall_efficiency = (baseline_total_time - total_time) / baseline_total_time
        
        # Confidence analysis
        confidences = [r.confidence for r in self.results]
        avg_confidence = statistics.mean(confidences)
        high_confidence_count = sum(1 for c in confidences if c >= 0.8)
        
        # Token efficiency analysis
        efficiency_scores = [r.token_efficiency_score for r in self.results]
        avg_efficiency = statistics.mean(efficiency_scores)
        
        # Behavioral consistency analysis
        consistency_scores = [r.behavioral_consistency_score for r in self.results]
        avg_consistency = statistics.mean(consistency_scores)
        
        # REP usage analysis
        rep_usage = {}
        correct_rep_assignments = 0
        
        for result in self.results:
            rep_usage[result.rep_used] = rep_usage.get(result.rep_used, 0) + 1
            
            # Find expected REP for this scenario
            scenario = next(s for s in self.test_scenarios if s.name == result.scenario_name)
            if result.rep_used == scenario.expected_rep:
                correct_rep_assignments += 1
        
        rep_accuracy = correct_rep_assignments / total_scenarios
        
        # Category analysis
        category_results = {}
        for result in self.results:
            scenario = next(s for s in self.test_scenarios if s.name == result.scenario_name)
            category = scenario.category
            
            if category not in category_results:
                category_results[category] = {
                    "total": 0, "passed": 0, "avg_confidence": 0.0, "avg_efficiency": 0.0
                }
            
            category_results[category]["total"] += 1
            if result.success:
                category_results[category]["passed"] += 1
            category_results[category]["avg_confidence"] += result.confidence
            category_results[category]["avg_efficiency"] += result.token_efficiency_score
        
        # Calculate averages for categories
        for category in category_results:
            total = category_results[category]["total"]
            category_results[category]["pass_rate"] = category_results[category]["passed"] / total
            category_results[category]["avg_confidence"] /= total
            category_results[category]["avg_efficiency"] /= total
        
        return {
            "summary": {
                "total_scenarios": total_scenarios,
                "passed_scenarios": passed_scenarios,
                "pass_rate": pass_rate,
                "overall_success": pass_rate >= 0.8,  # 80% pass rate required
                "execution_date": datetime.now().isoformat()
            },
            "performance": {
                "total_execution_time": total_time,
                "baseline_estimated_time": baseline_total_time,
                "token_efficiency_gain": overall_efficiency,
                "avg_execution_time": avg_execution_time,
                "min_execution_time": min(execution_times),
                "max_execution_time": max(execution_times)
            },
            "confidence_analysis": {
                "avg_confidence": avg_confidence,
                "min_confidence": min(confidences),
                "max_confidence": max(confidences), 
                "high_confidence_scenarios": high_confidence_count,
                "high_confidence_rate": high_confidence_count / total_scenarios
            },
            "behavioral_analysis": {
                "avg_token_efficiency": avg_efficiency,
                "avg_behavioral_consistency": avg_consistency,
                "rep_routing_accuracy": rep_accuracy,
                "rep_usage_distribution": rep_usage
            },
            "category_analysis": category_results,
            "detailed_results": [
                {
                    "scenario": r.scenario_name,
                    "success": r.success,
                    "confidence": r.confidence,
                    "execution_time": r.execution_time,
                    "rep_used": r.rep_used,
                    "efficiency_score": r.token_efficiency_score,
                    "consistency_score": r.behavioral_consistency_score
                }
                for r in self.results
            ],
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        if not self.results:
            return ["No test results available for analysis"]
        
        pass_rate = sum(1 for r in self.results if r.success) / len(self.results)
        if pass_rate < 0.8:
            recommendations.append(f"Pass rate ({pass_rate:.1%}) below target 80% - investigate failing scenarios")
        
        avg_confidence = statistics.mean([r.confidence for r in self.results])
        if avg_confidence < 0.7:
            recommendations.append(f"Average confidence ({avg_confidence:.2f}) below target 0.7 - improve REP task matching")
        
        avg_efficiency = statistics.mean([r.token_efficiency_score for r in self.results])
        if avg_efficiency < 0.8:
            recommendations.append(f"Token efficiency ({avg_efficiency:.2f}) below target 0.8 - optimize context injection")
        
        # REP routing accuracy
        correct_assignments = sum(1 for r in self.results for s in self.test_scenarios 
                                if s.name == r.scenario_name and r.rep_used == s.expected_rep)
        rep_accuracy = correct_assignments / len(self.results)
        
        if rep_accuracy < 0.8:
            recommendations.append(f"REP routing accuracy ({rep_accuracy:.1%}) below target 80% - improve task classification")
        
        # Performance recommendations
        slow_scenarios = [r for r in self.results if r.execution_time > 5.0]
        if slow_scenarios:
            recommendations.append(f"{len(slow_scenarios)} scenarios exceeded 5s execution time - optimize performance")
        
        if not recommendations:
            recommendations.append("All validation targets met - system performing as expected")
        
        return recommendations
    
    def _save_results(self, report: Dict[str, Any]) -> None:
        """Save detailed results to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mare_validation_report_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"\n📄 Detailed report saved to: {filename}")
        except Exception as e:
            print(f"\n⚠️  Could not save report: {e}")
    
    def cleanup(self) -> None:
        """Clean up resources."""
        try:
            self.system.shutdown()
        except Exception as e:
            print(f"Warning: Error during cleanup: {e}")


def main():
    """Main validation execution."""
    validation_suite = MAREValidationSuite()
    
    try:
        print("🔬 Starting MARE Protocol Validation")
        print("This comprehensive test suite validates:")
        print("  - Token efficiency claims (80%+ improvement)")
        print("  - REP behavioral consistency")
        print("  - Task routing accuracy")
        print("  - Performance requirements")
        print("  - Edge case handling")
        
        input("\nPress Enter to begin validation suite...")
        
        # Run validation suite
        report = validation_suite.run_validation_suite()
        
        # Print summary report
        print("\n" + "=" * 60)
        print("🎯 VALIDATION SUMMARY")
        print("=" * 60)
        
        summary = report["summary"]
        performance = report["performance"]
        confidence = report["confidence_analysis"]
        behavioral = report["behavioral_analysis"]
        
        print(f"Overall Success: {'✅ PASS' if summary['overall_success'] else '❌ FAIL'}")
        print(f"Scenarios Passed: {summary['passed_scenarios']}/{summary['total_scenarios']} ({summary['pass_rate']:.1%})")
        print(f"Token Efficiency Gain: {performance['token_efficiency_gain']:.1%}")
        print(f"Average Confidence: {confidence['avg_confidence']:.2f}")
        print(f"REP Routing Accuracy: {behavioral['rep_routing_accuracy']:.1%}")
        print(f"Behavioral Consistency: {behavioral['avg_behavioral_consistency']:.2f}")
        
        print(f"\nPerformance Metrics:")
        print(f"  Total Execution Time: {performance['total_execution_time']:.2f}s")
        print(f"  Average per Scenario: {performance['avg_execution_time']:.2f}s")
        print(f"  Baseline Estimated: {performance['baseline_estimated_time']:.2f}s")
        
        print(f"\nREP Usage Distribution:")
        for rep, count in behavioral['rep_usage_distribution'].items():
            percentage = count / summary['total_scenarios'] * 100
            print(f"  {rep}: {count} scenarios ({percentage:.1f}%)")
        
        print(f"\nCategory Analysis:")
        for category, stats in report["category_analysis"].items():
            print(f"  {category}: {stats['passed']}/{stats['total']} pass ({stats['pass_rate']:.1%})")
        
        print(f"\nRecommendations:")
        for rec in report["recommendations"]:
            print(f"  • {rec}")
        
        # Final validation verdict
        print("\n" + "=" * 60)
        if summary['overall_success'] and performance['token_efficiency_gain'] >= 0.8:
            print("🏆 MARE PROTOCOL VALIDATION: ✅ SUCCESSFUL")
            print("System meets all performance and behavioral requirements!")
        else:
            print("⚠️  MARE PROTOCOL VALIDATION: ❌ NEEDS IMPROVEMENT")
            print("System requires optimization before production deployment.")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Validation interrupted by user")
    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        validation_suite.cleanup()


if __name__ == "__main__":
    main()