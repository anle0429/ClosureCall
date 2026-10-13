# GitHub workflow

Repository: [anle0429/ClosureCall](https://github.com/anle0429/ClosureCall), verified **private** on October 13, 2026. Default branch: `master`. Portfolio application source and the private Linode release are distinct; GitHub pushes do not deploy the app.

Prepare changes on a review branch, inspect the diff, run checks and stage named files. The October 13 work continues `maintenance/portfolio-readiness`; its reviewed source/tests/docs will be promoted to the private default branch by fast-forward only if the remote base is unchanged. This is an authorized private progress update, not publication or production deployment.

```sh
git status --short
git diff
python -m pytest -q
python scripts/check_secrets.py
# Stage only the source/docs/evidence you reviewed.
git diff --cached
git commit -m "Describe the problem and the verified change"
git push
git rev-parse HEAD
git ls-remote origin refs/heads/master
```

The local pushed commit must match the intended remote branch; an unrelated branch's hash is not push proof. Never force-push to bypass new remote work. Review screenshots/logs before staging. Keep env, runtime DB/backups, keys and user-supplied untracked goal packages outside Git. Authentication comes from the existing credential manager, never a token in the URL or a command argument.

The manual verification workflow is prepared; no hosted CI run is claimed or triggered automatically by a push. License/team rights, public visibility, collaborator access, LinkedIn publication and any new deployment are separate decisions. [Current product review](PRODUCT_REVIEW.md), [release manifest](../RELEASE_MANIFEST.json), [historical first-push record](archive/hackathon/GITHUB_PROGRESS.md).
