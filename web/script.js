function _(x) {return document.getElementById(x);}
String.prototype.toHHMMSS = function () {
    var sec_num = parseInt(this, 10); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours+':'+minutes+':'+seconds;
}
const IPaddrTxt =_('IPaddrTxt');
const QRcontainer = _('QRcontainer');
const HandShakeEl = _('handshake');
const timerContainer = _('timerContainer');
const timerEl = _('timer');

var timeAtWebinarStart, timerInterval;
function setTimer() {
    var len = (new Date() - timeAtWebinarStart) / 1000;
    timerEl.innerHTML = String(Math.floor(len)).toHHMMSS();
}

eel.expose(setHandshake);
function setHandshake(shake) {
    timerContainer.style.display = 'block';
    timeAtWebinarStart = new Date();
    timerInterval = setInterval(setTimer, 1000);
    HandShakeEl.innerHTML = '<a>HandShake</a><br>' + shake;
}
eel.expose(webinarEnded);
function webinarEnded() {
    timerContainer.style.display = 'none';
    clearInterval(timerInterval);
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