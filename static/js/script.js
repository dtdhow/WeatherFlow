
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                window.location.href = `/weather?city=${latitude},${longitude}`;
            },
            function(error) {
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        alert("Доступ к геолокации запрещен. Разрешите доступ в настройках браузера.");
                        break;
                    case error.POSITION_UNAVAILABLE:
                        alert("Информация о местоположении недоступна.");
                        break;
                    case error.TIMEOUT:
                        alert("Время ожидания запроса геолокации истекло.");
                        break;
                    default:
                        alert("Произошла неизвестная ошибка при получении местоположения.");
                        break;
                }

                window.location.href = "/";
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 60000
            }
        );
    } else {
        alert("Geolocation не поддерживается вашим браузером.");
        window.location.href = "/";
    }
}

function getWeatherByCity() {
    const cityInput = document.querySelector('input[name="city"]');
    const city = cityInput.value.trim();

    if (city === '') {
        alert('Пожалуйста, введите название города');
        return;
    }

    window.location.href = `/weather?city=${encodeURIComponent(city)}`;
}

document.addEventListener('DOMContentLoaded', function() {
    const weatherForm = document.querySelector('form[action="/weather"]');
    if (weatherForm) {
        weatherForm.addEventListener('submit', function(e) {
            e.preventDefault();
            getWeatherByCity();
        });
    }

    const detectLocationBtn = document.getElementById('detect-location');
    if (detectLocationBtn) {
        detectLocationBtn.addEventListener('click', getLocation);
    }

    const detectLocationNBtn = document.getElementById('detect-location-nav');
    if (detectLocationNBtn) {
        detectLocationNBtn.addEventListener('click', getLocation);
    }
});
