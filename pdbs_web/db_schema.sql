CREATE TABLE IF NOT EXISTS jobs (
    id VARCHAR NOT NULL PRIMARY KEY,
    state INT NOT NULL DEFAULT 0,
    queued_at DATETIME NOT NULL DEFAULT current_timestamp,
    started_at DATETIME,
    completed_at DATETIME,
    info VARCHAR
);

CREATE TABLE IF NOT EXISTS job_params (
    id VARCHAR NOT NULL PRIMARY KEY REFERENCES jobs(id),
    params VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS input_cache (
    job_id VARCHAR NOT NULL PRIMARY KEY,
    hash VARCHAR NOT NULL,
    file_name VARCHAR NOT NULL
);
