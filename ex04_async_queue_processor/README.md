# Exercise 04 – Async Queue Processor (Workshop Version)

**Goal**  
Practice Python's `async` / `await`, batching, and concurrency.  
Simulate a simple queue processing service (similar to Azure Queue / Service Bus).

---

## 🧩 Scenario

We simulate a queue:

- `InMemoryQueue` – holds a list of string messages.
- `receive_batch` – async method that pops up to N messages.
- `process_queue_forever` – async loop that:
  - Receives batches of messages.
  - Processes each message with an async handler.
  - Waits when there are no messages.

This maps nicely to an Azure worker/queue consumer you might write in C#.

---

## 📁 Files in this exercise

- `starter_queue_processor.py` – **you work here** (contains TODOs).
- `solution_queue_processor.py` – reference solution.

Key elements in the starter:

- `MessageHandler` – a `Protocol` describing any async callable that takes a `str`.
- `InMemoryQueue.receive_batch` – **you implement** batch retrieval.
- `process_queue_forever` – **you implement** the processing loop.
- `example_handler` – small demo handler.
- `main()` – runs the queue processing and cancels after a few seconds.

---

## 🛠 Your Tasks

### 1️⃣ Implement `InMemoryQueue.receive_batch(self, batch_size: int) -> list[str]`

Inside this method:

1. Simulate I/O:

   ```python
   await asyncio.sleep(0.1)
   ```

2. If `batch_size <= 0` or there are no messages:

   - Return `[]`.

3. Otherwise:
   - Take up to `batch_size` items from the **front** of `self.messages`.
   - Remove those items from `self.messages`.
   - Return them as a list.

Hints:

- Use slicing: `self.messages[:batch_size]`
- Use `del self.messages[:batch_size]` to remove them.

---

### 2️⃣ Implement `process_queue_forever(...)`

Signature:

```python
async def process_queue_forever(
    queue: InMemoryQueue,
    handler: MessageHandler,
    batch_size: int = 5,
    poll_interval_seconds: float = 1.0,
) -> None:
```

Behavior:

1. Run in an **infinite loop** (`while True`) until cancelled.
2. Each iteration:

   - `batch = await queue.receive_batch(batch_size)`
   - If `batch` is empty:
     - `await asyncio.sleep(poll_interval_seconds)`
     - `continue`
   - If `batch` has messages:

     - Call the handler on each message **concurrently** using `asyncio.gather`, e.g.:

       ```python
       await asyncio.gather(*(handler(msg) for msg in batch))
       ```

3. Wrap the whole loop in `try/except asyncio.CancelledError` and allow graceful shutdown when the task is cancelled.

---

### 3️⃣ Run the script

`main()` already:

- Creates a queue with 10 messages.
- Starts `process_queue_forever` as a background task.
- Waits 5 seconds.
- Cancels the processing task.

Run:

```bash
python starter_queue_processor.py
```

You should see output like:

```text
Processed: msg-0
Processed: msg-1
...
```

---

## 💬 Discussion Points

- How does Python `async`/`await` compare to C# async?
- Why use `asyncio.gather` instead of processing messages sequentially?
- How might this map to processing messages from:
  - Azure Queue Storage
  - Azure Service Bus
  - AWS SQS, etc.

Consider:

- Backpressure: what happens if messages arrive faster than you process them?
- Error handling in handlers: what if one message fails? Do you fail the whole batch?

---

## 📚 Relevant Python Documentation

### 🧵 Async & Concurrency

- `asyncio` (main async framework) → https://docs.python.org/3/library/asyncio.html
- Coroutines & `async` / `await` → https://docs.python.org/3/reference/expressions.html#await
- `asyncio.gather` → https://docs.python.org/3/library/asyncio-task.html#asyncio.gather
- Running async programs with `asyncio.run()` → https://docs.python.org/3/library/asyncio-runner.html#asyncio.run

### 🧱 Types & Protocols

- Dataclasses → https://docs.python.org/3/library/dataclasses.html
- `typing.Protocol` → https://docs.python.org/3/library/typing.html#typing.Protocol
- Type hints in general → https://docs.python.org/3/library/typing.html

### 🧾 General Python

- Functions & `def` → https://docs.python.org/3/tutorial/controlflow.html#defining-functions
- Exceptions → https://docs.python.org/3/tutorial/errors.html

---

By completing this exercise you will:

- Deepen your understanding of Python `async` / `await`.
- Learn to batch and process work concurrently.
- Practice designing clean async APIs that are easy to plug into real queue systems.
