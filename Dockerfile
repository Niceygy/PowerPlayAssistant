FROM alpine:latest
# Set working directory in the container
WORKDIR /app/

COPY powerplayassistant .

LABEL org.opencontainers.image.description="PowerPlay Assistant"
LABEL org.opencontainers.image.authors="Niceygy (Ava Whale)"

RUN chmod 777 ./powerplayassistant

# Expose the application port
EXPOSE 8080
# Run the application
CMD ["./powerplayassistant"]