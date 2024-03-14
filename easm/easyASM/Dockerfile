# Use the official Golang image to create a build artifact.
FROM golang:1.22 as builder

# Set the Current Working Directory inside the container
WORKDIR /go/src/app

# Install EasyEASM and its dependencies
RUN go install github.com/g0ldencybersec/EasyEASM/easyeasm@latest && \
    go install github.com/projectdiscovery/httpx/cmd/httpx@latest && \
    go install github.com/owasp-amass/oam-tools/cmd/oam_subs@master && \
    go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install github.com/projectdiscovery/alterx/cmd/alterx@latest && \
    go install github.com/owasp-amass/amass/v3/...@master && \
    go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest

# Use a Docker multi-stage build to minimize the size of the final image
# by not including the build tools and intermediate files.
FROM golang:1.22

# Create a non-root user 
RUN adduser --gecos '' easyasm
USER easyasm
WORKDIR /home/easyasm
RUN mkdir -p /home/easyasm/results

# Copy the binary files from the builder stage to the final image
COPY --from=builder /go/bin /usr/local/bin
COPY config.yml /home/easyasm/config.yml

# Force notifications on all domains discovered for demo purposes
# Delete this line if you want to keep the EasyEASM.csv file
RUN touch /home/easyasm/EasyEASM.csv

# Set the working directory in the container
WORKDIR /home/easyasm/

# Run EasyEASM when the container launches
CMD ["easyeasm"]
