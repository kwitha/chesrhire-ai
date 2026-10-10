```vue
<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

const jobId = computed(() => Number(route.params.id))

const fullName = ref('')
const email = ref('')
const phone = ref('')
const coverLetter = ref('')
const cv = ref<File | null>(null)
const loading = ref(false)
const error = ref('')
const success = ref(false)

function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0] ?? null

  error.value = ''
  cv.value = null

  if (!file) return

  if (
    file.type !== 'application/pdf' &&
    !file.name.toLowerCase().endsWith('.pdf')
  ) {
    error.value = 'Please select a PDF file.'
    input.value = ''
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    error.value = 'Your CV must not exceed 5 MB.'
    input.value = ''
    return
  }

  cv.value = file
}

async function submitApplication() {
  error.value = ''

  if (!Number.isInteger(jobId.value) || jobId.value <= 0) {
    error.value = 'Invalid job reference. Please return to Careers.'
    return
  }

  if (!cv.value) {
    error.value = 'Please upload your CV in PDF format.'
    return
  }

  const formData = new FormData()
  formData.append('job_id', String(jobId.value))
  formData.append('full_name', fullName.value.trim())
  formData.append('email', email.value.trim())
  formData.append('phone', phone.value.trim())
  formData.append('cover_letter', coverLetter.value.trim())
  formData.append('cv', cv.value)

  loading.value = true

  try {
    await api.post('/applications/', formData, {
      headers: {
        'Content-Type': undefined,
      },
    })

    success.value = true
  } catch (err: any) {
    const detail = err.response?.data?.detail

    if (Array.isArray(detail)) {
      error.value = detail
        .map((item: { msg?: string }) => item.msg ?? 'Invalid input')
        .join(' ')
    } else {
      error.value =
        typeof detail === 'string'
          ? detail
          : 'Application submission failed. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="application-page">
    <button
      type="button"
      class="back-button"
      @click="router.push(`/careers/${jobId}`)"
    >
      Back to Job Details
    </button>

    <section class="application-card">
      <h1>Apply for This Position</h1>

      <p class="intro">
        Complete the form below to submit your application.
        No account is required.
      </p>

      <div v-if="success" class="success-message">
        <h2>Application Submitted Successfully!</h2>
        <p>Thank you. Your application has been received.</p>

        <button
          type="button"
          class="submit-button"
          @click="router.push('/careers')"
        >
          Browse More Jobs
        </button>
      </div>

      <form v-else @submit.prevent="submitApplication">
        <div class="form-group">
          <label for="fullName">Full Name</label>
          <input
            id="fullName"
            v-model="fullName"
            type="text"
            maxlength="255"
            autocomplete="name"
            placeholder="Enter your full name"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            maxlength="255"
            autocomplete="email"
            placeholder="you@example.com"
            required
          />
        </div>

        <div class="form-group">
          <label for="phone">Phone Number</label>
          <input
            id="phone"
            v-model="phone"
            type="tel"
            maxlength="30"
            autocomplete="tel"
            placeholder="Enter your phone number"
            required
          />
        </div>

        <div class="form-group">
          <label for="coverLetter">Cover Letter</label>
          <textarea
            id="coverLetter"
            v-model="coverLetter"
            rows="6"
            placeholder="Explain why you are suitable for this position..."
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label for="cv">Upload CV (PDF, maximum 5 MB)</label>
          <input
            id="cv"
            type="file"
            accept=".pdf,application/pdf"
            required
            @change="handleFileChange"
          />
          <small v-if="cv">Selected file: {{ cv.name }}</small>
        </div>

        <p v-if="error" class="error-message">{{ error }}</p>

        <button
          type="submit"
          class="submit-button"
          :disabled="loading"
        >
          {{ loading ? 'Submitting...' : 'Submit Application' }}
        </button>
      </form>
    </section>
  </main>
</template>

<style scoped>
.application-page {
  max-width: 760px;
  margin: 40px auto;
  padding: 24px;
  color: #1f2937;
}

.back-button {
  margin-bottom: 20px;
  padding: 8px 0;
  border: none;
  background: transparent;
  color: #15803d;
  font-size: 15px;
  cursor: pointer;
}

.application-card {
  padding: 32px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  background: white;
  box-shadow: 0 4px 16px rgb(0 0 0 / 4%);
}

h1 {
  margin-top: 0;
  font-size: 28px;
}

.intro {
  margin-bottom: 28px;
  color: #64748b;
  line-height: 1.6;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

label {
  font-weight: 600;
  font-size: 14px;
}

input,
textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font: inherit;
}

input:focus,
textarea:focus {
  outline: 2px solid #86efac;
  border-color: #15803d;
}

textarea {
  resize: vertical;
}

small {
  color: #64748b;
}

.submit-button {
  padding: 13px 20px;
  border: none;
  border-radius: 8px;
  background: #15803d;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.submit-button:hover {
  background: #166534;
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  margin-bottom: 16px;
  color: #b91c1c;
  line-height: 1.5;
}

.success-message {
  padding: 20px;
  background: #f0fdf4;
  border-radius: 10px;
  line-height: 1.6;
}

.success-message h2 {
  color: #166534;
}

@media (max-width: 600px) {
  .application-page {
    margin: 16px auto;
    padding: 14px;
  }

  .application-card {
    padding: 22px 16px;
  }
}
</style>
