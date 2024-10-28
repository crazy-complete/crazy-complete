# Maintainer: Benjamin Abendroth <braph93@gmx.de>

pkgname=python-crazy-complete
pkgver=0.1.2
pkgrel=1
pkgdesc='Generate shell completion files for all major shells'
arch=('any')
url='https://github.com/crazy-complete/crazy-complete'
license=('GPL-3')
depends=('python' 'python-yaml')
makedepends=(
  'git'
  'python-build'
  'python-installer'
  'python-wheel'
  'python-setuptools-scm'
)

#_commit='f09e930b12081d1afbd06b0376f88040d30a807c'
source=("$pkgname::git+$url") ##commit=$_commit")
b2sums=('SKIP')

build() {
  cd "$pkgname"

  python -m build --wheel --no-isolation

  local site_packages=$(python -c "import site; print(site.getsitepackages()[0])")

  # install to temporary directory
  python -m installer --destdir="$PWD/tmp_install" dist/*.whl

  export PYTHONPATH="$PWD/tmp_install$site_packages"
}

package() {
  cd "$pkgname"

  python -m installer --destdir="$pkgdir" dist/*.whl

  #  # completions
  #  install -vDm644 bash.completion "$pkgdir/usr/share/bash-completion/completions/shtab"
  #  install -vDm644 zsh.completion "$pkgdir/usr/share/zsh/site-functions/_shtab"

  #  # symlink license file
  #  local site_packages=$(python -c "import site; print(site.getsitepackages()[0])")
  #  install -d "$pkgdir/usr/share/licenses/$pkgname"
  #  ln -s "$site_packages/${pkgname#python-}-$pkgver.dist-info/LICENCE" \
  #    "$pkgdir/usr/share/licenses/$pkgname/LICENCE"
}
