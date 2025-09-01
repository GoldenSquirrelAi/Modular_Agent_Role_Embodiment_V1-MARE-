# MARE System Architecture Specification

**Author:** Software Architect REP  
**Version:** 1.0.0  
**Date:** September 1, 2025

---

## Executive Summary

This document defines the complete system architecture for a MARE (Modular Agent Role Embodiment) Protocol-compliant implementation. The architecture separates concerns between task orchestration (MAP) and execution identity (REP) to achieve 80%+ token efficiency and linear scalability.

---

## 1. System Overview

### 1.1 Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    MARE SYSTEM                              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐ │
│  │    MAP      │    │    REP       │    │      MCP        │ │
│  │  ROUTER     │◄──►│  REPOSITORY  │    │  INTEGRATION    │ │
│  │             │    │              │    │                 │ │
│  └─────────────┘    └──────────────┘    └─────────────────┘ │
│         │                    │                     │        │
│         ▼                    ▼                     ▼        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              RUNNER AGENT                               │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐│ │
│  │  │   TASK      │  │    REP       │  │    EXECUTION    ││ │
│  │  │ PROCESSOR   │  │  INJECTOR    │  │    CONTEXT      ││ │
│  │  └─────────────┘  └──────────────┘  └─────────────────┘│ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow Architecture

```
INPUT TASK
    │
    ▼
┌─────────────┐
│ MAP Router  │ ── Decomposes and routes tasks
│             │
└─────────────┘
    │
    ▼
┌─────────────┐
│ REP Repo    │ ── Retrieves role profile
│             │
└─────────────┘
    │
    ▼
┌─────────────┐
│ REP         │ ── Injects role behavior
│ Injector    │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Runner      │ ── Executes with embodied role
│ Agent       │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Context     │ ── Clears role state
│ Wiper       │
└─────────────┘
    │
    ▼
OUTPUT RESULT
```

---

## 2. Component Specifications

### 2.1 MAP Router

**Responsibility:** Task decomposition, REP selection, and execution orchestration

**Interface:**
```python
class MAPRouter:
    def decompose_task(self, task: Task) -> List[SubTask]
    def select_rep(self, task_context: Dict) -> REPProfile
    def route_execution(self, task: Task, rep: REPProfile) -> ExecutionPlan
    def handle_escalation(self, context: ExecutionContext) -> EscalationResponse
```

**Key Features:**
- Pattern-based task classification
- Dependency mapping and execution ordering  
- Fallback and escalation handling
- Health monitoring and redundancy support

**Failure Modes & Mitigations:**
- Router unavailable → Fallback router instances
- REP not found → Default generalist REP
- Task decomposition failure → Atomic task execution

### 2.2 REP Repository

**Responsibility:** Store, version, and serve Role Embodiment Profiles

**Interface:**
```python
class REPRepository:
    def get_rep(self, name: str, version: str = "latest") -> REPProfile
    def validate_rep(self, rep: REPProfile) -> ValidationResult
    def store_rep(self, rep: REPProfile) -> StorageResult
    def list_reps(self, filters: Dict = None) -> List[REPProfile]
```

**Storage Schema:**
```
reps/
├── {rep_name}/
│   ├── {version}/
│   │   ├── profile.json
│   │   ├── metadata.json
│   │   └── constraints.schema
│   └── latest -> {version}
└── index.json
```

**Key Features:**
- Semantic versioning with rollback
- Schema validation and constraint enforcement
- Caching layer for performance
- Audit trail for all modifications

### 2.3 REP Injector

**Responsibility:** Apply role behavior to Runner Agent context

**Interface:**
```python
class REPInjector:
    def inject_role(self, agent_context: AgentContext, rep: REPProfile) -> InjectedContext
    def validate_injection(self, context: InjectedContext) -> bool
    def extract_constraints(self, rep: REPProfile) -> List[Constraint]
```

**Injection Process:**
1. Parse REP system_prompt and constraints
2. Apply tone_guide formatting preferences  
3. Set tool access permissions
4. Configure confidence thresholds
5. Initialize execution context isolation

### 2.4 Runner Agent

**Responsibility:** Execute tasks with injected role behavior

**Interface:**
```python
class RunnerAgent:
    def initialize_context(self, rep: REPProfile) -> ExecutionContext
    def execute_task(self, task: Task, context: ExecutionContext) -> TaskResult
    def evaluate_confidence(self, result: TaskResult) -> ConfidenceScore
    def handle_escalation(self, task: Task, reason: str) -> EscalationResult
    def wipe_context(self) -> None
```

**Context Isolation:**
- Role state isolated between executions
- Tool permissions scoped per REP
- Memory boundaries enforced
- Audit logging for all actions

### 2.5 MCP Integration Layer

**Responsibility:** Standardized tool access with REP-based permissions

**Interface:**
```python
class MCPIntegration:
    def get_available_tools(self, rep_permissions: Dict) -> List[Tool]
    def execute_tool(self, tool: str, args: Dict, context: ExecutionContext) -> ToolResult
    def validate_permission(self, tool: str, rep: REPProfile) -> bool
```

**Tool Categories:**
- File system operations
- API integrations  
- Database access
- External services
- Specialized domain tools

---

## 3. Technology Stack

### 3.1 Core Implementation

**Language:** Python 3.9+
- **Rationale:** Excellent AI/ML ecosystem, mature async support
- **Key Libraries:** 
  - `asyncio` for concurrent execution
  - `pydantic` for schema validation
  - `fastapi` for API services
  - `sqlalchemy` for data persistence

### 3.2 Storage Systems

**REP Repository:** SQLite with JSON columns
- **Rationale:** Embedded, zero-config, excellent JSON support
- **Scaling Path:** PostgreSQL for multi-instance deployments

**Caching:** Redis
- **Rationale:** Fast REP retrieval, session state management
- **Fallback:** In-memory LRU cache

### 3.3 Integration Interfaces

**MCP Protocol:** HTTP/WebSocket
- **Tool Discovery:** REST endpoints
- **Tool Execution:** WebSocket for streaming

**Monitoring:** Structured logging + metrics
- **Logging:** JSON format with correlation IDs
- **Metrics:** Prometheus-compatible

---

## 4. Scalability Design

### 4.1 Horizontal Scaling

```
Load Balancer
    │
    ├── MAP Router Instance 1
    ├── MAP Router Instance 2  
    └── MAP Router Instance N
              │
              ▼
    Shared REP Repository
              │
              ▼
    Runner Agent Pool
```

**Scaling Characteristics:**
- Stateless routers enable linear scaling
- REP repository shared across instances
- Runner agents can be containerized
- No cross-instance coordination required

### 4.2 Performance Targets

- **Router Latency:** <100ms task decomposition
- **REP Retrieval:** <50ms with caching
- **Context Injection:** <20ms role application  
- **Concurrent Tasks:** 1000+ with proper resource allocation

---

## 5. Security Architecture

### 5.1 REP Security

```
┌─────────────────────────────────────┐
│          REP SECURITY               │
├─────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────┐│
│  │   SCHEMA    │  │   PERMISSION    ││
│  │ VALIDATION  │  │   BOUNDARY      ││
│  └─────────────┘  └─────────────────┘│
│  ┌─────────────┐  ┌─────────────────┐│
│  │    AUDIT    │  │   ENCRYPTION    ││
│  │  LOGGING    │  │    AT REST      ││
│  └─────────────┘  └─────────────────┘│
└─────────────────────────────────────┘
```

**Key Security Measures:**
- REP profiles encrypted at rest (AES-256)
- Tool access strictly scoped by REP permissions
- All actions logged with REP attribution
- Context isolation prevents data leakage
- Schema validation prevents malicious REPs

### 5.2 Runtime Security

- Process-level isolation for Runner Agents
- Network segmentation for tool access
- Rate limiting per REP type
- Execution timeouts with forced termination

---

## 6. Failure Handling Strategy

### 6.1 Failure Categories

| Failure Type | Detection | Mitigation | Recovery |
|--------------|-----------|------------|----------|
| Router Down | Health check | Failover router | Automatic |
| REP Not Found | 404 response | Default REP | Manual override |
| Tool Unavailable | Timeout/Error | Skip/Alternative | Retry/Escalate |
| Context Corruption | Validation | Fresh injection | Restart agent |
| Performance Degradation | Metrics | Load balancing | Scale out |

### 6.2 Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int, timeout: int):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
```

Applied to:
- REP repository access
- Tool execution calls  
- External API integrations

---

## 7. Monitoring and Observability

### 7.1 Key Metrics

**Router Metrics:**
- Task decomposition latency
- REP selection accuracy
- Routing success rate

**REP Metrics:**
- Injection success rate
- Execution completion rate
- Confidence score distribution

**System Metrics:**
- Token consumption per task
- Memory usage per agent
- Concurrent execution count

### 7.2 Alerting Strategy

**Critical Alerts:**
- Router unavailable (>1 minute)
- REP repository corruption
- Security policy violations
- Performance below SLA

**Warning Alerts:**
- High error rates (>5%)
- Resource utilization (>80%)
- Unusual confidence patterns

---

## 8. Implementation Phases

### Phase 1: Core MVP (4 weeks)
- Basic MAP router with pattern matching
- File-based REP repository
- Simple REP injection
- Single Runner Agent instance
- Basic MCP integration

### Phase 2: Production Features (6 weeks)
- Database-backed REP repository  
- Context isolation and security
- Health checks and failover
- Comprehensive logging
- Performance optimization

### Phase 3: Advanced Features (8 weeks)
- Horizontal scaling support
- Advanced routing algorithms
- REP inheritance and templating
- Real-time monitoring dashboard
- Compliance reporting

---

## 9. Success Criteria

### Functional Requirements
- [ ] Route tasks to appropriate REPs based on content analysis
- [ ] Successfully inject role behavior into Runner Agents  
- [ ] Execute tasks with consistent role-specific behavior
- [ ] Achieve context isolation between REP embodiments
- [ ] Support all required MCP tool integrations

### Performance Requirements
- [ ] 80%+ token efficiency vs baseline multi-agent systems
- [ ] <2s latency for routine tasks
- [ ] <30s latency for complex workflows
- [ ] 99.9% task completion rate
- [ ] Linear scalability to 1000+ concurrent tasks

### Security Requirements
- [ ] REP profiles encrypted at rest
- [ ] Tool access scoped per REP permissions
- [ ] Complete audit trail for all actions
- [ ] Context isolation prevents data leakage
- [ ] Schema validation blocks malicious REPs

---

## 10. Conclusion

This architecture provides a robust, scalable foundation for MARE Protocol implementation. The separation of orchestration (MAP) and execution identity (REP) enables efficient resource utilization while maintaining behavioral consistency and security.

The modular design allows for incremental development and deployment, with clear upgrade paths as requirements evolve. Key architectural decisions prioritize simplicity, maintainability, and performance while ensuring compliance with RFC specifications.

**Next Steps:** Proceed to implementation phase with Backend Developer REP embodiment.

---

*Architecture designed by SOFTWARE_ARCHITECT_REP v1.0.0*