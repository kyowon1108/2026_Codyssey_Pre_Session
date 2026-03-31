FROM nginx:alpine

LABEL org.opencontainers.image.title="codyssey-pre-session-web"
LABEL org.opencontainers.image.description="Simple static site for Docker workstation assignment"

ENV APP_ENV=dev

COPY app/ /usr/share/nginx/html/
