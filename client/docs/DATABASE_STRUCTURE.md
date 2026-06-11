# How the Database Will Look (PostgreSQL)

What Prisma generates as **physical Postgres tables** from [schema.prisma](./schema.prisma).
For relations/cardinality see [SCHEMA_RELATIONS.md](./SCHEMA_RELATIONS.md).

---

## Tables

### `User`
| Column | Postgres type | Constraints |
|---|---|---|
| id | `text` | **PK** (no default — you supply it; GitHub user id) |
| email | `text` | **UNIQUE**, NOT NULL |
| plan | `Plan` (enum) | NOT NULL, default `'FREE'` |
| polarCustomerId | `text` | nullable |
| polarSubscriptionId | `text` | nullable |
| prsUsed | `integer` | NOT NULL, default `0` |
| prsCreated | `integer` | NOT NULL, default `0` |
| issuesUsed | `integer` | NOT NULL, default `0` |
| chatMessagesUsed | `integer` | NOT NULL, default `0` |
| billingCycleStart | `timestamp(3)` | NOT NULL, default `now()` |
| createdAt | `timestamp(3)` | NOT NULL, default `now()` |
| updatedAt | `timestamp(3)` | NOT NULL, set on every update |

### `Rule`
| Column | Type | Constraints |
|---|---|---|
| id | `text` | **PK**, default cuid (app-generated) |
| content | `text` | NOT NULL |
| userId | `text` | **FK → User.id**, NOT NULL, `ON DELETE CASCADE` |
| createdAt | `timestamp(3)` | default `now()` |
| updatedAt | `timestamp(3)` | on update |

### `Installation`
| Column | Type | Constraints |
|---|---|---|
| id | `text` | **PK**, cuid |
| installationId | `integer` | **UNIQUE**, NOT NULL |
| accountLogin | `text` | NOT NULL |
| userId | `text` | **FK → User.id**, `ON DELETE CASCADE` |
| createdAt | `timestamp(3)` | default `now()` |

### `Repository`
| Column | Type | Constraints |
|---|---|---|
| id | `text` | **PK**, cuid |
| githubId | `bigint` | **UNIQUE**, NOT NULL |
| name | `text` | NOT NULL |
| fullName | `text` | NOT NULL |
| installationId | `text` | **FK → Installation.id**, `ON DELETE CASCADE` |
| indexingStatus | `IndexingStatus` (enum) | default `'NOT_STARTED'` |
| createdAt | `timestamp(3)` | default `now()` |

### `PullRequest`
| Column | Type | Constraints |
|---|---|---|
| id | `text` | **PK**, cuid |
| githubId | `bigint` | NOT NULL (⚠️ **not** unique) |
| number | `integer` | NOT NULL |
| title | `text` | NOT NULL |
| repositoryId | `text` | **FK → Repository.id**, `ON DELETE CASCADE` |
| reviewedAt | `timestamp(3)` | default `now()` |

### `Issue`
| Column | Type | Constraints |
|---|---|---|
| id | `text` | **PK**, cuid |
| githubId | `bigint` | NOT NULL (⚠️ **not** unique) |
| number | `integer` | NOT NULL |
| title | `text` | NOT NULL |
| repositoryId | `text` | **FK → Repository.id**, `ON DELETE CASCADE` |
| analyzedAt | `timestamp(3)` | default `now()` |

---

## Enum types (native Postgres enums)

```sql
CREATE TYPE "Plan" AS ENUM ('FREE', 'PRO');
CREATE TYPE "IndexingStatus" AS ENUM ('NOT_STARTED', 'INDEXING', 'COMPLETED', 'FAILED');
```

---

## Indexes that actually get created

Prisma auto-indexes **primary keys and `@unique` columns only**. Foreign keys are **not** indexed automatically in Postgres.

| Index | Table | Reason |
|---|---|---|
| PK | every table | primary key |
| `User_email_key` | User | `@unique` |
| `Installation_installationId_key` | Installation | `@unique` |
| `Repository_githubId_key` | Repository | `@unique` |

> ⚠️ **Missing FK indexes** — `Rule.userId`, `Installation.userId`, `Repository.installationId`, `PullRequest.repositoryId`, `Issue.repositoryId` have **no index**. Joins and cascade-deletes on these do a sequential scan. On real data volume, add `@@index([...])` on each FK column.

---

## Physical link chain (cascade)

```
User (id = GitHub user id, supplied by app)
 ├─ Rule         (userId FK)         ── delete User → rules deleted
 └─ Installation (userId FK)         ── delete User → installations deleted
     └─ Repository (installationId)  ── delete Installation → repos deleted
         ├─ PullRequest (repositoryId)
         └─ Issue       (repositoryId)
```

Deleting a single `User` row cascades through the entire subtree in the DB engine — no application code required.

---

## What a populated DB looks like (example rows)

```
User
 id="12345678"  email="dev@x.com"  plan=PRO  prsUsed=14  ...

Installation
 id="clx1.."  installationId=98765  accountLogin="acme"  userId="12345678"

Repository
 id="clx2.."  githubId=42424242  fullName="acme/api"  installationId="clx1.."  indexingStatus=COMPLETED

PullRequest
 id="clx3.."  githubId=111  number=27  title="Add auth"   repositoryId="clx2.."

Issue
 id="clx4.."  githubId=222  number=5   title="Login bug"  repositoryId="clx2.."
```

---

## Approximate generated DDL

```sql
CREATE TABLE "User" (
  "id"                  TEXT PRIMARY KEY,
  "email"               TEXT NOT NULL,
  "plan"                "Plan" NOT NULL DEFAULT 'FREE',
  "polarCustomerId"     TEXT,
  "polarSubscriptionId" TEXT,
  "prsUsed"             INTEGER NOT NULL DEFAULT 0,
  "prsCreated"          INTEGER NOT NULL DEFAULT 0,
  "issuesUsed"          INTEGER NOT NULL DEFAULT 0,
  "chatMessagesUsed"    INTEGER NOT NULL DEFAULT 0,
  "billingCycleStart"   TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "createdAt"           TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt"           TIMESTAMP(3) NOT NULL
);
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

CREATE TABLE "Rule" (
  "id"        TEXT PRIMARY KEY,
  "content"   TEXT NOT NULL,
  "userId"    TEXT NOT NULL,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt" TIMESTAMP(3) NOT NULL,
  CONSTRAINT "Rule_userId_fkey" FOREIGN KEY ("userId")
    REFERENCES "User"("id") ON DELETE CASCADE
);

CREATE TABLE "Installation" (
  "id"             TEXT PRIMARY KEY,
  "installationId" INTEGER NOT NULL,
  "accountLogin"   TEXT NOT NULL,
  "userId"         TEXT NOT NULL,
  "createdAt"      TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "Installation_userId_fkey" FOREIGN KEY ("userId")
    REFERENCES "User"("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX "Installation_installationId_key" ON "Installation"("installationId");

CREATE TABLE "Repository" (
  "id"             TEXT PRIMARY KEY,
  "githubId"       BIGINT NOT NULL,
  "name"           TEXT NOT NULL,
  "fullName"       TEXT NOT NULL,
  "installationId" TEXT NOT NULL,
  "indexingStatus" "IndexingStatus" NOT NULL DEFAULT 'NOT_STARTED',
  "createdAt"      TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "Repository_installationId_fkey" FOREIGN KEY ("installationId")
    REFERENCES "Installation"("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX "Repository_githubId_key" ON "Repository"("githubId");

CREATE TABLE "PullRequest" (
  "id"           TEXT PRIMARY KEY,
  "githubId"     BIGINT NOT NULL,
  "number"       INTEGER NOT NULL,
  "title"        TEXT NOT NULL,
  "repositoryId" TEXT NOT NULL,
  "reviewedAt"   TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "PullRequest_repositoryId_fkey" FOREIGN KEY ("repositoryId")
    REFERENCES "Repository"("id") ON DELETE CASCADE
);

CREATE TABLE "Issue" (
  "id"           TEXT PRIMARY KEY,
  "githubId"     BIGINT NOT NULL,
  "number"       INTEGER NOT NULL,
  "title"        TEXT NOT NULL,
  "repositoryId" TEXT NOT NULL,
  "analyzedAt"   TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "Issue_repositoryId_fkey" FOREIGN KEY ("repositoryId")
    REFERENCES "Repository"("id") ON DELETE CASCADE
);
```

---

## Before you migrate — two fixes

1. **`datasource db` has no `url`.** Add `url = env("DATABASE_URL")` (and `directUrl` if using a pooler) or `prisma migrate`/`generate` can't connect.
2. **No FK indexes.** Add `@@index([userId])`, `@@index([installationId])`, `@@index([repositoryId])` on the child models to avoid sequential scans on joins and cascade deletes.
