var isLoginAvailable = false;

function isFirstNameValid() {
	var nameNode = document.getElementById('firstname');
	return isNameValid(nameNode);
}

function isLastNameValid() {
	var nameNode = document.getElementById('lastname');
	return isNameValid(nameNode);
}

function isNameValid(nameNode) {
	var parent = nameNode.parentElement;
	checkpElementsAndRemoveIfExist(parent);
	if(nameNode.value.length < 3) {
		var p = document.createElement('p');
		p.innerHTML = "Podana fraza jest za krótka, wymagane minimum 3 znaki";
		p.className += "invalid_data";
		parent.appendChild(p);
		return false;
	}
	var regex = new RegExp(/^[a-zA-ZąęćśńółźżĄĘĆŚŃÓŁŹŻ]+$/);
	if(regex.test(nameNode.value)){
		nameNode.value = convertName(nameNode.value);
		return true;
	}
	else {
		var p = document.createElement('p');
		p.innerHTML = "Wystąpiły niedozwolone znaki";
		p.className += "invalid_data";
		parent.appendChild(p);
		return false;
	}
}

function convertName(name) {
	return name[0].toUpperCase() + name.slice(1);
}

async function isLoginValid() {
	var login = document.getElementById('login');
	var parent = document.getElementById('login').parentElement;
	checkpElementsAndRemoveIfExist(parent);
	var p = document.createElement('p');
	if(login.value < 3) {		
		p.innerHTML = "Login za krótki, wymagane minimum 3 znaki";
		p.className += "invalid_data";
		parent.appendChild(p);
		return false;
	}
	else if(login.value > 12) {
		p.innerHTML = "Login za długi, dopuszczalne maximum 12 znaków";
		p.className += "invalid_data";
		parent.appendChild(p);
		return false;
	}
	var regex = new RegExp(/^[a-z]+$/); // wersja pod regex serwera
	//var regex = new RegExp(/^[a-zA-Z0-9]+$/);
	if(!regex.test(login.value)){
		//p.innerHTML = "Wykryto niedozwolone znaki w loginie, dopuszczalne tylko litery i cyfry";
		p.innerHTML = "Wykryto niedozwolone znaki w loginie, dopuszczalne tylko małe litery"; // wersja pod regex serwera
		p.className += "invalid_data";
		parent.appendChild(p);
		return false;
	}
	var url = "https://pi.iem.pw.edu.pl/user/" + login.value;
	request('GET', url)
		.catch(e => {
			console.log(e);
		});
		
	return isLoginAvailable;
}

function request(method, url) {
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.onload = function () {
			if(this.status === 200) {
				var loginParent = document.getElementById('login').parentElement;
				var p = document.createElement('p');
				p.innerHTML = "Wybrany login jest zajęty";
				p.className += "invalid_data";
				loginParent.appendChild(p);
				resolve(xhr.response);
			} 
			else if(this.status === 404) {
				isLoginAvailable = true;
			}
			else if(this.status === 500 || this.status === 502 || this.status === 503 || this.status === 505) {
				window.alert("Występują błędy po stronie serwera, spróbuj ponownie później zarejestrować się w serwisie");
				isLoginAvailable = false;
			}
			else {
				reject({
					status: this.status,
					statusText: xhr.statusText
				});
				isLoginAvailable = false;
			}
		};
        xhr.onerror = function () {
            reject({request: xhr});
        };
        xhr.send();
    });
}

function isPasswordValid() {
	var pass = document.getElementById('password');
	var parent = pass.parentElement;
	var p = document.createElement('p');
	checkpElementsAndRemoveIfExist(parent);
	validatePasswordCompatibility();
	if(pass.value.length < 8) {
		p.innerHTML = "Hasło zbyt krótkie, wymagane minimum 8 znaków";
		p.className += "invalid_data";
		parent.appendChild(p);
		return false;
	}
	else {
		var score = scorePassword(pass.value);
		if(score < 60) {
			p.innerHTML = "Podane hasło jest zbyt słabe";
			p.className += "invalid_data";
			parent.appendChild(p);
			return false;
		}
	}
	return true;
}

function scorePassword(pass) {
    var score = 0;
    var letters = new Object();
    for (var i=0; i < pass.length; i++) {
        letters[pass[i]] = (letters[pass[i]] || 0) + 1;
        score += 5.0 / letters[pass[i]];
    }
    var variations = {
        digits: /\d/.test(pass),
        lower: /[a-z]/.test(pass),
        upper: /[A-Z]/.test(pass),
        nonWords: /\W/.test(pass),
    }
	
    var variationCount = 0;
    for(var check in variations) {
        variationCount += (variations[check] == true) ? 1 : 0;
    }
    score += (variationCount - 1) * 10;

    return parseInt(score);
}

function validatePasswordCompatibility() {
	var pass = document.getElementById('password');
	var rpass = document.getElementById('repeat_password');
	var parent = rpass.parentElement;
	checkpElementsAndRemoveIfExist(parent);
	if(pass.value === rpass.value) {
		return true;
	}
	else {
		var p = document.createElement('p');
		p.innerHTML = "Hasła nie są zgodne";
		p.className += "invalid_data";
		parent.appendChild(p);
		return false;
	}
}

function isPeselValid() {
	var pesel = document.getElementById('pesel');
	var parent = pesel.parentElement;
	checkpElementsAndRemoveIfExist(parent);
	if(isPeselSumValid(pesel.value)){
		setSex(pesel.value[9]);
		setBirthday(pesel.value);
		return true;
	}
	else {
		var p = document.createElement('p');
		p.innerHTML = "Nieprawidłowy numer pesel";
		p.className += "invalid_data";
		parent.appendChild(p);	
		return false;
	}
}

function isPeselSumValid(pesel) 
{
	var wagi = [9,7,3,1,9,7,3,1,9,7];
	var suma = 0;
    
	for(var i=0; i < wagi.length; i++) {
		suma += (parseInt(pesel.substring(i,i+1),10) * wagi[i]);
	}
	suma = suma % 10;
	var valid = (suma === parseInt(pesel.substring(10,11),10));
	return valid;
}

function setSex(number) {
	var male = document.getElementById('male');
	var female = document.getElementById('female');
	if(number%2 == 0) {
		male.checked = false;
		female.checked = true;
	}
	else {
		female.checked = false;
		male.checked = true;
	}
}

function setBirthday(pesel) {
	var year= parseInt(pesel.substring(0,2),10);
	var month = parseInt(pesel.substring(2,4),10) - 1;
	var day = parseInt(pesel.substring(4,6),10); 
	if(month > 80) {
		year = year + 1800;
		month = month - 80;
	}
	else if(month > 60) {
        year = year + 2200;
        month = month - 60;
	}
	else if(month > 40) {
        year = year + 2100;
        month = month - 40;
	}
	else if(month > 20) {
        year = year + 2000;
        month = month - 20;
	}
	else
	{
        year = year + 1900;
	}
	
	var date = new Date();
	date.setFullYear(year, month, day);
	document.getElementById('birthdate').valueAsDate = date;
	checkpElementsAndRemoveIfExist(document.getElementById('birthdate').parentElement)
}

function isBirthDateValid() {
	var birthDateNode = document.getElementById('birthdate');
	var birthDate = birthDateNode.value;
	var parent = birthDateNode.parentElement;
	var p = document.createElement('p');
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1;
	var yyyy = today.getFullYear();
	today = yyyy + "-" + mm + "-" + dd;
	var minDate = "1900-01-01";
	checkpElementsAndRemoveIfExist(parent);
	if(birthDate > today) {
		p.innerHTML = "Data urodzenia nie może być większa niż dzisiejsza data";
		p.className += "invalid_data";
		parent.appendChild(p);
		return false;
	}
	else if(birthDate < minDate) {
		p.innerHTML = "Data urodzenia musi być większa niż 1900-01-01";
		p.className += "invalid_data";
		parent.appendChild(p);
		return false;
	}
	return true;
}

function isFileValid() {
	var file = document.getElementById('file');
	var parent = file.parentElement;
	checkpElementsAndRemoveIfExist(parent);
	if(file.files.length == 0 ){
		var p = document.createElement('p');
		p.innerHTML = "Nie wybrano pliku";
		p.className += "invalid_data";
		parent.appendChild(p);
		return false;
	}
	else {
		if(file.files[0]['type'].split('/')[0] === 'image') {
			return true;
		}
		else {
			var p = document.createElement('p');
			p.innerHTML = "Wybrany plik nie jest plikiem graficznym";
			p.className += "invalid_data_file";
			parent.appendChild(p);
			return false;
		}
	}
}

function checkpElementsAndRemoveIfExist(parent) {
	var p_elements = parent.querySelectorAll('p')
	if(p_elements.length == 1) {
		parent.removeChild(p_elements[0]);
	}
}

async function isFormValid(form) {
	if((isFirstNameValid() && isLastNameValid() && await isLoginValid() && isPasswordValid() && validatePasswordCompatibility() && isPeselValid() && isBirthDateValid() && isFileValid()) == 1) {
		form.submit();
	}
}