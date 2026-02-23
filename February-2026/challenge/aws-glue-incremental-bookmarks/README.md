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

## Submission Instructions
1. Fork this repository and complete the February 2026 challenge, then push your changes to your fork.
2. Write and publish a blog post explaining your approach, learnings, and implementation. Include the blog link in your submission form.
3. Submit Here [Form](https://forms.gle/BtjxwxspdiFow8y16)
4. Last day for submission is 15th March 2026

## Optional Enhancements
Participants are encouraged to go beyond the core requirements and extend the solution with additional features if they’d like.

Adding enhancements is not mandatory, but it’s a great way to showcase deeper understanding, creativity, and production thinking.

💡 Examples of Enhancements
1. Partition the curated dataset for better query performance
2. Add data quality checks or validations
3. Implement alerting or monitoring
4. Handle late-arriving or updated records
5. Provide infrastructure as code (CDK/Terraform)
6. Add dashboards or query examples

Submissions that include thoughtful enhancements may receive additional recognition.

## References
1. https://www.youtube.com/watch?v=9HN6oWJBHtc
2. https://medium.com/@abinayasv/incremental-data-processing-with-glue-bookmark-3cb9e8a26b14
