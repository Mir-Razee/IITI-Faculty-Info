function showPass() {
    var x = document.getElementById("pwd");
    if (x.type =="password") {
        x.type = "text";
    } else {
        x.type = "password";
    }

    var cb = document.getElementById('showPwd');
    var label = document.getElementById('pass')
    cb.addEventListener('click',function(evt){
        if(!cb.checked){
            label.innerHTML='Show Password';
        }else{
            label.innerHTML='Hide Password';
        }
    },false);
}