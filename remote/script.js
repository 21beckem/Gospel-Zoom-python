Storage.prototype.setObject = function(key, value) { 
    this.setItem(key, JSON.stringify(value)); 
}
Storage.prototype.getObject = function(key) { 
    var value = this.getItem(key);
    return value && JSON.parse(value); 
}
let Handshake;
function getHandshake() {
    let shake = localStorage.getObject('Handshake') || [];
    if (shake.length == 1) {
        Handshake = shake[0];
        //handshakeInput.value = Handshake;
        return shake;
    }
}
async function connectToHost() {
    
}
let NavOpen = false;
function _(x) {return document.getElementById(x);}
const sideNav = _("sideNav");
const mainContent = _("mainContent");
const handshakeInput = _('handshakeInput');
const page_home = _('page-home');
const page_handshake = _('page-handshake');
const page_about = _('page-about');
const previewScreenBox = _('previewScreenBox');

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
            page_about.style.display = 'none';
            break;
        case 'handshake':
            page_home.style.display = 'none';
            page_handshake.style.display = 'block';
            page_about.style.display = 'none';
            setTimeout(handshakeInput.focus(), 400);
            getHandshake();
            break;
        case 'about':
            page_home.style.display = 'none';
            page_handshake.style.display = 'none';
            page_about.style.display = 'block';
            break;
        default:
            break;
    }
    closeNav();
}
function refreshPreviewImg() {
    previewScreenBox.style.backgroundImage = 'url(/feed?x=' + Handshake + '&t=' + new Date().getTime() + ')';
}
function handlePreviewToggle(toggleEl) {
    if (toggleEl.checked) {
        refreshPreviewImg();
    } else {
        previewScreenBox.style.backgroundImage = 'url(/churchZoomIcon)';
    }
}
async function sendBtnPress(path) {
    fetch(path + '?x=' + Handshake);
}

function showAlert(alertBoxId, timeMillis=2000) {
    _(alertBoxId).style.opacity = '1';
    setTimeout(function() {
        _(alertBoxId).style.opacity = '0'
    }, timeMillis);
}
function verifyHandshakeLength() {
    if (handshakeInput.value.length > 4) handshakeInput.value = handshakeInput.value.slice(0, 4);
}
function saveHandshake() {
    var toBeSaved = [handshakeInput.value];
    handshakeInput.value = '';
    localStorage.setObject('Handshake', toBeSaved);
    openPage('home');
    showAlert('successBox');
    getHandshake();
}
function detectswipe(el,func) {
  swipe_det = new Object();
  swipe_det.sX = 0; swipe_det.sY = 0; swipe_det.eX = 0; swipe_det.eY = 0;
  var min_x = 30;  //min x swipe for horizontal swipe
  var max_x = 30;  //max x difference for vertical swipe
  var min_y = 50;  //min y swipe for vertical swipe
  var max_y = 60;  //max y difference for horizontal swipe
  var direc = "";
  ele = _(el);
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