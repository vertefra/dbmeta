cd tests && \
docker build -t test-db . && \
docker run --rm -p 2345:5432 --name test-db-container -d test-db