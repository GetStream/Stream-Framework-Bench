class base_server {

    $programs = [
      'git-core', 
      'gcc',
      'python-dev',
      'libev4',
      'libev-dev',
      'python-pip',
    ]

    package { $programs: 
        ensure => 'present',
    }

}