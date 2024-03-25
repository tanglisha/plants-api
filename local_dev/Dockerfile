FROM python:3.12-slim-bookworm as poetry

ARG USERNAME="app"
ARG APPDIR="/app"
ENV POETRY_NO_INTERACTION=1

WORKDIR "${APPDIR}"

# Create and use a non-root user
# Then install poetry sysytem wide
RUN useradd --create-home --shell /bin/bash "${USERNAME}" && \
    chown -R "${USERNAME}:${USERNAME}" "${APPDIR}" && \
    python -m pip install poetry

# Switch to the non-root user
USER "${USERNAME}"

# In docker-compose . is one directory up
COPY --chown=${USERNAME} . "${APPDIR}"
COPY --chown=${USERNAME} pyproject.toml "${APPDIR}"
RUN poetry install

CMD ["/bin/bash"]