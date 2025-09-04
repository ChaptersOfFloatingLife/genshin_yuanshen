FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y wget && \
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && \
    dpkg -i cloudflared-linux-amd64.deb && \
    rm cloudflared-linux-amd64.deb && \
    apt-get remove -y wget && apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Environment variable defaults
ENV MODE=quick \
    ORIGIN_URL= \
    ORIGIN_HOST= \
    ORIGIN_SNI=

ENTRYPOINT ["/entrypoint.sh"]

