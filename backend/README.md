# Clinical AI Backend

Architecture scaffold only. There is no Python application, API endpoint,
database connection, or model call yet. The frontend still uses simulated replies.

## Stack

- Python 3.12 and uv for the environment and dependency management.
- FastAPI for HTTP endpoints and request/response validation.
- Pydantic Settings for environment-based configuration.
- pytest and Ruff for tests and linting.
- Planned: OpenAI Python SDK for model calls, added with the first integration.
- Planned: PostgreSQL, SQLAlchemy and Alembic for persistence.
- Planned: pgvector for document retrieval once the RAG workflow is introduced.

Only the initial API and development dependencies are declared in pyproject.toml.
No dependencies or Python environment have been installed as part of this scaffold.

## Structure

```text
backend/
  pyproject.toml
  .python-version
  .env.example
  src/
    clinical_ai/
      api/           HTTP routes and request/response schemas
      core/          Configuration and shared infrastructure
      services/      Chat and retrieval workflows
      integrations/  OpenAI and other external clients
      repositories/  Controlled database access
  tests/             Focused backend tests
```

Directories contain placeholders, not executable Python modules. Add modules
and package initialization files only when implementing their responsibilities.
Add migrations and document ingestion tools when database work begins.

## Boundaries

```text
Next.js -> API -> Chat service -> OpenAI integration
                      |
                      +-> Retrieval service -> Repositories -> PostgreSQL
```

Routes validate requests and delegate to services. Services control the workflow;
they do not contain provider-specific HTTP details or raw SQL. Integrations own
external API calls. Repositories own database queries and access restrictions.

The first implementation should be a direct chat workflow, not an autonomous
agent. Keep database tools read-only and explicitly scoped when introduced.
Use document retrieval for protocols; use controlled structured queries for
patient records instead of treating all database data as embeddings.

## Future OpenAI Integration

OpenAI API is the model provider interface; OpenAPI is the API specification
that FastAPI can generate. They are different things.

- Add the official `openai` Python SDK when implementing the integration.
- Store credentials only in backend environment variables, never in Next.js
  public variables or browser code.
- Configure the model through `OPENAI_MODEL`; no model is selected yet.
- The environment template is not loaded until configuration code is implemented.
- Define timeouts, controlled retries and error handling in the integration.
- Do not send patient data until permissions, provider data handling and hospital
  policies have been approved. Use synthetic or approved non-sensitive data first.
- Avoid recording sensitive prompts and responses in application logs.

## Environment Setup (When Implementation Starts)

Install uv, then run from this directory:

```powershell
uv sync
Copy-Item .env.example .env
```

`uv sync` creates the local environment and uv.lock. Commit uv.lock when generated.
Fill in credentials locally only when needed. There is intentionally no server
start command yet because no application entry point exists.

## Implementation Order

1. Implement configuration, a health endpoint and tests.
2. Add a chat endpoint and the OpenAI integration using non-sensitive inputs.
3. Connect the existing frontend and handle API errors.
4. Add approved documents, PostgreSQL/pgvector and answers with source references.
5. Evaluate retrieval, citation accuracy and insufficient-evidence responses.

Authentication and authorization, source access filtering, audit policy and
clinical review are required before any real hospital deployment. Fine-tuning
is a later experiment based on measured failures, not the initial data-access layer.