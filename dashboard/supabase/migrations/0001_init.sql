CREATE TABLE repos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),

    github_repo_id BIGINT NOT NULL,
    repo_name TEXT NOT NULL,

    UNIQUE (github_repo_id)
);

CREATE TABLE audits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),

    repo_name TEXT NOT NULL,
    commit_sha TEXT NOT NULL,
    audit_time TIMESTAMPTZ NOT NULL DEFAULT now(),

    repo_id UUID NOT NULL REFERENCES repos(id)
);

CREATE TABLE detections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),

    package TEXT NOT NULL,
    package_version TEXT NOT NULL,
    depr_status TEXT NOT NULL,
    src TEXT NOT NULL,

    audit_id UUID NOT NULL REFERENCES audits(id)
);

CREATE TABLE usages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),

    usage_file TEXT NOT NULL,
    usage_line INT NOT NULL,
    usage_code TEXT NOT NULL,

    detection_id UUID NOT NULL REFERENCES detections(id)
);

ALTER TABLE repos ENABLE ROW LEVEL SECURITY;
ALTER TABLE audits ENABLE ROW LEVEL SECURITY;
ALTER TABLE detections ENABLE ROW LEVEL SECURITY;
ALTER TABLE usages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can only access their own repos" ON repos
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can only read their own audits" ON audits
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can only read their own detections" ON detections
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can only read their own usages" ON usages
    FOR ALL USING (auth.uid() = user_id);

GRANT SELECT, INSERT, UPDATE, DELETE ON repos TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON audits TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON detections TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON usages TO authenticated;

GRANT SELECT, INSERT, UPDATE, DELETE ON repos TO service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON audits TO service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON detections TO service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON usages TO service_role;
