FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y tor privoxy curl supervisor && \
    apt-get clean

# Configure Tor
RUN echo 'ControlPort 9051' >> /etc/tor/torrc && \
    echo 'CookieAuthentication 0' >> /etc/tor/torrc

# Configure Privoxy
RUN echo 'forward-socks5t / 127.0.0.1:9050 .' >> /etc/privoxy/config

# Configure Supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose Privoxy port
EXPOSE 8118

# Run Supervisor
CMD ["/usr/bin/supervisord"]