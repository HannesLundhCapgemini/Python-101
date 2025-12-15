from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Protocol


class MessageHandler(Protocol):
    """
    Protocol for message handling.

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
        """
        Pop up to batch_size messages from the queue.

        - Take up to batch_size items from self.messages.
        - Remove them from the list.
        - Return them.

        Simulates network I/O with asyncio.sleep.
        """
        await asyncio.sleep(0.1)

        if batch_size <= 0 or not self.messages:
            return []

        batch = self.messages[:batch_size]
        # Remove the messages we just returned
        del self.messages[:batch_size]
        return batch


async def process_queue_forever(
    queue: InMemoryQueue,
    handler: MessageHandler,
    batch_size: int = 5,
    poll_interval_seconds: float = 1.0,
) -> None:
    """
    Continuously:
      - Fetch a batch of messages.
      - Process each message using the handler.
      - Wait poll_interval_seconds when there are no messages.

    Stops only when the task is cancelled (CancelledError).
    """
    try:
        while True:
            batch = await queue.receive_batch(batch_size)
            if not batch:
                await asyncio.sleep(poll_interval_seconds)
                continue

            # Process each message concurrently with the handler
            tasks = [handler(message) for message in batch]
            await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        # allow graceful shutdown
        return


async def example_handler(message: str) -> None:
    """Simple message handler for demo purposes."""
    await asyncio.sleep(0.2)
    print(f"Processed: {message}")


async def main() -> None:
    """
    Manual test:
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
