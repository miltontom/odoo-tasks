$(document).ready(function () {
    $("#locationInput").keypress(function (e) {
        let key = e.keyCode

        if (key == 13) {
            $("#searchButton").trigger("click")
        }
    })

    let locationG = ""
    let tempCG = ""
    let tempFG = ""
    let latG = ""
    let lonG = ""

    $("#searchButton").click(function () {
        let location = $("#locationInput").val()

        if (location === "") {
        } else {
            const apiKey = "4afd3bfc045a403dbd754111251505"
            const apiUrl = "http://api.weatherapi.com/v1/current.json"
            const completeurl = `${apiUrl}?q=${location}&key=${apiKey}`

            $.ajax({
                url: completeurl,
                method: 'get',
                success: function (data) {
                    $("#location").show()
                    $("#coordinates").show()
                    $("#temperature").show()
                    locationG = data.location.name + ", " + data.location.region
                    tempCG = data.current.temp_c
                    tempFG = data.current.temp_f
                    latG = data.location.lat
                    lonG = data.location.lon
                    $("#location").html(locationG)
                    if (!fahrenheitEnabled) {
                        $("#temperature").html(tempCG + "\u00B0" + "&nbsp" + "C")
                        fahrenheitEnabled = false
                    } else {
                        $("#temperature").html(tempFG + "\u00B0" + "&nbsp" + "F")
                        fahrenheitEnabled = true
                    }
                    $("#coordinates").html(`<b>Latitude</b>: ${latG}&nbsp;&nbsp;<b>Longitude</b>: ${lonG}`)
                },
                error: function (error) {
                    $("#errorModal").modal('show')
                    $("#location").hide()
                    $("#temperature").hide()
                    $("#coordinates").hide()
                }
            })
        }
    })

    $("#currLocButton").click(function () {
        let lat = ""
        let lon = ""

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(success, error);
        } else {
            x.innerHTML = "Geolocation is not supported by this browser.";
        }

        function success(position) {
            lat = position.coords.latitude
            lon = position.coords.longitude
            const currWeatherUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=133c7ba2e358c8f1358aa62325651784&units=metric`
            $.ajax({
                url: currWeatherUrl,
                method: 'get',
                success: function (data) {
                    console.log(data.name)
                    console.log(data.main.temp)
                    console.log(data.coord.lat)
                    console.log(data.coord.lon)
                    $("#location").show()
                    $("#coordinates").show()
                    $("#temperature").show()
                    locationG = data.name
                    tempCG = data.main.temp
                    tempFG = (tempCG * (9/5) + 32)
                    latG = data.coord.lat
                    lonG = data.coord.lon
                    $("#location").html(locationG)
                    if (!fahrenheitEnabled) {
                        $("#temperature").html(tempCG + "\u00B0" + "&nbsp" + "C")
                        fahrenheitEnabled = false
                    } else {
                        $("#temperature").html(tempFG + "\u00B0" + "&nbsp" + "F")
                        fahrenheitEnabled = true
                    }
                    $("#coordinates").html(`<b>Latitude</b>: ${latG}&nbsp;&nbsp;<b>Longitude</b>: ${lonG}`)
                },
                error: function (data) {
                    $("#errorModal").modal('show')
                    $("#location").hide()
                    $("#temperature").hide()
                    $("#coordinates").hide()
                }
            })
        }

        function error() {
            alert("Sorry, no position available.");
        }
    })

    let fahrenheitEnabled = false
    $('input[type="checkbox"]').click(function () {
        let value = $("input[type='checkbox']:checked").val()

        if (value === "fahrenheitUnit") {
            fahrenheitEnabled = true
            $("#temperature").html(tempFG + "\u00B0" + "&nbsp" + "F")
        } else {
            fahrenheitEnabled = false
            $("#temperature").html(tempCG + "\u00B0" + "&nbsp" + "C")
        }
    })
})