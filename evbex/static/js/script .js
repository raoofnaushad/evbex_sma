// Code for displaying and hiding overlay.
body = document.querySelector("body");
const overlay = document.querySelector(".dark-overlay");

function openOverlay(){
    overlay.style.display = "block";
    body.style.overflow = "hidden";
}
function closeOverlay(){
    overlay.style.display = "none";
    body.style.overflowY = "unset";
    body.style.overflowX = "hidden";
}


//Code for displaying Subscribe popup when button is clicked and hiding popup when cancel button is clicked
// const subscribePopup = document.querySelector(".subscribe-popup");
// var scroll_y;
// window.addEventListener("scroll", function(event) {  
//     var scroll_y = this.scrollY;
//     overlay.style.top =  scroll_y + 'px';
//     subscribePopup.style.top =  scroll_y + 'px';
// });
// function displaySubscribePopup(){
//     openOverlay();
//     subscribePopup.style.display = "flex";
// }
// function hideSubscribePopup(){
//     closeOverlay();
//     subscribePopup.style.display = "none";
// }


const adsPopup = document.querySelector(".ads-popup");
//Code for displaying Subscribe popup when button is clicked and hiding popup when cancel button is clicked
//Code for the unsubscribe popup

const subscribePopup = document.querySelector(".subscribe-popup");
const unsubscribePopup = document.querySelector(".unsubscribe-popup");
var scroll_y;
window.addEventListener("scroll", function(event) {  
    var scroll_y = this.scrollY;
    overlay.style.top =  scroll_y + 'px';
    subscribePopup.style.top =  scroll_y + 'px';
    unsubscribePopup.style.top =  scroll_y + 'px';
    adsPopup.style.top =  scroll_y + 'px';
});
function displaySubscribePopup(){
    openOverlay();
    subscribePopup.style.display = "flex";
}
function hideSubscribePopup(){
    closeOverlay();
    subscribePopup.style.display = "none";
}
function displayUnsubscribePopup(){
    openOverlay();
    unsubscribePopup.style.display = "flex";
}
function hideUnsubscribePopup(){
    closeOverlay();
    unsubscribePopup.style.display = "none";
}


//code for hiding subscribe popup when user clicks anywhere outside the popup
overlay.addEventListener("click", function(){
    console.log('print endheenkilum');
    hideSubscribePopup();
});


//code for copying content
// var copyBtn = document.getElementsByClassName("copy-btn");
// for(var i = 0;i<copyBtn.length;i++){
//     copyBtn[i].addEventListener("click",function(){
//         var parent = this.parentElement.parentElement;
//         var content = parent.children[0].children[1].children[1].children[0].innerHTML;
//         var link = parent.children[0].children[1].children[1].children[1].innerHTML;
//         var postableText = content.trim() + '\n' + link.trim();
//         console.log(postableText.trim());
//         navigator.clipboard.writeText(postableText.trim());
//         alert("Post Content Copied to Clipboard"); 
//     });
// }
var copyBtn = document.getElementsByClassName("copy-btn");
for(var i = 0;i<copyBtn.length;i++){
    copyBtn[i].addEventListener("click",function(){
        var postableText = "";
        var parent = this.parentElement.parentElement;
        var content = parent.children[0].children[1].children[1].children[0].innerHTML;
        // var link = parent.children[0].children[1].children[1].children[1].innerHTML;
        // postableText = content.trim() + '\n' + link.trim();
        postableText = content.trim();
        console.log(postableText.trim());
        navigator.clipboard.writeText(postableText.trim());
        alert("Post Content Copied to Clipboard"); 
    });
}


//Code to change date on user wish.
const tapToChange = document.querySelector('.change-date');
const calender = document.querySelector('.calender');
Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});
document.querySelector('.date-set').value = new Date().toDateInputValue();//to display current date in the date picker
function showCalender(){
    calender.style.display = "flex";
    tapToChange.style.display = "none";//to display tapToChange again(normal state) set tapToChange.style.display = "flex";
}


//code for Checking correctness of gmail id entered by user in subscribe popup
const mailInputBox = document.querySelector(".mail");
const nameInputBox = document.querySelector(".name");
const subscribeBtn = document.querySelector(".subscribe-on-popup");
subscribeBtn.style.opacity = 0.5;
subscribeBtn.style.cursor = 'not-allowed';
mailInputBox.value = "";
nameInputBox.value = "";
mailInputBox.addEventListener("keyup",function(){
    var text = mailInputBox.value;
    var flag = "false";    
    const errorMessage = document.querySelector(".error");
    if((text.length>8) && (text.search("@")!= -1) && (text.search(".com")!= -1) && (text.search('.')!= -1) && (text.search(" ") == -1)){
        errorMessage.innerHTML = "Seems correct";
        errorMessage.style.color = "green";
        errorMessage.style.display = "block";
        flag = "true";
    }
    else{
        if(text.length>8){
            errorMessage.style.display = "block";
            errorMessage.innerHTML = "*Invalid Mail Id";
            errorMessage.style.color = "red";
        }
    }
    if(text.length === 0){
        errorMessage.style.display = "none";
    }
    if ((text.length > 0) && (nameInputBox.value.length > 0) && (flag == "true")){
        subscribeBtn.style.opacity = 1;
        subscribeBtn.style.cursor = 'pointer';
    }
});


//back-to-top button 
const toppestElement = document.querySelector(".toppest-element");
const goToTop = () => {
    toppestElement.scrollIntoView({behavior: "smooth", block: "start", inline: "start"});
};


//code to manage 1 post condition
// const posts = document.querySelector(".posts");
// const footer = document.querySelector(".footer");
// const noDataImg = document.querySelector('.no-data');
// var footerPosition = footer.style.position;
// if (posts.childElementCount <= 1){
//     console.log('posts child count' + posts.childElementCount);
//     footer.style.position = "absolute";
//     footer.style.bottom = 0;
//     footer.style.left = 0;
//     footer.style.right = 0;
//     body.style.overflow = "hidden";
// }
// else{
//     footer.style.position = "relative";
// }
// if(posts.childElementCount == 0){
//     noDataImg.style.display = 'flex';
//     posts.style.margin = '150px 0px 10px 0px';

// }

//code to close the success notificication
const successNoti = document.querySelector(".success-message");
function closeSuccessNoti(){
    successNoti.style.display = 'none';
}


//services button dropdown 
const servicesBtn = document.querySelector(".our-services");
const dropDown = document.querySelector(".services-extension");
const primaryNav = document.querySelector(".navbar")
servicesBtn.addEventListener("mouseover",function(){
    dropDown.style.display = "flex";
});
var clickValue = 0;
servicesBtn.addEventListener("click",function(){
    if (clickValue === 0){
        dropDown.style.display = "flex";
        clickValue = 1;
    }
    else{
        dropDown.style.display = "none";
        clickValue = 0;
    }
    
});
primaryNav.addEventListener("mouseleave",function(){
    dropDown.style.display = "none";
});



//code to hide the Ads-Popup
// body.style.overflow = "hidden";
// const adsPopup = document.querySelector(".ads-popup");
// function closeAdsPopup(){
//     adsPopup.style.display = "none";
//     body.style.overflow = "unset";
// }


//code to show adspopup after 10s after refrshing
function displayAdsPopup(){
    body.style.overflow = "hidden";
    adsPopup.style.display = 'flex';
}

const adsVar = document.querySelector(".advar").innerHTML;
if (adsVar ==='1'){
    const timeId = setTimeout(displayAdsPopup,10000);
}


//code to hide the Ads-Popup
function closeAdsPopup(){
    adsPopup.style.display = "none";
    body.style.overflow = "unset";
}


//code for diaplaying evbex originals
var evbexValue = document.getElementsByClassName("evbex-value");
var postTitle = document.getElementsByClassName("evbex-originals-txt");
var lineDiv = document.getElementsByClassName("orginals");
for(var k = 0;k<evbexValue.length;k++){
    if(evbexValue[k].innerHTML === '1'){
        lineDiv[k].style.display = "block";
        postTitle[k].style.display = "inline";
    }
}


//code to move slides as slide show
var hotSlides = document.getElementsByClassName("hot-service-slide");
var slideControls = document.getElementsByClassName("slide-control");
var s = 0;
hotSlides[s].className += " active-hot-service-slide";
slideControls[s].className += " active-slide-control";
var intervalId;
function callSetInterval(){
    intervalId = setInterval(changeSlide,4000);
}
callSetInterval();
function changeSlide(){
    s++;
    if (s == hotSlides.length){
        s = 0;
    }
    hotSlides[s].className += " active-hot-service-slide";
    slideControls[s].className += " active-slide-control";
    if(s == 0){
        hotSlides[hotSlides.length - 1].classList.remove("active-hot-service-slide");
        slideControls[slideControls.length - 1].classList.remove("active-slide-control");
    }
    else{
        hotSlides[s - 1].classList.remove("active-hot-service-slide");
        slideControls[s - 1].classList.remove("active-slide-control");
    }
}
function slideChecker(n){
    for(var l = 0; l < hotSlides.length; l++){
        if(l != n){
            hotSlides[l].classList.remove("active-hot-service-slide");
            slideControls[l].classList.remove("active-slide-control");
        }
    }
}
slideControls[0].addEventListener("click",()=>{
    clearInterval(intervalId);
    if(s == 0){
        hotSlides[hotSlides.length - 1].classList.remove("active-hot-service-slide");
        slideControls[slideControls.length - 1].classList.remove("active-slide-control");
    }
    else{
        hotSlides[s - 1].classList.remove("active-hot-service-slide");
        slideControls[s - 1].classList.remove("active-slide-control");
    }
    s = 0;
    slideChecker(s);
    hotSlides[s].className += " active-hot-service-slide";
    slideControls[s].className += " active-slide-control";
    callSetInterval();
});
slideControls[1].addEventListener("click",()=>{
    clearInterval(intervalId);
    if(s == 0){
        hotSlides[hotSlides.length - 1].classList.remove("active-hot-service-slide");
        slideControls[slideControls.length - 1].classList.remove("active-slide-control");
    }
    else{
        hotSlides[s - 1].classList.remove("active-hot-service-slide");
        slideControls[s - 1].classList.remove("active-slide-control");
    }
    s = 1;
    slideChecker(s);
    hotSlides[s].className += " active-hot-service-slide";
    slideControls[s].className += " active-slide-control";
    callSetInterval();
});
slideControls[2].addEventListener("click",()=>{
    clearInterval(intervalId);
    if(s == 0){
        hotSlides[hotSlides.length - 1].classList.remove("active-hot-service-slide");
        slideControls[slideControls.length - 1].classList.remove("active-slide-control");
    }
    else{
        hotSlides[s - 1].classList.remove("active-hot-service-slide");
        slideControls[s - 1].classList.remove("active-slide-control");
    }
    s = 2;
    slideChecker(s);
    hotSlides[s].className += " active-hot-service-slide";
    slideControls[s].className += " active-slide-control";
    callSetInterval();
});
slideControls[3].addEventListener("click",()=>{
    clearInterval(intervalId);
    if(s == 0){
        hotSlides[hotSlides.length - 1].classList.remove("active-hot-service-slide");
        slideControls[slideControls.length - 1].classList.remove("active-slide-control");
    }
    else{
        hotSlides[s - 1].classList.remove("active-hot-service-slide");
        slideControls[s - 1].classList.remove("active-slide-control");
    }
    s = 3;
    slideChecker(s);
    hotSlides[s].className += " active-hot-service-slide";
    slideControls[s].className += " active-slide-control";
    callSetInterval();
});