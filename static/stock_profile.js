document.getElementById("pills-home-tab").addEventListener("click",function(e) {
       // e.target is our targetted element.
                   // try doing console.log(e.target.nodeName), it will result LI
       <!-- if(e.target && e.target.nodeName == "LI") {
           console.log(e.target.id + " was clicked");
       } -->

       console.log(e.target.id + " was clicked");

   });
