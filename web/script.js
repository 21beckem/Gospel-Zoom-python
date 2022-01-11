function _(x) {return document.getElementById(x);}
const remoteUrlQR = _('remoteUrlQR');
const HandShakeEl = _('handshake');

new QRCode(_("remoteUrlQR"), 'https://21beckem.github.io/Gospel-Zoom/remote/');

eel.expose(setHandshake);
function setHandshake(shake) {
    HandShakeEl.innerHTML = shake;
}
eel.expose(webinarEnded);
function webinarEnded() {
    HandShakeEl.innerHTML = '';
}
eel.expose(remoteConnected);
function remoteConnected() {
    console.log('remote opened');
}
eel.expose(setIPconnectionQR);
function setIPconnectionQR(ipAddr) {
    new QRCode(_("IPqrcode"), ipAddr);
}