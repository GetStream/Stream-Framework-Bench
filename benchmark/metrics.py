from stream_framework.metrics.statsd import StatsdMetrics


class BenchMetrics(StatsdMetrics):
    def on_day_change(self, day):
        self.statsd.gauge('day', day)
        
    def on_network_size_change(self, new_size):
        self.statsd.gauge('network_size', new_size)