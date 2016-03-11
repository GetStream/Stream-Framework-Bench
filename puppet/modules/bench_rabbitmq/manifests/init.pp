class bench_rabbitmq {

    class { "rabbitmq::server":
    }

    rabbitmq_user { 'admin':
        admin    => true,
        password => 'admin',
        provider => "rabbitmqctl",
    }

    rabbitmq_vhost { 'stream':
        ensure => present,
        provider => "rabbitmqctl",
    }

    rabbitmq_user_permissions { 'admin@stream':
        configure_permission => '.*',
        read_permission      => '.*',
        write_permission     => '.*',
        provider => "rabbitmqctl",
    }

    exec { 'rabbitmq-plugins':
        path        => "/usr/bin:/usr/sbin:/bin",
        environment => "HOME=/root",
        command     => "rabbitmq-plugins enable rabbitmq_management",
        require     => Package["rabbitmq-server"]
    }

    file { '/etc/default/rabbitmq-server':
        ensure => "present",
        content => "ulimit -n 100000"
    }
}