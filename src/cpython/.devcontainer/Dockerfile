# syntax=docker/dockerfile:1
FROM ubuntu:24.04

SHELL ["/bin/bash", "-c"]

ARG INSTALL_TOML=082-3-13_cpython.toml
ARG USERNAME=vscode

WORKDIR /tmp

# Install tools required to expand and run the AtCoder install script and for
# common development tasks.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        python3 \
        python3-pip \
        python3-venv \
        sudo \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user that matches the VS Code default.
RUN useradd -ms /bin/bash "${USERNAME}" \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-cloud-init-users \
    && chmod 0440 /etc/sudoers.d/90-cloud-init-users

# Copy the AtCoder language definition and extract the embedded install script.
COPY ${INSTALL_TOML} /tmp/install.toml
RUN set -euo pipefail; \
    python3 - <<'PY' >/tmp/install.sh
import tomllib
import pathlib
install = tomllib.loads(pathlib.Path("/tmp/install.toml").read_text())
script = install["install"].replace("sudo ", "")
pathlib.Path("/tmp/install.sh").write_text(script)
PY

# Run the AtCoder-provided install script and remove build leftovers.
RUN bash /tmp/install.sh \
    && rm -f /tmp/install.sh /tmp/install.toml /tmp/Python-*.tar.xz \
    && rm -rf /tmp/Python-*

# Ensure the newly installed interpreter is available under common names.
RUN update-alternatives --install /usr/local/bin/python python /usr/local/bin/python3.13 10 \
    && update-alternatives --install /usr/local/bin/python3 python3 /usr/local/bin/python3.13 10

WORKDIR /workspace
USER ${USERNAME}
