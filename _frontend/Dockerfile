FROM node:18-alpine AS builder

RUN npm install -g pnpm

WORKDIR /app

COPY package.json pnpm-lock.yaml ./

RUN pnpm install

COPY . .

RUN pnpm run build

EXPOSE 3000

FROM node:18-alpine

RUN npm install -g pnpm

WORKDIR /app

# Copy built assets from builder stage
COPY --from=builder /app/package.json ./
COPY --from=builder /app/pnpm-lock.yaml ./

RUN pnpm install --prod

COPY --from=builder /app/dist ./dist

EXPOSE 3000

# CMD [ "pnpm", "run", "preview" ]
