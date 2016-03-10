
# Stream-Framework-Bench

A real-life benchmark for NoSQL databases. It simulates the use case of powering the newsfeed for a social app. The benchmark is open source and easy to replicate. It uses [Stream-Framework](https://github.com/tschellenbach/stream-framework), the most widely used open source package for building scalable newsfeeds and activity streams. 

# Running the benchmark

Note that running a benchmark can be expensive. 

## Setup your development environment

```
git clone https://github.com/GetStream/Stream-Framework-Bench.git
```

Create a new python virtual env

```
mkvirtualenv bench
```

Install the dependencies

```
pip install -r requirements
```

Ensure you have your AWS cli [installed and configured](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).

Configure your [credentials file](https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration)

Change the key pair name used for starting the instances by editing stack.template

## Start the cluster

Start the cluster on AWS (warning, this is expensive)

```
fab create_stack:stack=cassandra
```

You can view the progress in your Cloudformation dashboard.
Note that cloud-init will take a while to run. (cassandra-driver takes a while to install)

## Running the benchmark using stream framework

```
fab run_bench:stack=cassandra
```

The benchmark will slowly increase the number of users in the graph
and measure:

* The time it takes to read a feed
* The fanout delay for feed updates

## Stopping the stack

fab delete_stack:stack=cassandra

# Testing another NoSQL database

Fork Stream-Framework
https://github.com/tschellenbach/stream-framework

Implement your own storage backend

Fork Stream-Framework-Bench

Update requirements.txt and reference your Stream-Framework fork

Copy the cassandra.json cloudformation file and make the required changes

# Benchmarks using Stream-Framework-Bench

* HighScalability post

# A typical stack

A stack will typically start several components

* RabbitMQ (message queue) & Admin instance - 1 large node
* Task workers/ Celery - An autoscaling group of task workers
* A cluster of your database instances - 3 by default

# Development tips

* Running a celery worker locally 

```
celery -A benchmark worker -l debug
```

* Set CELERY_ALWAYS_EAGER to False
