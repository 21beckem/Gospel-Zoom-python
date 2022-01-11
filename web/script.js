function _(x) {return document.getElementById(x);}
const HandShakeEl = _('handshake');
function StartZoomMeeting() {
    eel.set_handshake();
}

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