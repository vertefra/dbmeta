set -x

./scripts/init_test_db.sh && \
    export PYTHONPATH=./ && \
    pip install .[test] && \
        python -m pytest --cov=src -rP tests/ 

./scripts/cleanup_test_db.sh