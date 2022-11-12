cd tests/ && \
docker stop test-db-container
docker rm test-db-container
docker image rm test-db