CREATE TABLE IF NOT EXISTS jobs (
    id VARCHAR NOT NULL PRIMARY KEY,
    state INT NOT NULL DEFAULT 0,
    queued_at DATETIME NOT NULL DEFAULT current_timestamp,
    started_at DATETIME,
    completed_at DATETIME
);

CREATE TABLE IF NOT EXISTS job_params (
    id VARCHAR NOT NULL PRIMARY KEY REFERENCES jobs(id),
    rfd_mode VARCHAR NOT NULL,
    rfd_num_designs INT  NOT NULL,
    seqs_per_design INT  NOT NULL,
    rfd_min_helices INT  NOT NULL,
    rfd_max_helices INT  NOT NULL,
    rfd_min_strands INT  NOT NULL,
    rfd_max_strands INT  NOT NULL,
    rfd_min_ss INT  NOT NULL,
    rfd_max_ss INT  NOT NULL,
    rfd_min_rog INT  NOT NULL,
    rfd_max_rog INT  NOT NULL
);
