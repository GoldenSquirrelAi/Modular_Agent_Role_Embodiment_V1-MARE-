#!/bin/bash

# MARE System Deployment Script
# DevOps Engineer REP - Production Deployment Automation

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARE_VERSION="1.0.0"
DEPLOYMENT_ENV="${MARE_ENV:-production}"
LOG_LEVEL="${MARE_LOG_LEVEL:-INFO}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Banner
print_banner() {
    echo "=================================================================="
    echo "  🚀 MARE SYSTEM DEPLOYMENT"
    echo "  Modular Agent Role Embodiment Protocol"
    echo "  Version: $MARE_VERSION"
    echo "  Environment: $DEPLOYMENT_ENV"
    echo "=================================================================="
    echo ""
}

# Pre-deployment checks
check_prerequisites() {
    log_info "Checking deployment prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker daemon
    if ! docker ps &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    # Check required files
    required_files=("Dockerfile" "docker-compose.yml" "requirements.txt")
    for file in "${required_files[@]}"; do
        if [[ ! -f "$SCRIPT_DIR/$file" ]]; then
            log_error "Required file not found: $file"
            exit 1
        fi
    done
    
    log_success "Prerequisites check passed"
}

# Build MARE system image
build_image() {
    log_info "Building MARE system Docker image..."
    
    cd "$SCRIPT_DIR"
    
    # Build with build args
    docker build \
        --build-arg MARE_VERSION="$MARE_VERSION" \
        --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
        --tag "mare-protocol:$MARE_VERSION" \
        --tag "mare-protocol:latest" \
        .
    
    log_success "Docker image built successfully"
}

# Deploy services
deploy_services() {
    log_info "Deploying MARE system services..."
    
    cd "$SCRIPT_DIR"
    
    # Create necessary directories
    mkdir -p config monitoring/grafana
    
    # Set environment variables
    export MARE_VERSION
    export DEPLOYMENT_ENV
    export LOG_LEVEL
    
    # Deploy with Docker Compose
    docker-compose down --volumes 2>/dev/null || true
    docker-compose up -d
    
    log_success "Services deployed"
}

# Wait for services to be healthy
wait_for_health() {
    log_info "Waiting for services to become healthy..."
    
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        log_info "Health check attempt $attempt/$max_attempts"
        
        # Check MARE system health
        if docker-compose exec -T mare-system python3 -c "
import sys
sys.path.insert(0, '/app/src')
from mare import MARESystem
try:
    system = MARESystem()
    health = system.get_system_health()
    system.shutdown()
    exit(0 if health['system_status'] == 'healthy' else 1)
except Exception as e:
    print(f'Health check failed: {e}')
    exit(1)
" 2>/dev/null; then
            log_success "MARE system is healthy"
            break
        fi
        
        if [[ $attempt -eq $max_attempts ]]; then
            log_error "Services failed to become healthy within timeout"
            show_service_logs
            exit 1
        fi
        
        sleep 10
        ((attempt++))
    done
}

# Show service logs for debugging
show_service_logs() {
    log_info "Showing recent service logs..."
    docker-compose logs --tail=50
}

# Run validation tests
run_validation() {
    log_info "Running post-deployment validation..."
    
    # Run basic system validation
    docker-compose exec -T mare-system python3 -c "
import sys
sys.path.insert(0, '/app/src')
from mare import MARESystem

print('🧪 Running deployment validation...')
system = MARESystem()

# Test system health
health = system.get_system_health()
print(f'System Status: {health[\"system_status\"]}')

# Test REP loading
reps = system.list_available_reps()
print(f'Available REPs: {len(reps)}')

# Test basic task execution
result = system.execute_task('Test deployment validation', 'Validation result')
print(f'Test Task Status: {result.status}')
print(f'Test Task REP: {result.rep_used}')

system.shutdown()
print('✅ Deployment validation completed')
"
    
    if [[ $? -eq 0 ]]; then
        log_success "Validation tests passed"
    else
        log_error "Validation tests failed"
        exit 1
    fi
}

# Show deployment summary
show_deployment_summary() {
    echo ""
    echo "=================================================================="
    echo "  🎉 MARE SYSTEM DEPLOYMENT COMPLETE"
    echo "=================================================================="
    echo ""
    echo "Services:"
    echo "  • MARE System:    http://localhost:8080"
    echo "  • Prometheus:     http://localhost:9090" 
    echo "  • Grafana:        http://localhost:3000 (admin/mare2025)"
    echo ""
    echo "Available Commands:"
    echo "  • Interactive Demo:       docker-compose exec mare-system python3 demo_mare.py"
    echo "  • Validation Suite:       docker-compose exec mare-system python3 mare_validation_suite.py"
    echo "  • Benchmark Comparison:   docker-compose exec mare-system python3 mare_benchmark_comparison.py"
    echo "  • View Logs:              docker-compose logs -f mare-system"
    echo "  • System Health:          docker-compose exec mare-system python3 -c \"import sys; sys.path.insert(0, '/app/src'); from mare import MARESystem; s=MARESystem(); print(s.get_system_health()); s.shutdown()\""
    echo ""
    echo "Management:"
    echo "  • Stop Services:          docker-compose down"
    echo "  • View Status:            docker-compose ps"
    echo "  • Scale Services:         docker-compose up -d --scale mare-system=2"
    echo ""
    echo "=================================================================="
}

# Cleanup function
cleanup() {
    log_info "Performing cleanup..."
    # Add any cleanup tasks here
    log_success "Cleanup completed"
}

# Error handler
handle_error() {
    log_error "Deployment failed on line $1"
    cleanup
    exit 1
}

# Set error trap
trap 'handle_error $LINENO' ERR

# Main deployment flow
main() {
    print_banner
    
    case "${1:-deploy}" in
        "deploy")
            check_prerequisites
            build_image
            deploy_services
            wait_for_health
            run_validation
            show_deployment_summary
            ;;
        "build")
            check_prerequisites
            build_image
            ;;
        "start")
            deploy_services
            wait_for_health
            show_deployment_summary
            ;;
        "stop")
            log_info "Stopping MARE services..."
            docker-compose down
            log_success "Services stopped"
            ;;
        "status")
            log_info "Checking service status..."
            docker-compose ps
            ;;
        "logs")
            log_info "Showing service logs..."
            docker-compose logs -f
            ;;
        "validate")
            run_validation
            ;;
        "clean")
            log_info "Cleaning up deployment..."
            docker-compose down --volumes --rmi local
            docker system prune -f
            log_success "Cleanup completed"
            ;;
        "help")
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  deploy    - Full deployment (default)"
            echo "  build     - Build Docker image only"
            echo "  start     - Start services"
            echo "  stop      - Stop services"
            echo "  status    - Show service status"
            echo "  logs      - Show service logs"
            echo "  validate  - Run validation tests"
            echo "  clean     - Clean up everything"
            echo "  help      - Show this help"
            ;;
        *)
            log_error "Unknown command: $1"
            echo "Use '$0 help' for available commands"
            exit 1
            ;;
    esac
}

# Execute main function with all arguments
main "$@"