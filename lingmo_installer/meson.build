pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'lingmo_installer')
gnome = import('gnome')

gnome.compile_resources('lingmo-installer',
  'lingmo-installer.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'lingmo-installer.in',
  output: 'lingmo-installer',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)

configure_file(
  input: 'lingmo-installer-processor.in',
  output: 'lingmo-installer-processor',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)

subdir('defaults')
subdir('layouts')
subdir('core')
subdir('utils')
subdir('views')
subdir('windows')

lingmo_installer_sources = [
  '__init__.py',
  'main.py',
]

install_data(lingmo_installer_sources, install_dir: moduledir)
