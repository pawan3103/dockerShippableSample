FROM nginx:latest
ADD nginx.conf /etc/nginx/nginx.conf
COPY live /app/live
COPY certificates /app/certificates
RUN chown -R nginx /app

