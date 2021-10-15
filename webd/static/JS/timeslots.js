function genDays(){
    var no =document.getElementsByName('no_of_classes')[0].value;
    if (no<1 || no>5){
        no=0
        alert("Enter number between 1 to 5")
    }
    var container=document.getElementsByName('dummy')[0];
    while(container.firstChild){
        container.removeChild(container.firstChild);
    }
    for(var i=0;i<no;i++){
        var rowdiv = document.createElement("div");
        rowdiv.className="row g-3";
        rowdiv.id="beside";

        var coldiv1 = document.createElement("div");
        coldiv1.className="col";
        var formdiv1 = document.createElement("div");
        formdiv1.className="form-floating";
        var day_select = document.createElement("select");
        day_select.name= `day_select_${i+1}`;
        day_select.className="form-select";
        day_select.id="day";
        var label1 = document.createElement("label");
        label1.for=`day_select_${i+1}`;
        label1.textContent=`Class ${i+1} Day`;
        var option=document.createElement("option");
        option.selected=true;
        option.text="Select Day";
        day_select.appendChild(option);

        const week=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
        for(var j=0;j<week.length;j++){
            var option=document.createElement("option");
            option.value=`${week[j]}`;
            option.text=`${week[j]}`;
            day_select.appendChild(option);
        }

        formdiv1.appendChild(day_select);
        formdiv1.appendChild(label1);
        coldiv1.appendChild(formdiv1);
        var coldiv2 = document.createElement("div");
        coldiv2.className="col";
        var formdiv2 = document.createElement("div");
        formdiv2.className="form-floating";
        var time_select = document.createElement("select");
        time_select.name= `time_select_${i+1}`;
        time_select.className="form-select";
        var label2 = document.createElement("label");
        label2.for=`time_select_${i+1}`;
        label2.textContent=`Class ${i+1} Time`;
        var option=document.createElement("option");
        option.selected=true;
        option.text="Select Time";
        time_select.appendChild(option);

        formdiv2.appendChild(time_select);
        formdiv2.appendChild(label2);
        coldiv2.appendChild(formdiv2);

        rowdiv.appendChild(coldiv1);
        rowdiv.appendChild(coldiv2);
        container.appendChild(rowdiv);
    }
}
$(document).on("change", "#day", function(){
    var day=this.value;
    var str=this.name;
    var year = document.getElementsByName("year")[0].value;
    var sem  = document.getElementsByName("sem")[0].value;
    str=str.replace('day_select_','');
    var time_str="time_select_";
    time_str=time_str.concat(str);
    var container=document.getElementsByName(time_str)[0];
    while(container.firstChild){
        container.removeChild(container.firstChild);
    }
    lmao(day, year, sem);
    console.log(day);
    function lmao(day, year, sem){
        $.ajax({
            type: 'GET',
            url: '/gettime',
            data:{ day: day, year: year, sem : sem},
            success: function(data) {
                obj=JSON.parse(data);
                for(i=0;i<obj.length;i++){
                    var option=document.createElement("option");
                    option.value=obj[i];
                    option.text=obj[i];
                    container.appendChild(option);
                }
            }
        });
    }

});