# syntax=docker/dockerfile:1.6
# PyQuantLib Docker image (multi-stage)
#
# Stage 1 builds QuantLib (static) and compiles a self-contained PyQuantLib wheel.
# Stage 2 is a slim runtime with only the wheel + JupyterLab; the build toolchain,
# Boost headers, and QuantLib source never reach the final image.
#
# Build:   docker build -t pyquantlib:latest .
# Run:     docker run --rm -p 8888:8888 pyquantlib:latest
# Then open http://localhost:8888 in a browser.

# ==============================================================================
# Stage 1: builder
# ==============================================================================
FROM python:3.11-slim AS builder

# Build-time system dependencies. QuantLib needs a C++ toolchain and Boost
# headers; Ninja matches the CI build.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        ninja-build \
        libboost-all-dev \
        wget \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Build and install QuantLib from source (STATIC).
# QuantLib MUST be a static library built with PIC and the std:: type flags:
# a shared build duplicates the Settings singleton and breaks evaluationDate.
# Mirrors .github/workflows/linux.yml.
ARG QUANTLIB_VERSION=1.42.1
WORKDIR /tmp
RUN wget --quiet https://github.com/lballabio/QuantLib/releases/download/v${QUANTLIB_VERSION}/QuantLib-${QUANTLIB_VERSION}.tar.gz \
    && tar xzf QuantLib-${QUANTLIB_VERSION}.tar.gz \
    && cd QuantLib-${QUANTLIB_VERSION} \
    && cmake -B build -G Ninja \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DBUILD_SHARED_LIBS=OFF \
        -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
        -DQL_USE_STD_SHARED_PTR=ON \
        -DQL_USE_STD_OPTIONAL=ON \
        -DQL_USE_STD_ANY=ON \
        -DQL_BUILD_EXAMPLES=OFF \
        -DQL_BUILD_TEST_SUITE=OFF \
        -DQL_BUILD_BENCHMARK=OFF \
    && cmake --build build \
    && cmake --install build \
    && cd /tmp \
    && rm -rf QuantLib-${QUANTLIB_VERSION}*

# Build a self-contained PyQuantLib wheel. The static QuantLib is linked into the
# extension and Boost is header-only, so the wheel needs no QuantLib at runtime.
# QuantLib_ROOT lets scikit-build-core's CMake find the static install above.
ENV QuantLib_ROOT=/usr/local
WORKDIR /src
COPY . /src
RUN pip install --no-cache-dir --upgrade pip build \
    && pip wheel . --no-deps -w /wheels

# ==============================================================================
# Stage 2: runtime
# ==============================================================================
FROM python:3.11-slim AS runtime

# C++ runtime the compiled extension links against (matches the builder's gcc).
RUN apt-get update && apt-get install -y --no-install-recommends \
        libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Install the PyQuantLib wheel plus the JupyterLab + scientific stack.
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl \
        jupyterlab \
        numpy \
        scipy \
        matplotlib \
        pandas \
    && rm -rf /wheels

# Example notebooks for interactive use.
WORKDIR /app
COPY examples/ /app/examples/
COPY README.md /app/

EXPOSE 8888

CMD ["jupyter", "lab", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--allow-root", \
     "--ServerApp.token=", \
     "--ServerApp.password="]
