import { Component } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { InitialAPIService } from '../../initial-api.service';
import { AuthService } from '../../auth.service';

@Component({
  selector: 'app-account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.css']
})
export class AccountComponent {
  isCreatingAccount = false;
  errorMessage = '';
  successMessage = '';

  accountForm = this.fb.group({
    email: new FormControl('', { validators: [Validators.required, Validators.email] }),
    password: new FormControl('', { validators: [Validators.required] }),
  });

  constructor(
    private initialApiService: InitialAPIService,
    private authService: AuthService,
    private router: Router,
    private fb: FormBuilder
  ) {}

  toggleMode() {
    this.isCreatingAccount = !this.isCreatingAccount;
    this.errorMessage = '';
    this.successMessage = '';
  }

  submit() {
    if (this.accountForm.invalid) {
      this.errorMessage = 'Please fill in all required fields correctly.';
      return;
    }

    const email = this.accountForm.value.email || '';
    const password = this.accountForm.value.password || '';

    if (this.isCreatingAccount) {
      this.createAccount(email, password);
    } else {
      this.login(email, password);
    }
  }

  private createAccount(email: string, password: string) {
    this.initialApiService.createUser(email, password).subscribe({
      next: (response) => {
        this.successMessage = response.message || 'Account created successfully!';
        this.errorMessage = '';
        // Switch to login mode after successful account creation
        this.isCreatingAccount = false;
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Failed to create account. Please try again.';
        this.successMessage = '';
      }
    });
  }

  private login(email: string, password: string) {
    this.initialApiService.login(email, password).subscribe({
      next: (response) => {
        // Store the token in localStorage
        localStorage.setItem('token', response.access_token);
        // Update auth service state
        this.authService['_isLoggedIn$'].next(true);
        // Navigate to dashboard or home page
        this.router.navigateByUrl('/home');
      },
      error: (error) => {
        this.errorMessage = 'Login failed. Please check your credentials and try again.';
        this.successMessage = '';
      }
    });
  }
}
