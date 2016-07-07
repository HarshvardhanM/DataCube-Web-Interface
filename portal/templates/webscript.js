		document.getElementById("input_year").value = 1995;
		document.getElementById("input_layer").value = 1;
		document.getElementById("product").value = "Reflectance";
		document.getElementById("id_epsg").value = 32644;
		var year=1990, layer=1, prod="Reflectance", x1, x2, y1, y2,epsg,bounds;
		function showValue(obj){
			if (obj.id=="input_year") {
			document.getElementById("result").innerHTML=obj.value;
			 year=obj.value;
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
	    	  	center: {lat:29.8543441, lng: 78.8339968},
	    	    zoom: 13
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
	    function bound(){
	    	console.log(map.getBounds())
	    	var x = map.getBounds().toJSON()
	    	console.log()
	    	$.ajax({
			type: "POST",
			url: "/ajax/",
			dataType: "json",
			async: true,
			data: {
				csrfmiddlewaretoken: '{{csrf_token}}',
				bounds:x,
				  }
			});
	    }


		function funct(){
			x1=document.getElementById("id_x1").value;
			x2=document.getElementById("id_x2").value;
			y1=document.getElementById("id_y1").value;
			y2=document.getElementById("id_y2").value;
			year=document.getElementById("input_year").value;
			layer=document.getElementById("input_layer").value;
			prod=document.getElementById("product").value;
			epsg = document.getElementById("id_epsg").value;
			bounds = map.getBounds().toJSON()
			// if(x1==null||x1==""||x2==null||x2==""||y1==null||y1==""||y2==null||y2=="")
			// 	alert("Please fill missing fields!");
			console.log("Here")
			$.ajax({
			type: "POST",
			url: "/ajax/",
			dataType: "json",
			async: true,
			data: {
				csrfmiddlewaretoken: '{{csrf_token}}',
				x1:x1,
				x2:x2,
				y1:y1,
				y2:y2,
				year:year,
				layer:layer,
				prod:prod,
				epsg:epsg,
			},
			success: function(data) {
				if(data.status == 1){
					document.getElementById("image_data").src = data.message;
				}    			
			}	
			
			});
		}