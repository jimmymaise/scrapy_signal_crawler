#!/bin/sh

# Start Tor service
service tor start

# Start Privoxy service
service privoxy start

# Keep the container running
exec "$@"
