FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1

# NEXT_PUBLIC_* degerleri derleme aninda gomulur; sitede NEXT_PUBLIC_SITE_URL
# verilmezse canonical/OG/sitemap localhost'a duser ve SEO bozulur. Bu yuzden
# build arg'i zorunlu tutuluyor: verilmeden build calisirsa hata verir.
ARG NEXT_PUBLIC_SITE_URL
RUN test -n "$NEXT_PUBLIC_SITE_URL" || ( \
      echo "HATA: NEXT_PUBLIC_SITE_URL build arg'i verilmedi."; \
      echo "Ornek: docker build --build-arg NEXT_PUBLIC_SITE_URL=https://www.siten.com ."; \
      exit 1 \
    )
ENV NEXT_PUBLIC_SITE_URL=$NEXT_PUBLIC_SITE_URL

RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.ts ./
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000

CMD ["sh", "-c", "npx next start -p ${PORT:-3000}"]
