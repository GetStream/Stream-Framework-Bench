class bench_celery {

  $virtualenvdir = '/opt/stream'
  $fanout_procs = $::processorcount + 2
  $realtime_procs = $::processorcount / 2
  $celery_default_procs = $::processorcount / 2

}