// Login form submission: set logged-in flag then submit
document.addEventListener('DOMContentLoaded', function() {
	const loginForm = document.getElementById('loginForm');
	if (!loginForm) return;

	loginForm.addEventListener('submit', function(e) {
		try {
			// Set a client-side logged-in flag so protected pages won't redirect back
			localStorage.setItem('isLoggedIn', 'true');
		} catch (err) {
			console.warn('Could not set localStorage flag:', err);
		}

		// Allow normal form submission (navigates to /welcome.html)
	});
// Client-side login handler
document.addEventListener('DOMContentLoaded', function () {
	const loginForm = document.getElementById('loginForm');
	const loginError = document.getElementById('loginError');

	if (!loginForm) return;

	loginForm.addEventListener('submit', function (e) {
		e.preventDefault();

		const email = (document.getElementById('email') || {}).value?.trim() || '';
		const password = (document.getElementById('password') || {}).value || '';

		// Simple client-side validation
		if (!email || !password) {
			showError('Please enter both email and password');
			return;
		}

		// Hard-coded test credentials (for local testing)
		const testEmail = 'mahesha@gmail.com';
		const testPassword = 'm@123';

		if (email === testEmail && password === testPassword) {
			try {
				localStorage.setItem('isLoggedIn', 'true');
			} catch (err) {
				console.warn('Could not set localStorage:', err);
			}

			// Navigate to welcome page
			window.location.href = '/welcome.html';
		} else {
			showError('Invalid email or password');
		}
	});

	function showError(msg) {
		if (!loginError) return;
		loginError.textContent = msg;
		loginError.style.display = 'block';
	}
});
});