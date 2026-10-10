
<template>
  <div class="login-page">
    <div class="login-card">
      <div class="brand">
        <h1>ChesrHire AI</h1>
        <p>AI-Powered Recruitment and Talent Management</p>
      </div>

      <div class="login-content">
        <h2>Recruiter Login</h2>

        <p class="subtitle">
          Sign in to manage jobs, applications and candidate analysis.
        </p>

        <p
          v-if="errorMessage"
          class="error-message"
          role="alert"
        >
          {{ errorMessage }}
        </p>

        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="email">Email Address</label>

            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="Enter your email"
              autocomplete="username"
              required
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>

            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Enter your password"
              autocomplete="current-password"
              required
              :disabled="loading"
            />
          </div>

          <button type="submit" :disabled="loading">
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import api from '../services/api'

const router = useRouter()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  if (loading.value) return

  loading.value = true
  errorMessage.value = ''

  try {
    const response = await api.post('/auth/login', {
      email: email.value.trim(),
      password: password.value,
    })

    const { access_token, token_type, recruiter } = response.data

    if (!access_token || token_type?.toLowerCase() !== 'bearer') {
      errorMessage.value = 'The server returned an invalid login response.'
      return
    }

    localStorage.setItem('access_token', access_token)
    localStorage.setItem('recruiter', JSON.stringify(recruiter))

    password.value = ''

    await router.push({ name: 'dashboard' })
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      if (error.response?.status === 401) {
        errorMessage.value = 'Incorrect email or password.'
      } else if (error.response?.status === 422) {
        errorMessage.value = 'Please enter a valid email and password.'
      } else if (!error.response) {
        errorMessage.value =
          'Cannot connect to the server. Please check that the backend is running.'
      } else {
        errorMessage.value = 'Login failed. Please try again.'
      }
    } else {
      errorMessage.value = 'An unexpected error occurred.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: #f4f7fb;
}

.login-card {
  width: 100%;
  max-width: 430px;
  box-sizing: border-box;
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.brand {
  text-align: center;
  margin-bottom: 32px;
}

.brand h1 {
  margin: 0;
  font-size: 30px;
  color: #1f2937;
}

.brand p {
  margin-top: 8px;
  color: #6b7280;
  font-size: 14px;
}

.login-content h2 {
  margin-bottom: 8px;
  color: #111827;
}

.subtitle {
  margin-bottom: 24px;
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
}

.error-message {
  margin-bottom: 16px;
  padding: 10px 12px;
  border-radius: 8px;
  background: #fef2f2;
  color: #dc2626;
  font-size: 14px;
  line-height: 1.5;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 7px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.form-group input {
  width: 100%;
  box-sizing: border-box;
  padding: 12px 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 15px;
}

.form-group input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.form-group input:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
}

button {
  width: 100%;
  padding: 13px;
  border: none;
  border-radius: 8px;
  background: #2563eb;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

button:hover:not(:disabled) {
  background: #1d4ed8;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .login-page {
    padding: 16px;
  }

  .login-card {
    padding: 28px 22px;
  }

  .brand h1 {
    font-size: 26px;
  }
}
</style>
