# Your Dockerfile, built from the TOP of the repository.
#   - FROM python:3.12-slim, WORKDIR /app
#   - copy requirements.txt FIRST and pip install it, then the rest of the repo
#     (raglab, data and the weeks) - so a code change does not reinstall everything
#   - a user that is not root, owning /data
#   - SNAPSHOT, VERSIONS and QUEUE pointing into /data
#   - WORKDIR week-13/milestone, EXPOSE 8000, and run:
#     uvicorn run_service:app --host 0.0.0.0 --port 8000
