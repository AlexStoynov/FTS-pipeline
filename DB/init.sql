CREATE TABLE pipeline_runs (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source          TEXT NOT NULL,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at     TIMESTAMPTZ,
    total       INTEGER NOT NULL DEFAULT 0,
    passed      INTEGER NOT NULL DEFAULT 0,
    failed      INTEGER NOT NULL DEFAULT 0,
    CHECK (total >= 0 AND passed >= 0 AND failed >= 0),
    CHECK (passed + failed = total)
);

CREATE TABLE transactions (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id          BIGINT NOT NULL REFERENCES pipeline_runs(id),
    source          TEXT NOT NULL,
    transaction_id  TEXT,
    date            DATE NOT NULL,
    amount          NUMERIC NOT NULL,
    currency        TEXT NOT NULL,
    description     TEXT NOT NULL,
    transaction_type    TEXT NOT NULL,
    dt              TIMESTAMPTZ,
    raw_description TEXT,
    raw_type        TEXT,
    counterparty_name   TEXT,
    counterparty_iban   TEXT,
    mcc_code        TEXT,
    merchant_category   TEXT,
    fee             NUMERIC,
    category        TEXT NOT NULL DEFAULT 'uncategorized',

    UNIQUE (source, transaction_id)
);

CREATE TABLE quarantine (
    id             BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id          BIGINT NOT NULL REFERENCES pipeline_runs(id),
    source          TEXT NOT NULL,
    raw_record      JSONB NOT NULL,
    failed_check    TEXT NOT NULL,
    error_detail    TEXT,
    quarantined_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);