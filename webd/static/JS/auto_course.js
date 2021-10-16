  $(document).on("change", "#dept", function(){
        var dept=this.value;
        var container=document.getElementsByName("cou")[0];
        while(container.firstChild){
            container.removeChild(container.firstChild);
        }
        lmao2(dept);
        function lmao2(dept){
            $.ajax({
                type: 'GET',
                url: '/getcou',
                data:{ dept: dept},
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





  function getYear(){
    var year=document.getElementsByName('from_year')[0].value;
    var to=document.getElementsByName('to_year')[0];
    while(to.firstChild){
            to.removeChild(to.firstChild);
        }
    var selected_option=document.createElement("option");
    selected_option.selected=true;
    selected_option.text="To";
    to.appendChild(selected_option);
    for(var i=year;i<=2021;i++){
      var option=document.createElement("option");
      option.value=i;
      option.text=`${i}`;
      to.appendChild(option);
    }
  }
