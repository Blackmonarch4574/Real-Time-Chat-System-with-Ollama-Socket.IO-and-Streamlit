#!/bin/bash

# Script to initialize Ollama with the required model
echo "Initializing Ollama with required model..."

# Wait for Ollama to be ready
echo "Waiting for Ollama service to be ready..."
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
    echo "Waiting for Ollama..."
    sleep 2
done

echo "Ollama is ready!"

# Pull the required model
echo "Pulling llama3.2:1b model..."
curl -X POST http://localhost:11434/api/pull \
    -H "Content-Type: application/json" \
    -d '{"name": "llama3.2:1b"}' \
    --no-progress-meter

echo "Model pull initiated. This may take several minutes..."

# Wait for model to be available
echo "Waiting for model to be ready..."
while true; do
    if curl -s http://localhost:11434/api/tags | grep -q "llama3.2:1b"; then
        echo "Model llama3.2:1b is ready!"
        break
    fi
    echo "Still pulling model..."
    sleep 10
done

echo "Ollama initialization complete!"