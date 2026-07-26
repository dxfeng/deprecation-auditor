import sys; args = sys.argv[1:]

from .dependency_checker.audit_glue import perform_audit

def main():
    if args[0] == "pypi_audit":
        """
        args -> ["manifest_path", "repo_root", "repo_info", "github_token"]
        """

        return perform_audit(args[1:])
    return 0
        

if __name__ == "__main__":
    res = main()
    sys.exit(res);