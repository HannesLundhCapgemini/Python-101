from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Protocol


class MessageHandler(Protocol):
    """Protocol for message handling.

    Any async callable with this signature can be used
    (similar to an interface in C#).
    """

    async def __call__(self, message: str) -> None:
        ...


@dataclass
class InMemoryQueue:
    """Very small in-memory queue to simulate queue processing."""
    messages: list[str]

    async def receive_batch(self, batch_size: int) -> list[str]:
        """Pop up to batch_size messages from the queue.

        Requirements:

        - Simulate network I/O by awaiting asyncio.sleep(0.1).
        - If batch_size <= 0 or there are no messages, return [].
        - Otherwise:
            - Take up to batch_size items from the front of self.messages.
            - Remove the items you return from self.messages.
            - Return them as a list[str].
        """
        # TODO: implement this method.
        raise NotImplementedError("receive_batch is not implemented yet")


async def process_queue_forever(
    queue: InMemoryQueue,
    handler: MessageHandler,
    batch_size: int = 5,
    poll_interval_seconds: float = 1.0,
) -> None:
    """Continuously process messages from the queue.

    Loop forever until the task is cancelled:

    1. Await queue.receive_batch(batch_size).
    2. If the batch is empty:
         - await asyncio.sleep(poll_interval_seconds)
         - continue
    3. If the batch has messages:
         - Call the handler for each message concurrently using asyncio.gather.
           (i.e. await asyncio.gather(*(handler(m) for m in batch)))
    4. Catch asyncio.CancelledError and allow graceful shutdown.
    """
    # TODO: implement this async loop.
    raise NotImplementedError("process_queue_forever is not implemented yet")


async def example_handler(message: str) -> None:
    """Simple message handler for demo purposes."""
    await asyncio.sleep(0.2)
    print(f"Processed: {message}")


async def main() -> None:
    """Manual test:

    - Creates a queue with 10 messages.
    - Starts processing in the background.
    - Cancels after a few seconds.
    """
    queue = InMemoryQueue(messages=[f"msg-{i}" for i in range(10)])
    task = asyncio.create_task(process_queue_forever(queue, example_handler))

    await asyncio.sleep(5)
    task.cancel()
    await task


if __name__ == "__main__":
    asyncio.run(main())
