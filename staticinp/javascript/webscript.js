document.getElementById("input_year").value = 1995;
document.getElementById("input_layer").value = 1;
document.getElementById("product").value = "Reflectance";
document.getElementById("algo").value = "None";
document.getElementById("id_epsg").value = 32644;
var year=1990, layer=1, prod="Reflectance", x1, x2, y1, y2,epsg,bounds,algo;
function showValue(obj){
if (obj.id=="input_year") {
	if (obj.value==1985){
		document.getElementById("result").innerHTML=parseInt(obj.value)+4;
		year=parseInt(obj.value)+4;
	}else if(obj.value==2005){
		document.getElementById("result").innerHTML=parseInt(obj.value)-2;
		year=parseInt(obj.value)-2;
	}else{
document.getElementById("result").innerHTML=obj.value;
 year=obj.value;
	}
}
if (obj.id=="input_layer") {
document.getElementById("result2").innerHTML=obj.value;
 layer=obj.value;
}
if (obj.id=="product") {
 prod=obj.value;
}

}

var map = null;
function initMap() {
var mapDiv = document.getElementById('map');
map = new google.maps.Map(mapDiv, {	      		
  	center: {lat:29.665, lng: 80.415},
    zoom: 13,
    mapTypeId: google.maps.MapTypeId.SATELLITE
});
map.addListener('bounds_changed', function() {
changebox();
});
}

function changebox(){
var bd = map.getBounds().toJSON()
document.getElementById("id_x1").value = parseFloat(bd["west"]).toFixed(2);
document.getElementById("id_x2").value = parseFloat(bd["east"]).toFixed(2);
document.getElementById("id_y1").value = parseFloat(bd["south"]).toFixed(2);
document.getElementById("id_y2").value = parseFloat(bd["north"]).toFixed(2);
}

function bound(x,y){
 console.log(x,y);
 var center = new google.maps.LatLng(y,x); 
 map.setCenter(center);
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function funct(){
	submit = document.getElementById("id_submit2")
	submit.value = 'Querying...';
	submit.disable = true;
	x1=document.getElementById("id_x1").value;
	x2=document.getElementById("id_x2").value;
	y1=document.getElementById("id_y1").value;
	y2=document.getElementById("id_y2").value;
	year=document.getElementById("input_year").value;
	if (year==1985){
		document.getElementById("result").innerHTML=parseInt(year)+4;
		year=parseInt(year)+4;
	}else if(year==2005){
		document.getElementById("result").innerHTML=parseInt(year)-2;
		year=parseInt(year)-2;
	}
	layer=document.getElementById("input_layer").value;
	prod=document.getElementById("product").value;
	algo=document.getElementById("algo").value;
	epsg = document.getElementById("id_epsg").value;
	
	// if(x1==null||x1==""||x2==null||x2==""||y1==null||y1==""||y2==null||y2=="")
	// 	alert("Please fill missing fields!");
	console.log("Here")
	$.ajax({
	type: "POST",
	url: "/ajax/",
	dataType: "json",
	async: true,
	data: {
		//csrfmiddlewaretoken: csrf_token,
		x1:x1,
		x2:x2,
		y1:y1,
		y2:y2,
		year:year,
		layer:layer,
		prod:prod,
		algo:algo,
		epsg:epsg
	},	
	success: function(data) {
	submit = document.getElementById("id_submit2")
	submit.value = 'Submit';
	submit.disable = false;
	document.getElementById("image_data").src = data.message;
	},
	error: function(){
	submit = document.getElementById("id_submit2")
	submit.value = 'Submit';
	submit.disable = false;
	document.getElementById("image_data").src = "media/images/nodata.jpg";
	}	

	});
}
