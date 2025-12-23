# Chaos Testbed

This folder contains ideas/scripts to run chaos tests against the local docker-compose stack.

Examples:

- Stop `kafka` container during ingestion to validate producer retries.
- Kill `spark` job to confirm checkpointing and resume.
