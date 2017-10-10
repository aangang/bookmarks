(function(){ 
    if(window.myBookmarklet!==undefined){ 
        myBookmarklet(); 
    } else{ 
        document.body.appendChild(document.createElement('script')).src='http://127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999); 
    } 
})();


//because some browser can not support so,
//handly add this js code to bookmark of browser
//javascript:(function(){if(window.myBookmarklet!==undefined){myBookmarklet(); } else{document.body.appendChild(document.createElement('script')).src='http://127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999); } })();
