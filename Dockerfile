FROM alpine:3.19 as scripts
WORKDIR /src

COPY .swcrc .
COPY scripts ./scripts

RUN apk add swc && swc compile --config-file .swcrc --out-dir . scripts

FROM denoland/deno:alpine-1.41.0
EXPOSE 8000
WORKDIR /app
USER deno

COPY deno.json .
COPY deno.lock .
COPY *.ts .
COPY templates ./templates
COPY public ./public
COPY --from=scripts /src/scripts public/scripts

RUN deno cache --reload --lock=deno.lock main.ts
CMD ["run", "--lock=deno.lock", "--cached-only", "--allow-env", "--allow-read", "--allow-net", "main.ts"]

