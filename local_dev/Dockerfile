FROM python:3.12-slim-bookworm

# Image for development

# Non-root user of this image
ARG USERNAME="app"
# Location of the code
ARG APPDIR="/app"

# Poetry won't ask for confirmations
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_PATH=/app/venv

# cd to the code directory
WORKDIR "${APPDIR}"

# Create and use a non-root user
# Install poetry sysytem wide
# Install tk library
RUN useradd --create-home --shell /bin/bash "${USERNAME}" && \
    chown -R "${USERNAME}:${USERNAME}" "${APPDIR}" && \
    python -m pip install poetry && \
    apt-get update && \
    apt-get install -y python3-tk && \
    apt-get install -y postgresql && \
    rm -r /var/lib/apt/lists/*

# Switch to the non-root user
# USER "${USERNAME}"

# In docker-compose . is one directory up
COPY --chown=${USERNAME} . "${APPDIR}"
COPY --chown=${USERNAME} pyproject.toml "${APPDIR}"
COPY --chown=${USERNAME} local_dev/bin/start-app /usr/local/bin/
RUN poetry install

CMD ["/bin/bash"]
