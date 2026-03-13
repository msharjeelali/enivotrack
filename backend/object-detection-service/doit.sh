case "$1" in
    dev-setup)
        python3.10 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements-dev.txt
        ;;
    setup)
        python3.10 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
        ;;
    run)
        uvicorn app.main:app --reload
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
    *)
        echo "Usage: ./doit.sh {run|test|lint|lint-fix}"
        exit 1
        ;;
esac
    