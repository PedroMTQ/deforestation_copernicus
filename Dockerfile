FROM python:3.11.3-bullseye AS build
# installs uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir app
COPY ./uv.lock app/uv.lock
COPY ./pyproject.toml app/pyproject.toml
COPY ./README.md app/README.md

# Extract version and add to a __version__ file which will be read by the service later
RUN echo $(grep -m 1 'version' app/pyproject.toml | sed -E 's/version = "(.*)"/\1/') > /app/__version__


# copying source code
COPY ./src/ app/src/
WORKDIR "/app"

# installs package
RUN uv sync --frozen
ENV PATH="/app/.venv/bin:$PATH"


# Final
FROM build
RUN apt autoremove -y && apt clean -y
