FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y tor privoxy curl && \
    apt-get clean

# Configure Tor

RUN echo 'ControlPort 0.0.0.0:9051' >> /etc/tor/torrc && \
    echo 'CookieAuthentication 0' >> /etc/tor/torrc &&\
        echo 'SOCKSPort 0.0.0.0:9050' >> /etc/tor/torrc &&\
echo "HashedControlPassword $(tor --quiet --hash-password abc123)" >> /etc/tor/torrc


# Configure Privoxy
RUN echo 'forward-socks5t / 0.0.0.0:9050 .' >> /etc/privoxy/config

# Change Privoxy listen address to 0.0.0.0
RUN sed -i 's/listen-address\s*127.0.0.1:8118/listen-address 0.0.0.0:8118/g' /etc/privoxy/config

# Expose Privoxy port
EXPOSE 8118
EXPOSE 9050
EXPOSE 9051


# Start Tor and Privoxy
CMD service tor start && \
    service privoxy start && \
    sleep infinity