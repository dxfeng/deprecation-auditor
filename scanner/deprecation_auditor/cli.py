import sys; args = sys.argv[1:]

from .dependency_checker.audit_glue import perform_audit

def main():
    if args[0] == "pypi_audit":
        perform_audit(args[1:])
        

if __name__ == "__main__":
    main()