FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
		openssh-server \
		iproute2 \
		nmap \
		tcpdump \
		net-tools \
		netcat-traditional \
		screen \
		rsyslog \
		rsync \
		vim \
		curl \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN echo "UseDNS no" >> /etc/ssh/sshd_config && \
	echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
	echo "PasswordAuthentication no" >> /etc/ssh/sshd_config && \
	echo "StrictModes no" >> /etc/ssh/sshd_config && \
	echo "ClientAliveInterval 60" >> /etc/ssh/sshd_config && \
	echo "ClientAliveCountMax 3" >> /etc/ssh/sshd_config

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

# Install the package in editable mode
RUN pip install -e .

ENTRYPOINT ["/bin/bash", "-c", "service ssh start && tail -f /dev/null"]

