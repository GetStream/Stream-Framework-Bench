# Stream-Framework-Bench
An open source and easy to replicate benchmark for NoSQL databases using Stream-Framework.
Stream-Framework is the most widely used open source package for building scalable newsfeeds and activity streams.

# Starting a stack

Create a new python virtual env
mkvirtualenv bench

Install the dependencies
pip install -r requirements

Configure your credentials file
https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration

Start the cluster on AWS (warning, this is expensive)
fab launch_stack cassandra

# Running the benchmark using stream framework

fab start_bench cassandra

# Stopping the stack

go to your AWS cloudformation dashboard and shut down the stack.
(be careful not to shutdown the wrong stack)

# Testing a different database backend

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

* Admin instance - This instance launches the benchmark
* RabbitMQ (message queue) - 1 large node
* Task workers/ Celery - An autoscaling group of task workers
* A cluster of your database instances - 3 by default

# The benchmark script

* The benchmark runs for either flat or aggregated feeds. Aggregated feeds are heavier on the cluster.
