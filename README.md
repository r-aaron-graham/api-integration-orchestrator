# API Integration Orchestrator

This repository demonstrates a simple orchestrator for chaining together API calls.  Many
business processes require fetching data from one API, transforming it, and sending it to
another service.  This orchestrator provides a structured way to define such workflows using
asynchronous functions and dependency graphs.

## Key concepts

* **Task** – An atomic unit of work representing an API call or computation.
* **Workflow** – A composition of tasks with dependencies between them.  The orchestrator
  ensures tasks run in the correct order and propagates results to downstream tasks.
* **Async execution** – All tasks are asynchronous functions executed concurrently where
  possible.

## Example

The included `orchestrator.py` defines a small workflow that fetches user data from a mock
CRM API, enriches it using a mock enrichment service, and posts the result to a billing
system.  Run the example with:

```bash
pip install -r requirements.txt
python orchestrator.py
```

You should see the orchestrator execute the tasks in the proper sequence and print the
results.

## Extending

To use this orchestrator in your own projects, subclass `Task` to implement your API calls
and construct a `Workflow` by specifying task dependencies.  Real‑world orchestrators may
use frameworks like Apache Airflow or Prefect for more advanced features; this example is
designed to illustrate the underlying concepts in a lightweight way.