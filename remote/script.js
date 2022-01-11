Storage.prototype.setObject = function(key, value) { 
    this.setItem(key, JSON.stringify(value)); 
}
Storage.prototype.getObject = function(key) { 
    var value = this.getItem(key);
    return value && JSON.parse(value); 
}
let HostAddr;
let Handshake;
function getHandshake() {
    let shake = localStorage.getObject('Handshake') || [];
    if (shake.length == 1) {
        Handshake = shake[0];
        handshakeInput.value = Handshake;
        return shake;
    }
}
function getHostAddr() {
    let addr = localStorage.getObject('HostAddr') || [];
    if (addr.length == 2) {
        ipInput.value = addr[0];
        portInput.value = addr[1];
    }
    HostAddr = 'http://' + addr.join(':');
    return HostAddr;
}
async function connectToHost() {
    
}
let NavOpen = false;
const sideNav = document.getElementById("sideNav");
const mainContent = document.getElementById("mainContent");
const handshakeInput = document.getElementById('handshakeInput');
const ipInput = document.getElementById('ipInput');
const portInput = document.getElementById('portInput');
const page_home = document.getElementById('page-home');
const page_handshake = document.getElementById('page-handshake');
const page_connect = document.getElementById('page-connect');
const page_qr = document.getElementById('page-qr');
const qrLoader = document.getElementById('qrLoader');

getHostAddr();
getHandshake();

function openNav() {
    sideNav.style.transform = "translateX(0)";
    mainContent.style.transform = "translateX(60%)";
    mainContent.style.marginLeft = "10px";
    document.body.style.backgroundColor = "rgba(0,0,0,0.5)";
    NavOpen = true;
}
function closeNav() {
    sideNav.style.transform = "translateX(calc(-100% - 4px))";
    mainContent.style.transform = "translateX(0)";
    mainContent.style.marginLeft = "0";
    document.body.style.backgroundColor = "white";
    NavOpen = false;
}
function swipeCloseNavbar(el,d) {
    document.activeElement.blur();
    if (NavOpen && d=='l') {
        closeNav();
    }else if (!NavOpen && d=='r') {
        openNav();
    }
}
function openPage(pageName) {
    switch (pageName) {
        case 'home':
            page_home.style.display = 'block';
            page_handshake.style.display = 'none';
            page_connect.style.display = 'none';
            page_qr.style.display = 'none';
            break;
        case 'handshake':
            page_home.style.display = 'none';
            page_handshake.style.display = 'block';
            page_connect.style.display = 'none';
            page_qr.style.display = 'none';
            setTimeout(handshakeInput.focus(), 400);
            getHandshake();
            break;
        case 'connect':
            page_home.style.display = 'none';
            page_handshake.style.display = 'none';
            page_connect.style.display = 'block';
            page_qr.style.display = 'none';
            getHostAddr();
            break;
        case 'qr':
            page_home.style.display = 'none';
            page_handshake.style.display = 'none';
            page_connect.style.display = 'none';
            page_qr.style.display = 'block'; qrLoader.style.display = 'block';
            break;
        default:
            break;
    }
    closeNav();
}
function onScanSuccess(decodedText, decodedResult) {
    let thisData = JSON.parse(decodedText);
    console.log(thisData);
    if (thisData.length == 2) {
        if (typeof thisData[0] === 'string' && typeof thisData[1] === 'number') {
            localStorage.setObject('HostAddr', thisData);
            html5QrCodeScan.stop().then(function() {
                openPage('home')
                showAlert('successBox')
            });
        }
    }
}
function cancelScanning() {
    html5QrCodeScan.stop();
    openPage('connect');
}
let html5QrCodeScan;
function getCameraAccess() {
    openPage('qr')
    Html5Qrcode.getCameras().then(devices => {
        /**
         * devices would be an array of objects of type:
         * { id: "id", label: "label" }
         */
        if (devices && devices.length) {
            var cameraId;
            var foundBack = false;
            for (let i = 0; i < devices.length; i++) {
                if (devices[i].label.toLowerCase().includes("back")) {
                    foundBack = true;
                    cameraId = devices[i].id
                    break;
                }
            }
            if (!foundBack) {
                cameraId = devices[0].id;
            }
            html5QrCodeScan = new Html5Qrcode("qr-preview");
            const config = { fps: 10, qrbox: { width: 250, height: 250 } };
            html5QrCodeScan.start({ facingMode: "environment" }, config, onScanSuccess);
            qrLoader.style.display = 'none';
        }
    }).catch(err => {
        alert(err);
    });
}

function showAlert(alertBoxId, timeMillis=2000) {
    document.getElementById(alertBoxId).style.opacity = '1';
    setTimeout(function() {
        document.getElementById(alertBoxId).style.opacity = '0'
    }, timeMillis);
}
function verifyHandshakeLength() {
    if (handshakeInput.value.length > 4) handshakeInput.value = handshakeInput.value.slice(0, 4);
}
function saveHandshake() {
    var toBeSaved = [handshakeInput.value];
    localStorage.setObject('Handshake', toBeSaved);
    openPage('home');
    showAlert('successBox');
}
function saveAddress() {
    var toBeSaved = [ipInput.value, portInput.value];
    localStorage.setObject('HostAddr', toBeSaved);
    openPage('home');
    showAlert('successBox');
}
function detectswipe(el,func) {
  swipe_det = new Object();
  swipe_det.sX = 0; swipe_det.sY = 0; swipe_det.eX = 0; swipe_det.eY = 0;
  var min_x = 30;  //min x swipe for horizontal swipe
  var max_x = 30;  //max x difference for vertical swipe
  var min_y = 50;  //min y swipe for vertical swipe
  var max_y = 60;  //max y difference for horizontal swipe
  var direc = "";
  ele = document.getElementById(el);
  ele.addEventListener('touchstart',function(e){
    var t = e.touches[0];
    swipe_det.sX = t.screenX; 
    swipe_det.sY = t.screenY;
  },false);
  ele.addEventListener('touchmove',function(e){
    e.preventDefault();
    var t = e.touches[0];
    swipe_det.eX = t.screenX; 
    swipe_det.eY = t.screenY;    
  },false);
  ele.addEventListener('touchend',function(e){
    //horizontal detection
    if ((((swipe_det.eX - min_x > swipe_det.sX) || (swipe_det.eX + min_x < swipe_det.sX)) && ((swipe_det.eY < swipe_det.sY + max_y) && (swipe_det.sY > swipe_det.eY - max_y) && (swipe_det.eX > 0)))) {
      if(swipe_det.eX > swipe_det.sX) direc = "r";
      else direc = "l";
    }
    //vertical detection
    else if ((((swipe_det.eY - min_y > swipe_det.sY) || (swipe_det.eY + min_y < swipe_det.sY)) && ((swipe_det.eX < swipe_det.sX + max_x) && (swipe_det.sX > swipe_det.eX - max_x) && (swipe_det.eY > 0)))) {
      if(swipe_det.eY > swipe_det.sY) direc = "d";
      else direc = "u";
    }

    if (direc != "") {
      if(typeof func == 'function') func(el,direc);
    }
    direc = "";
    swipe_det.sX = 0; swipe_det.sY = 0; swipe_det.eX = 0; swipe_det.eY = 0;
  },false);  
}
detectswipe('mainContent', swipeCloseNavbar);
detectswipe('sideNav', swipeCloseNavbar);