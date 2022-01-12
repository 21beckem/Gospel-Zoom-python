function _(x) {return document.getElementById(x);}
const IPaddrTxt =_('IPaddrTxt');
const QRcontainer = _('QRcontainer');
const HandShakeEl = _('handshake');

eel.expose(setHandshake);
function setHandshake(shake) {
    HandShakeEl.innerHTML = '<a>HandShake</a><br>' + shake;
}
eel.expose(webinarEnded);
function webinarEnded() {
    HandShakeEl.innerHTML = '<a>HandShake</a><br>';
}
eel.expose(remoteConnected);
function remoteConnected() {
    console.log('remote opened');
    QRcontainer.style.display = 'none';
}
eel.expose(setIPconnectionQR);
function setIPconnectionQR(ipAddr) {
    ipAddr = JSON.parse(ipAddr);
    new QRCode(_("remoteUrlQR"), 'http://' + ipAddr.join(':'));
    IPaddrTxt.innerHTML = '<u>' + ipAddr.join('</u> : <u>') + '</u>';
}