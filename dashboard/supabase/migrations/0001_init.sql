CREATE TABLE repos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    
    repo_id BIGINT NOT NULL,
    repo_name TEXT NOT NULL,

    unique (repo_id)
);

CREATE TABLE audits {
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),

    repo_name TEXT NOT NULL,
    commit_sha TEXT NOT NULL,
    audit_time TIMESTAMPTZ NOT NULL DEFAULT now(),

    repo_id UUID NOT NULL REFERENCES repos(id)
}

CREATE TABLE detections {
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),

    package TEXT NOT NULL,
    package_version TEXT NOT NULL,
    depr_status TEXT NOT NULL,
    src TEXT NO NULL,

    audit_id UUID NOT NULL REFERENCES audits(id)
}

CREATE TABLE usages {
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),

    usage_file TEXT,
    usage_line INT,
    usage_code TEXT,

    detection_id UUID NOT NULL REFERENCES detections(id)
}

CREATE POLICY "Users can only access their own repos" ON repos FOR ALL USING (auth.uid() = user_id);