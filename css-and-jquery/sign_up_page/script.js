$(document).ready(function() {
	let nameValidation = false
	let emailValidation = false
	let addrValidation = false
	let ageValidation = false
	let genderValidation = false
	let passwordValidation = false
	let confPasswordValidation = false

	let isNameEmpty = true
	let isEmailEmpty = true
	let isAddrEmpty = true
	let isAgeEmpty = true
	let isGenderEmpty = true
	let isPasswordEmpty = true
	let isConfPasswordEmpty = true

	// username
	$("#name").keyup(function() {
		let name = $("#name").val()

		if (name === "") {
			isNameEmpty = true
			nameValidation = false
			$("#name-check").show()
			$("#name-check").html("This is required")
		} else if (name.length < 3) {
			nameValidation = false
			$("#name-check").show()
			$("#name-check").html("Min 3 characters is required")
		} else {
			isNameEmpty = false
			nameValidation = true
			$("#name-check").hide()
		}
	})

	// email
	$("#email").keyup(function() {
		let emailRegex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/
		let emailAddr = $("#email").val()

		isEmail = emailRegex.test(emailAddr)
		if (emailAddr === "") {
			isEmailEmpty = true
			emailValidation = false
			$("#email-check").show()
			$("#email-check").html("This is required")
		} else if (!isEmail) {	
			emailValidation = false
			$("#email-check").show()
			$("#email-check").html("Invalid format")
		} else {
			isEmailEmpty = false
			emailValidation = true
			$("#email-check").hide()
		}
	})

	// address
	$("#address").keyup(function() {
		let address = $("#address").val()

		if (address === "") {
			isAddrEmpty = true
			addrValidation = false
			$("#address-check").show()
			$("#address-check").html("This is required")
		} else if (address.length < 10) {
			addrValidation = false
			$("#address-check").show()
			$("#address-check").html("Min 10 characters is required")
		} else {
			isAddrEmpty = false
			addrValidation = true
			$("#address-check").hide()
		}
	})

	// date of birth
	$("#dob").change(function() {
		let dateStr = $("#dob").val()
		
		let dob = new Date(dateStr)
		
		let birthYear = dob.getFullYear()
		let birthMonth = dob.getMonth() + 1
		let birthDate = dob.getDate()
		let currYear = new Date().getFullYear()
		let currMonth = new Date().getMonth() + 1
		let currDate = new Date().getDate()
		
		age = currYear - birthYear

		let isBirthdayMonth = (currMonth == birthMonth)
		let isBirthday = isBirthdayMonth && (currDate == birthDate)

		if (!isBirthdayMonth && !isBirthday) {
			age -= 1
		}
		
		$("#age").val(age)
		if (age === "") {
			isAgeEmpty = true
			ageValidation = false
		} else if (age == 18) {
			ageValidation = false
			$("#ageModal").modal('show')
		} else if (!(age >= 10 && age <= 100)) {
			ageValidation = false
			$("#age-check").show()
			$("#age-check").html("Age should be between 10 and 100")
		}  else {
			isAgeEmpty = false
			ageValidation = true
			$("#age-check").hide()
		}
	})

	// gender
	let isMaleSelected = false
	let isFemaleSelected = false
	let isOtherSelected = false
	$("input[type='radio']").change(function() {
		var selectedValue = $('input[name="gender"]:checked').val()
		
		if (selectedValue === 'male') {
			isMaleSelected = true
		} else if (selectedValue === 'female') {
			isFemaleSelected = true
		} else if (selectedValue === 'other') {
			isOtherSelected = true
		}

		genderValidation = true
		isGenderEmpty = false

		if (!isGenderEmpty) {
			$("#gender-check").hide()
		}
	})

	// password visibility
	$(".toggle-password").click(function() {
		$(this).toggleClass("fa-eye-slash")

		var type = $(this).hasClass("fa-eye-slash") ? "text" : "password";
		$("#password").attr("type", type)

	})

	$(".toggle-confpassword").click(function() {
		$(this).toggleClass("fa-eye-slash")

		var type = $(this).hasClass("fa-eye-slash") ? "text" : "password";
		$("#confirm-password").attr("type", type)

	})

	// password
	$("#password").on("cut copy paste", function(e) {
		e.preventDefault()
	})
	$("#password").keyup(function() {
		let password = $("#password").val()
		let passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/

		if (password === "") {
			isPasswordEmpty = true
			passwordValidation = false
		} else if (!passwordRegex.test(password)) {
			$("#password-check").show()
			$("#password-check").html("Must contain atleast 8 characters and one: number, uppercase, lowercase, special character")
			passwordValidation = false
		} else {
			isPasswordEmpty = false
			passwordValidation = true
			$("#password-check").hide()
		}

		let confirmPass = $("#confirm-password").val()

		if (confirmPass === "") {
			isConfPasswordEmpty = true
			confPasswordValidation = false
		} else if (password === confirmPass) {
			isConfPasswordEmpty = false
			confPasswordValidation = true
			$("#confirm-password-check").hide()
		} else {
			confPasswordValidation = false
			$("#confirm-password-check").show()
			$("#confirm-password-check").html("The password doesn't match")
		}
	})

	// confirm password
	$("#confirm-password").on("cut copy paste", function(e) {
		e.preventDefault()

		$("#ccpModal").modal('show')
	})

	$("#confirm-password").keyup(function() {
		let password = $("#password").val()
		let confirmPass = $("#confirm-password").val()

		if (confirmPass === "") {
			isConfPasswordEmpty = true
			confPasswordValidation = false
		} else if (password === confirmPass) {
			isConfPasswordEmpty = false
			confPasswordValidation = true
			$("#confirm-password-check").hide()
		} else {
			confPasswordValidation = false
			$("#confirm-password-check").show()
			$("#confirm-password-check").html("The password doesn't match")
		}
	})

	$("form").submit(function(e) {
		e.preventDefault()

		// gender 
		if (!(isMaleSelected || isFemaleSelected || isOtherSelected)) {
			genderValidation = false
			isGenderEmpty = true
		}

		if (
			nameValidation &&
			emailValidation &&
			addrValidation &&
			ageValidation &&
			genderValidation &&
			passwordValidation &&
			confPasswordValidation
		) {
			window.location.href = "https://cybrosys.com"
		} else {
			if (isNameEmpty) {
				$("#name-check").show()
				$("#name-check").html("This is required")
			} else {
				$("#name-check").hide()
			}

			if (isEmailEmpty) {
				$("#email-check").show()
				$("#email-check").html("This is required")
			} else {
				$("#email-check").hide()
			}

			if (isAddrEmpty) {
				$("#address-check").show()
				$("#address-check").html("This is required")
			} else {
				$("#address-check").hide()
			}

			if (isAgeEmpty) {
				$("#age-check").show()
				$("#age-check").html("This is required")
			} else {
				$("#age-check").hide()
			}

			if (isGenderEmpty) {
				$("#gender-check").show()
				$("#gender-check").html("This is required")
			} else {
				$("#gender-check").hide()
			}

			if (isPasswordEmpty) {
				$("#password-check").show()
				$("#password-check").html("This is required")
			} else {
				$("#password-check").hide()
			}

			if (isConfPasswordEmpty) {
				$("#confirm-password-check").show()
				$("#confirm-password-check").html("This is required")
			} else {
				$("#confirm-password-check").hide()
			}
		}
	})
})
