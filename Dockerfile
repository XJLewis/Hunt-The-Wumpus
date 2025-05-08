FROM python:3.11-slim

# Install SDL2 and other dependencies (see Pygame docs):contentReference[oaicite:2]{index=2}
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libfreetype6-dev libportmidi-dev libjpeg-dev libpng-dev \
    python3-dev python3-setuptools python3-pip \
    libx11-6 libx11-dev libasound2 \
    x11-common xfonts-base \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# Set the DISPLAY so the container uses the host X server:contentReference[oaicite:3]{index=3}
ENV DISPLAY=host.docker.internal:0.0

# Run the game (adjust the command/path as needed)
CMD ["python", "main.py"]
