import time
from django.test import TestCase
from api.utilities.cache import ttl_cache, _ttl_hash_gen

@ttl_cache(ttl=5)
def test_function(x):
    time.sleep(3)  # Simulate a delay
    return x

class TTLCacheTestCase(TestCase):
    def test_ttl_cache(self):
        start_time = time.time()
        self.assertEqual(test_function(1), 1)
        first_call_duration = time.time() - start_time

        start_time = time.time()
        self.assertEqual(test_function(1), 1)
        second_call_duration = time.time() - start_time

        # The second call should be faster due to caching
        self.assertTrue(first_call_duration > 3)
        self.assertTrue(second_call_duration < 1)

        # Wait for the TTL to expire
        time.sleep(6)

        start_time = time.time()
        self.assertEqual(test_function(1), 1)
        third_call_duration = time.time() - start_time

        # The third call should be slower as the cache has expired
        self.assertTrue(third_call_duration > 3)

    def test_ttl_hash_gen(self):
        gen = _ttl_hash_gen(2)
        
        first_hash = next(gen)
        time.sleep(1)
        second_hash = next(gen)
        self.assertEqual(first_hash, second_hash, "Hashes should be the same within the TTL period")
        
        time.sleep(2)
        third_hash = next(gen)
        self.assertNotEqual(second_hash, third_hash, "Hashes should be different after the TTL period")

