var prevScrollpos = window.pageYOffset;
var scrl = document.querySelector(".videos");
var sidebar = document.querySelector(".sidebar");
var menu = document.querySelector("#menu");
var acc_cont = document.querySelector(".acc_cont");
var header_search = document.querySelector(".header__search form");

var header = document.querySelector(".header");

scrl.addEventListener("scroll", function () {
  var currentScrollPos = scrl.scrollTop;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0px";
    sidebar.style.top = "3.2rem";
    acc_cont.style.top = "2.1rem";
    header_search.style.top = ".4rem";
  } else {
    document.getElementById("navbar").style.top = "-50px";
    sidebar.style.top = "-39rem";
    acc_cont.style.top = "-30rem";
    header_search.style.top = "-39rem";
  }
  prevScrollpos = currentScrollPos;
});

function crind(vivind) {

  document.querySelector("#ind").value = vivind;
  document.querySelector("#f1").submit();
}
