# TODO tech

* Instance configuration via Puppet or shell (Rabbit & Celery workers)
* Verify Cassandra, Cassandra3 and ScyllaDB instances work
* Verify Stream-Framwork test suite passes against ScyllaDB
* Making sure the instances can find RabbitMQ and Cassandra
* Add tracking metrics for read time and fanout delay
* Store the tracking metrics (redis/cloudwatch?)
* Find a way to visualize those metrics
* Test the assumption that 1 RabbitMQ instance with 1 python script and 20ish celery workers can generate enough load

# TODO tech - phase 2

* Create a backend for Aerospike
* Simplify the process for adding backends and document it well


# TODO promotion

* Improve the readme for this project
* Write the blogpost
* Contact ScyllaDB
* Contact Datastax
