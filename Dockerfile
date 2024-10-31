FROM ghcr.io/astral-sh/uv:0.4.28 as uv
FROM python:3.12-slim

# install UV package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Create a virtual environment with uv inside the container
RUN /usr/local/bin/uv venv 
# We need to set this environment variable so that uv knows where
# the virtual environment is to install packages
ENV VIRTUAL_ENV=/app/.venv
# Make sure that the virtual environment is in the PATH so
# we can use the binaries of packages that we install such as pip
# without needing to activate the virtual environment explicitly
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app
COPY app /app/
COPY uv.lock pyproject.toml .python-version /app/

# TODO: is this too much? Can I just uv sync inside the container?
RUN /usr/local/bin/uv venv

RUN /usr/local/bin/uv sync

# these two need to be specified via `docker run -e PGPASS=FOO`
# ENV USER=MIKE
# ENV PGPASS=Secret123

CMD [ "streamlit", "run", "/app/app.py" ] 