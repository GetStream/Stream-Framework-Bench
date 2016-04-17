

benchmark_dict = dict()
def register_benchmark(benchmark_class):
    benchmark_dict[benchmark_class.name] = benchmark_class

def get_benchmark(benchmark_name):
    return benchmark_dict[benchmark_name]


class StreamBenchV1(object):
    '''
    Fixed configuration for the benchmark
    Ensures we can run the exact same benchmarks
    '''
    name = 'stream_bench_v1'
    
    network_size = 10000
    max_network_size = 10 ** 7
    multiplier = 2
    duration = 10
    
    def get_social_model(self):
        from benchmark.social_model import SocialModelV1
        return SocialModelV1(network_size=self.network_size)
    
register_benchmark(StreamBenchV1)
    
    
class CustomBenchmark(object):
    '''
    Benchmark class for custom benchmarks
    '''
    name = 'stream_bench_custom'
    
    def __init__(self, network_size, max_network_size, multiplier, duration):
        self.network_size = network_size
        self.max_network_size = max_network_size
        self.multiplier = multiplier
        self.duration = duration
   
    def get_social_model(self):
        from benchmark.social_model import SocialModelV1
        return SocialModelV1(network_size=self.network_size)
    
register_benchmark(CustomBenchmark)
    
    
