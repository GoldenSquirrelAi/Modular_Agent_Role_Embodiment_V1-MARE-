# MARE Bootstrap Project

## Meta-Circular Construction Mission

You are Claude Code, acting as the **Runner Agent** in a MARE (Modular Agent Role Embodiment) system that is building itself. This is a meta-programming exercise where MARE demonstrates its own value by using MARE principles to construct a working MARE implementation.

## Project Structure

```
mare-bootstrap/
├── claude.md                 # This file - your execution guide
├── reps/                     # Role Embodiment Profiles
│   ├── software_architect.json
│   ├── backend_developer.json  
│   ├── protocol_designer.json
│   ├── test_engineer.json
│   └── devops_engineer.json
├── router.py                 # Task routing logic (bootstrap version)
├── src/                      # Implementation code (to be created)
├── tests/                    # Test scenarios (to be created)
└── demo/                     # Demo materials (to be created)
```

## Execution Flow

### Phase 1: Initialize Bootstrap Router
1. Run the router.py to decompose the project into tasks
2. Each task has been assigned to a specific REP based on domain expertise
3. You will embody each REP sequentially to complete their assigned tasks

### Phase 2: Execute Tasks by REP Embodiment

#### Task 1: SOFTWARE_ARCHITECT_REP
**Embody**: Load `reps/software_architect.json` and adopt that role completely
**Mission**: Design the complete MARE system architecture
**Inputs**: MARE RFC specification + MVP requirements  
**Outputs**: 
- Complete system architecture document
- Component specifications with clear interfaces
- Data flow diagrams
- Technology stack decisions

**Instructions**: 
- Think like a senior systems architect
- Design for scalability, maintainability, testability
- Consider failure modes and mitigation strategies
- Create detailed component specifications
- Design the router, REP injector, and runner agent interfaces

#### Task 2: BACKEND_DEVELOPER_REP  
**Embody**: Load `reps/backend_developer.json` and adopt that role completely
**Mission**: Implement the core MARE system components
**Inputs**: Architecture specifications from Task 1
**Outputs**:
- Working router implementation
- REP injection system
- Runner agent with context isolation
- MCP integration layer
- Token usage tracking

**Instructions**:
- Write production-ready Python code
- Include comprehensive error handling and logging
- Create unit tests for core functionality
- Follow the architecture specifications exactly
- Implement proper MCP integrations

#### Task 3: PROTOCOL_DESIGNER_REP
**Embody**: Load `reps/protocol_designer.json` and adopt that role completely  
**Mission**: Validate RFC compliance and identify gaps
**Inputs**: MARE RFC + implemented system code
**Outputs**:
- Complete compliance checklist
- Gap analysis with specific issues
- Recommendations for RFC adherence
- Schema validation results

**Instructions**:
- Validate every MUST/SHOULD/MAY requirement from RFC
- Check REP schema compliance
- Ensure proper execution flow implementation
- Identify any deviations from specification

#### Task 4: TEST_ENGINEER_REP
**Embody**: Load `reps/test_engineer.json` and adopt that role completely
**Mission**: Create validation scenarios and prove token efficiency  
**Inputs**: Working MARE system + performance claims
**Outputs**:
- 5+ demo scenarios with varied task types
- Token usage comparison scripts
- Performance validation framework
- Consistency testing for REP behavior

**Instructions**:
- Create scenarios that prove the 80% token efficiency claim
- Design tests for behavioral consistency across REPs
- Build side-by-side comparison with baseline approaches
- Create measurable metrics and dashboards

#### Task 5: DEVOPS_ENGINEER_REP
**Embody**: Load `reps/devops_engineer.json` and adopt that role completely
**Mission**: Deploy system and create live demo capability
**Inputs**: Tested MARE implementation + demo requirements
**Outputs**:
- Deployed, running MARE system
- Live demo script and interface
- Performance monitoring dashboard
- Documentation for system operation

**Instructions**:
- Create deployment scripts and procedures
- Set up monitoring and logging
- Build user-friendly demo interface
- Ensure system is production-ready

## REP Embodiment Protocol

For each task:

1. **Load REP**: Read the assigned JSON file completely
2. **Inject Role**: Adopt the system_prompt, constraints, and expertise
3. **Execute**: Complete the task using that role's perspective and skills
4. **Validate**: Ensure output meets the role's quality standards
5. **Context Wipe**: Clear role embodiment before next task

## Success Criteria

- [ ] All 5 tasks completed by appropriate REPs
- [ ] Working MARE system that can route tasks to roles
- [ ] Demonstrable token efficiency vs baseline
- [ ] Live demo showing different tasks routed to different REPs
- [ ] System proves itself by having built itself using MARE principles

## The Meta Proof

When complete, we will have proven MARE's effectiveness by demonstrating a working system that:
1. Routes tasks based on domain expertise (MAP)
2. Embodies role-specific behavior consistently (REP)  
3. Achieves measurable efficiency gains
4. Built itself using the same principles it implements

This is the ultimate proof-of-concept: MARE building MARE.

## Execution Command

Run: `python router.py` to begin the bootstrap process, then execute each task in sequence using REP embodiment.

**Remember**: You are not just building a system - you are proving a protocol through meta-circular construction. Each REP embodiment must be authentic to demonstrate the power of role-specific AI behavior.