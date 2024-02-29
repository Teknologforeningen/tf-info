FROM denoland/deno:alpine-1.41.0

EXPOSE 8000

WORKDIR /app

USER deno

COPY . .
RUN deno cache main.ts

CMD ["run", "--allow-env", "--allow-read", "--allow-net", "--unstable", "main.ts"]


