FROM alpine:3.19

RUN apk add --no-cache python3 bash

COPY entrypoint.sh /entrypoint.sh
COPY banner_server.py /banner_server.py
RUN chmod +x /entrypoint.sh

EXPOSE 21 22 80 8080

CMD ["/entrypoint.sh"]
