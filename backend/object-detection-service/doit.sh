set -e

case "$1" in
    dev-setup)
        python3.10 -m venv .venv
        .venv/bin/pip install -r requirements-dev.txt
        echo "Setup complete. Run: source .venv/bin/activate"
        ;;
    setup)
        python3.10 -m venv .venv
        .venv/bin/pip install -r requirements.txt
        echo "Setup complete. Run: source .venv/bin/activate"
        ;;
    run)
        source .venv/bin/activate
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8001     
        ;;
    test)
        pytest tests/ -v
        ;;
    lint)
        ruff check app/ tests/
        ;;
    lint-fix)
        ruff check --fix app/ tests/
        ruff format app/ tests/
        ;;
    docker-build)
        docker compose build
        ;;
    docker-run)
        docker compose up
        ;;
    docker-run-detached)
        docker compose up -d
        ;;
    docker-stop)
        docker compose down
        ;;
    docker-logs)
        docker compose logs -f
        ;;
    *)
        echo "Usage: ./doit.sh {dev-setup|setup|run|test|lint|lint-fix|docker-build|docker-run|docker-run-detached|docker-stop|docker-logs}"
        exit 1
        ;;
esac