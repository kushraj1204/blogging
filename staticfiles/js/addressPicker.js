class addressPicker {
    constructor(props) {
        this.map = '';
        this.infoWindow = '';
        this.marker = '';
        this.address = '';
        this.autocomplete = '';
        this.geocoder = '';
        this.pos = {
            lat: props.lat,
            lng: props.lng
        };
        this.mapid = props.mapid;
        this.addressid = props.addressid;
        this.latid = props.latid;
        this.lngid = props.lngid;
        this.initMap();
    }


    initMap() {
        this.geocoder = new google.maps.Geocoder;
        this.map = new google.maps.Map(
            document.getElementById(this.mapid), {
                zoom: 14,
                center: this.pos
            });
        this.detectLocation();
        this.autocomplete = new google.maps.places.Autocomplete(document.getElementById('address'));
        this.places = new google.maps.places.PlacesService(this.map);
        this.autocomplete.addListener('place_changed', this.onPlaceChanged);
    }

    detectLocation() {
        this.infoWindow = new google.maps.InfoWindow;
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                this.pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                this.infoWindow.setPosition(pos);
                document.getElementById(this.latid).value = this.pos.lat;
                document.getElementById(this.lngid).value = this.pos.lng;
                this.marker = new google.maps.Marker({
                    position: this.pos,
                    map: this.map,
                    draggable: true
                });
                this.marker.addListener('dragend', this.handleEvent);
                this.map.setCenter(this.pos);
            }, function () {
                this.handleLocationError(true, this.infoWindow, this.map.getCenter());
            });
        } else {
            // Browser doesn't support Geolocation
            this.handleLocationError(false, this.infoWindow, this.map.getCenter());
        }
    }

    handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
            'Error: The Geolocation service failed.' :
            'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(this.map);
    }

    handleEvent(event) {
        document.getElementById('latitude').value = event.latLng.lat();
        document.getElementById('longitude').value = event.latLng.lng();
        geocodeLatLng(event.latLng.lat(), event.latLng.lng());
    }

    onPlaceChanged() {
        var place = this.autocomplete.getPlace();
        if (place.geometry) {
            map.panTo(place.geometry.location);
            let latlng = new google.maps.LatLng(map.getCenter().lat(), map.getCenter().lng());
            marker.setPosition(latlng);
            document.getElementById('latitude').value = map.getCenter().lat();
            document.getElementById('longitude').value = map.getCenter().lng();
            map.setZoom(14);
        } else {
            document.getElementById('autocomplete').placeholder = 'Enter a city';
        }
    }

    geocodeLatLng(lat, lng) {
        var latlng = {lat: lat, lng: lng};
        this.geocoder.geocode({'location': latlng}, function (results, status) {
            if (status === 'OK') {
                if (results[0]) {
                    document.getElementById(this.addressId).value = results[0].formatted_address;
                } else {
                    window.alert('Error parsing Address');
                }
            } else {
                window.alert('Geocoder failed due to: ' + status);
            }
        });
    }


}

