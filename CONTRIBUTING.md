# Contributing

ClosureCall is a decision-support prototype. Changes must preserve the distinction between source evidence, prototype rules, model review and manager authority.

Use Python 3.12, the development requirements and Node.js only for frontend formatting. The app serves ordinary HTML/CSS/JS; there is no frontend build step.

```sh
python -m pip install -r requirements-dev.txt
npm ci --ignore-scripts
python -m black --target-version py312 app tests scripts
npm run format
python -m pytest -q
```

Formatters are pinned development tools. [Black](https://black.readthedocs.io/en/stable/) formats Python; [Prettier](https://prettier.io/docs/install) formats only the three static files. Never format frozen evidence or archived exports.

For behavior changes, start with a concrete failure and a test that exercises the relevant boundary. API changes need authentication/authority checks. Source handling needs facility/time/applicability coverage. History changes need exact frozen-body comparison and checks that replay calls no source, model or current routing. Keep test fixtures explicitly synthetic.

Run the full suite before a release, then test the exact Linux image if application code changes. A test total does not prove live integration. Record failed checks and limitations; do not skip or weaken assertions to hide them. The deadline tests separately cover startup without output and trace retention after a real worker is ready, while retaining a 0.2s budget and process-termination assertions.

The manual [verification workflow](.github/workflows/verify.yml) is prepared but has not been dispatched in this pass. It starts no deployments, uses no provider credentials and is disabled for automatic push/PR events. Running hosted CI remains an operator decision.

Keep `.env`, databases, backups, private keys and runtime logs out of Git. Review screenshots and new evidence before staging. Discuss public access, a project license and team publication rights separately; contribution does not itself authorize deployment or social publication.
