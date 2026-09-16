FROM ollama/ollama:latest

RUN (ollama serve &) && sleep 5 && ollama pull qwen2.5:7b

EXPOSE 10000
ENTRYPOINT ["ollama", "serve"]
