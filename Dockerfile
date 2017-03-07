FROM alpine:3.5
COPY opt /opt
RUN apk -Uuv add groff less python3 git && \
    pip3 install -r /opt/requirements.txt && \
    rm /var/cache/apk/*