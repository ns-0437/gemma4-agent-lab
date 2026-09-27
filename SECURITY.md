# Security and data handling

Never paste credentials into an issue. Use GitHub's private vulnerability reporting when
available for sensitive findings. If credentials are exposed, revoke them at their issuer;
deleting a file from the latest commit does not remove it from history.

The evaluation subprocess backend is not a filesystem security boundary. Answer-key access
invalidates a task result even when the prompt itself excludes reference patches. Read
traces before using measurements to select a candidate.

Generated notebooks run shell commands. Review them locally and use an isolated environment.
