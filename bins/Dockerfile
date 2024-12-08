FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV HOST=i386-pc-linux
ENV IDIR=/home/tester/simplescalar
ENV TARGET=sslittle-na-sstrix
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

RUN dpkg --add-architecture i386 && \
	apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    curl \
	ssh \
	bison \
	flex \
	gzip \
	gcc-multilib \
	libc6:i386 \
    libz1:i386 \
    libncurses5:i386 \
    libbz2-1.0:i386 \
	make \
	python3 \
	python3-pip \
	python3-venv \
	pigz \
    ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install flask requests

RUN mkdir -p /home/tester/simplescalar

COPY ./simplesim-3v0e.tgz /home/tester/simplescalar
COPY ./simpleutils-2.0d.tar.gz /home/tester/simplescalar
COPY ./benchmark.tar /home/tester/simplescalar
# COPY ./env /home/tester/.bashrc
COPY ./server.py /home/tester

WORKDIR /home/tester

SHELL ["/bin/bash", "-c"]

RUN cd simplescalar && \
	tar xf simplesim-3v0e.tgz && \
	tar xf simpleutils-2.0d.tar.gz

RUN	cd simplescalar/binutils-2.5.2 && \
	./configure --host=$HOST --target=$TARGET --with-gnu-as --with-gnu-ld --prefix=$IDIR && \
	make all && \
	make install

RUN cd simplescalar/simplesim-3.0 && \
	make config-alpha && \
	make

RUN cd simplescalar && \
	tar xf benchmark.tar

CMD ["flask", "run"]

