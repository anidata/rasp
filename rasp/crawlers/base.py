import asyncio
import random
import copy
import time
from rasp.engines.base import DefaultEngine

__author__ = 'willmcginnis'


class AsyncBoundedCrawler:
    """
    """

    def __init__(self, engine, urls, n_workers=5):
        # The base enigne passed in will be used to create our consumers
        self._engine = engine

        # An asyncio queue is how we communicate with our consumers
        self._queue = asyncio.Queue(maxsize=n_workers)
        self._loop = asyncio.get_event_loop()

        # enqueue our initial data, and start the consumers
        self._producer = self._loop.create_task(self.enqueue_many(urls))
        self._consumers = []
        for idx in range(n_workers):
            self._consumers.append(asyncio.ensure_future(self.consumer('worker_%s' % (idx, ))))

        self._tasks = self._consumers # + [self._producer]

    async def _main(self):
        await asyncio.wait(self._tasks)

    async def enqueue_many(self, urls):
        for url in urls:
            await self._queue.put(url)
        await self._queue.join()
        print('queue finished')

    async def consumer(self, consumer_id):
        print('starting up consumer: %s' % (consumer_id, ))
        engine = copy.deepcopy(self._engine)
        while not self._queue.empty():
            url = await self._queue.get()
            if url is None:
                self._queue.task_done()
                print('shutting down consumer: %s' % (consumer_id, ))
                break
            else:
                wp = engine.get_page_source(url)
                print('%s: %s' % (url, consumer_id, ))
                # for testing
                await asyncio.sleep(random.random())
                self._queue.task_done()
        print('shutting down consumer: %s' % (consumer_id, ))

    def run(self):
        try:
            self._loop.run_until_complete(self._main())
        finally:
            for task in asyncio.Task.all_tasks():
                task.cancel()
            self._loop.close()

    def stop(self):
        self._loop.close()

if __name__ == '__main__':
    # Hacky benchmark
    # - workers=1, range=100, 100.97s
    # - workers=3, range=100, 18.1s
    # - workers=10, range=100, 9.3s

    data = ('https://www.google.com?q=%s' % _ for _ in range(100))
    engine = DefaultEngine()

    start_time = time.time()
    crawler = AsyncBoundedCrawler(engine, data, 10)
    crawler.run()
    end_time = time.time()
    print('%s elapsed' % (end_time - start_time, ))
