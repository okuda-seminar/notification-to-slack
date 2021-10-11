ARG PYTHON_VERSION=3.8

FROM python:${PYTHON_VERSION}
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq && \
    apt-get install -y \
      curl libopencv-dev lsof git sudo tmux tree vim wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apk/*

ENV WORK_PATH /workspace
WORKDIR $WORK_PATH
ENV PYTHONPATH "/workspace:${PYTHONPATH}"
ENV PIP_OPTIONS "--no-cache-dir --progress-bar off"
COPY docker/requirements.txt $WORK_PATH/docker/
RUN pip install ${PIP_OPTIONS} -r $WORK_PATH/docker/requirements.txt && \
    pip install ${PIP_OPTIONS} -U setuptools

RUN curl -sL https://deb.nodesource.com/setup_15.x | sudo -E bash -&& \
    apt-get install -y nodejs
