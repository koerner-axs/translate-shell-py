# Maintainer: lambdabraham
pkgname=translate-shell-py
pkgver=0.1.0
pkgrel=1
pkgdesc="Translation CLI tool with TTS and interactive shell"
arch=('any')
#url="https://github.com/koerner-axs/translate-shell-py"
license=('MIT')
depends=('python' 'python-requests' 'python-termcolor')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-setuptools')
# source=("$pkgname-$pkgver.tar.gz::https://github.com/koerner-axs/translate-shell-py/archive/v$pkgver.tar.gz")
source=("file://$PWD")
sha256sums=('SKIP')  # For local development, replace with actual checksum for AUR


build() {
    cd "$startdir"
    python -m build --wheel --no-isolation
}

package() {
    cd "$startdir"
    python -m installer --destdir="$pkgdir" dist/*.whl
}
