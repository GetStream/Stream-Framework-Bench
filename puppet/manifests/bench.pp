include base_server


node default {
    notice("Detected role: ${role}")

    case $role {
      rabbitmq: { include bench_rabbitmq }
      celery: { include bench_celery }
    }
}
