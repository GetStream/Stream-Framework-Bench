class base_server {
  $virtualenvdir = '/opt/stream'
  $user = "streambench"
  $group = $user

  $programs = [
    'git-core',
    'gcc',
    'python-dev',
    'libev4',
    'libev-dev',
    'python-pip',
  ]

  package { $programs:
    ensure => 'present'
  }

  file { $virtualenvdir:
    ensure => 'directory',
    owner  => $user
  }

  python::pip { 'virtualenvwrapper':
    virtualenv => $virtualenvdir,
    owner      => $user,
    require    => [Class['python'], File[$virtualenvdir]]
  }

  python::virtualenv { $virtualenvdir:
    ensure       => present,
    version      => 'system',
    systempkgs   => true,
    distribute   => false,
    owner        => $user,
    group        => $group,
    cwd          => $virtualenvdir,
    timeout      => 0,
    require      => Python::Pip['virtualenvwrapper']
  }
}