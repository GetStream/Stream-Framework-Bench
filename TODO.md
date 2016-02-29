# TODO tech


## cassandra.template

* Security group setup via cloudformation 
* Instance discovery (how do celery and rabbit know where to find the cassandra nodes?)
* Instance configuration via cloud-init (Rabbit & Celery workers, almost done)


## other steps

* Add tracking metrics for read time and fanout delay
* Store the tracking metrics (redis/cloudwatch?)
* Find a way to visualize those metrics
* Test the assumption that 1 RabbitMQ instance with 1 python script and 20ish celery workers can generate enough load

# TODO tech - phase 2

* Simplify the process for adding backends and document it well


# TODO promotion

* Improve the readme for this project
* Write the blogpost
* Contact ScyllaDB
* Contact Datastax
