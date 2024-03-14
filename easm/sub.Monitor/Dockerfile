# Use an official Go runtime as a parent image
FROM golang:alpine as builder

# Install necessary build tools
RUN apk update && apk add --no-cache git gcc g++ make

# Install amass
RUN go install -v github.com/owasp-amass/amass/v4/...@master

# Install subfinder
RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Install assetfinder
RUN go install github.com/tomnomnom/assetfinder@latest

# Install notify
RUN go install -v github.com/projectdiscovery/notify/cmd/notify@latest

# Final image
FROM alpine:latest

# Copy the binaries from the builder stage
COPY --from=builder /go/bin/amass /usr/local/bin/
COPY --from=builder /go/bin/subfinder /usr/local/bin/
COPY --from=builder /go/bin/assetfinder /usr/local/bin/
COPY --from=builder /go/bin/notify /usr/local/bin/

# Install runtime dependencies, Python3, pip and create a non-root user
RUN apk --no-cache add ca-certificates python3 py3-pip git && \
    adduser -D -g '' submonitor 

# Create a non-root user 
USER submonitor

# Set working directory
WORKDIR /home/submonitor
RUN mkdir -p /home/submonitor/.config

# Copy configuration files
COPY --chown=submonitor:submonitor local_config/amass_config.ini /home/submonitor/.config/amass/config.ini
COPY --chown=submonitor:submonitor local_config/subfinder_config.yaml /home/submonitor/.config/subfinder/config.yaml
COPY --chown=submonitor:submonitor local_config/notify_config.yaml /home/submonitor/.config/notify/provider-config.yaml
COPY --chown=submonitor:submonitor wordlists /home/submonitor/.config/wordlists

# Clone the sub.Monitor repository
RUN git clone https://github.com/e1abrador/sub.Monitor.git
COPY config.ini /home/submonitor/sub.Monitor/config.ini
RUN pip3 install --break-system-packages -r /home/submonitor/sub.Monitor/requirements.txt 

# Open a shell in the container and follow instructions from https://github.com/e1abrador/sub.Monitor
ENTRYPOINT ["/bin/sh"]

