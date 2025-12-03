import time
import logging


class RateLimiter:
    """Utility class to limit the rate of requests"""
    
    def __init__(self, max_requests_per_second):
        self.max_requests_per_second = max_requests_per_second
        self.cronjob_start_time = time.time()
        self.start_limiter_time = time.time()
        self.requests_cnt = 0

    def add_request(self):
        self.requests_cnt += 1
        if self.requests_cnt % self.max_requests_per_second == 0:
            self._rate_limiter()

    def _rate_limiter(self):
        elapsed_time = time.time() - self.start_limiter_time
        total_elapsed_time = time.time() - self.cronjob_start_time
        sleep_time = max(1 - elapsed_time, 0)
        time.sleep(sleep_time)
        self.start_limiter_time = time.time()
        logging.info(
            f"Total Requests made: {self.requests_cnt}, Total Time Elapsed: {total_elapsed_time}")
