import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "@/app/generated/prisma/client";
import { Pool } from "pg";

const DEFAULT_POOL_MAX = 10;
const DEFAULT_IDLE_TIMEOUT_MS = 30_000;
const DEFAULT_CONNECTION_TIMEOUT_MS = 5_000;

type GlobalWithPrisma = typeof globalThis & {
    prisma?: PrismaClient;
};

const globalForPrisma = globalThis as GlobalWithPrisma;

function readRequiredEnv(name: string): string {
    const value = process.env[name]?.trim();

    if (!value) {
        throw new Error(`${name} is required but was not configured.`);
    }

    return value;
}

function readPositiveIntegerEnv(name: string, fallback: number): number {
    const rawValue = process.env[name]?.trim();

    if (!rawValue) {
        return fallback;
    }

    const value = Number(rawValue);

    if (!Number.isInteger(value) || value <= 0) {
        throw new Error(`${name} must be a positive integer.`);
    }

    return value;
}

function createPool(): Pool {
    return new Pool({
        connectionString: readRequiredEnv("DATABASE_URL"),
        max: readPositiveIntegerEnv("PRISMA_POOL_MAX", DEFAULT_POOL_MAX),
        idleTimeoutMillis: readPositiveIntegerEnv(
            "PRISMA_POOL_IDLE_TIMEOUT_MS",
            DEFAULT_IDLE_TIMEOUT_MS,
        ),
        connectionTimeoutMillis: readPositiveIntegerEnv(
            "PRISMA_POOL_CONNECTION_TIMEOUT_MS",
            DEFAULT_CONNECTION_TIMEOUT_MS,
        ),
    });
}

function createPrismaClient(): PrismaClient {
    const adapter = new PrismaPg(createPool(), {
        disposeExternalPool: true,
    });

    return new PrismaClient({ adapter });
}

export const prisma = globalForPrisma.prisma ?? createPrismaClient();

if (process.env.NODE_ENV !== "production") {
    globalForPrisma.prisma = prisma;
}

export default prisma;
