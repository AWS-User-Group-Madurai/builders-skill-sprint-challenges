# Challenge: Incremental ETL with AWS Glue Job Bookmarks

## Scenario
You are working in a retail analytics team. Raw order events land in S3 throughout the day. Current ETL reloads everything every run, causing higher cost and longer runtime.

Your goal is to build an AWS Glue job that processes only incremental data using **job bookmarks**.

Session reference: **AWS User Group Madurai – "Builders Skill Sprint – Analytics Month"**.

## What You Have in This Starter
- `starter/data/orders_batch_1.json` → baseline input
- `starter/data/orders_batch_2.json` → incremental input to add before second test run
- `starter/glue_incremental_job.py` → minimal Glue script skeleton
- `docs/design.md` and `docs/validation.md` → submission templates

## Step Details (High-Level Only)
1. Create raw and curated S3 paths and upload starter batch 1 into raw.
2. Create Glue job from the starter script and **enable job bookmarks**.
3. Complete transformation logic based on your own assumptions.
4. Run job once and validate baseline output.
5. Add batch 2 data to raw path.
6. Run the same job again and verify only incremental records are processed.
7. Add schedule/trigger for periodic runs.
8. Document your logic and validation evidence in `docs/`.

## Constraints
- Use AWS Glue bookmarks for incremental behavior (mandatory).
- Do not redesign this as full refresh each run.
- Keep solution production-oriented (clear assumptions, repeatable run behavior).

## Deliverables
1. Completed Glue job script.
2. `docs/design.md` with source, target, logic, and schedule choices.
3. `docs/validation.md` with run-by-run incremental proof.
