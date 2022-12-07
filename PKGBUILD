pkgname="discordsqueezer"
pkgver="1.0.0"
pkgrel="1"
pkgdesc="Video compression tool for Discord file size limits"
arch=("x86_64")
source=("git+http://github.com/mcharlsto/discordsqueezer.git")
sha512sums=("SKIP")
depends=("python" "python-pip")
makedepends=("git")

package() {
    /usr/bin/pip install PyQt5 ffmpeg-python
    mkdir -p "${pkgdir}/usr/bin"
    cp discordsqueezer/main.py ${pkgdir}/usr/bin/discordsqueezer.py
    cp discordsqueezer/discordsqueezer_ui.py ${pkgdir}/usr/bin/discordsqueezer_ui.py
    mkdir -p "${pkgdir}/usr/share/applications"
    cp discordsqueezer/DiscordSqueezer.desktop ${pkgdir}/usr/share/applications/DiscordSqueezer.desktop
    chmod +x "${pkgdir}/usr/bin/discordsqueezer.py"
}
