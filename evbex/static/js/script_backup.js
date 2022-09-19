// Code for displaying and hiding overlay.
body = document.querySelector("body");
const overlay = document.querySelector(".dark-overlay");

function openOverlay(){
    overlay.style.display = "block";
    body.style.overflow = "hidden";
}
function closeOverlay(){
    overlay.style.display = "none";
    body.style.overflow = "unset";
}


//Code for displaying Subscribe popup when button is clicked and hiding popup when cancel button is clicked
const subscribePopup = document.querySelector(".subscribe-popup");
var scroll_y;
window.addEventListener("scroll", function(event) {  
    var scroll_y = this.scrollY;
    overlay.style.top =  scroll_y + 'px';
    subscribePopup.style.top =  scroll_y + 'px';
});
function displaySubscribePopup(){
    openOverlay();
    subscribePopup.style.display = "flex";
}
function hideSubscribePopup(){
    closeOverlay();
    subscribePopup.style.display = "none";
}


//code for hiding subscribe popup when user clicks anywhere outside the popup
overlay.addEventListener("click", function(){
    console.log('print endheenkilum');
    hideSubscribePopup();
});


//code for copying content
var copyBtn = document.getElementsByClassName("copy-btn");
for(var i = 0;i<copyBtn.length;i++){
    copyBtn[i].addEventListener("click",function(){
        var parent = this.parentElement.parentElement;
        var content = parent.children[0].children[1].children[1].children[0].innerHTML;
        navigator.clipboard.writeText(content);
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
    if((text.length>8) && (text.search("@")!= -1) && (text.search(".com")!= -1) && (text.search('.')!= -1) && (text.search("mail")!= -1) && (text.search(" ") == -1)){
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
const posts = document.querySelector(".posts");
const footer = document.querySelector(".footer");
const noDataImg = document.querySelector('.no-data');
var footerPosition = footer.style.position;
if (posts.childElementCount <= 1){
    console.log('posts child count' + posts.childElementCount);
    footer.style.position = "absolute";
    footer.style.bottom = 0;
    footer.style.left = 0;
    footer.style.right = 0;
    body.style.overflow = "hidden";
}
else{
    footer.style.position = "relative";
}
if(posts.childElementCount == 0){
    noDataImg.style.display = 'flex';
    posts.style.margin = '150px 0px 10px 0px';

}
