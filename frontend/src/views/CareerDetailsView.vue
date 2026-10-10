```vue
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

interface Job {
  id: number
  title: string
  description: string
  requirements: string
  location: string
  employment_type: string
  closing_date: string | null
  status: string
  created_at: string
}

const route = useRoute()
const router = useRouter()

const job = ref<Job | null>(null)
const loading = ref(true)
const error = ref('')

const loadJob = async () => {
  try {
    const response = await api.get<Job>(
      `/public/jobs/${route.params.id}`,
    )
    job.value = response.data
  } catch {
    error.value = 'Unable to load this job. It may no longer be available.'
  } finally {
    loading.value = false
  }
}

const applyForJob = () => {
  router.push({
    name: 'career-apply',
    params: { id: route.params.id },
  })
}

onMounted(loadJob)
</script>

<template>
  <main class="career-details">
    <button class="back-button" @click="router.push('/careers')">
      ← Back to Careers
    </button>

    <p v-if="loading">Loading job details...</p>

    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <article v-else-if="job" class="job-card">
      <span class="job-type">{{ job.employment_type }}</span>

      <h1>{{ job.title }}</h1>

      <p class="job-meta">
        {{ job.location }}
      </p>

      <p v-if="job.closing_date">
        Application deadline:
        {{ new Date(job.closing_date).toLocaleDateString() }}
      </p>

      <section>
        <h2>Job Description</h2>
        <p>{{ job.description }}</p>
      </section>

      <section>
        <h2>Requirements</h2>
        <p>{{ job.requirements }}</p>
      </section>

      <button class="apply-button" @click="applyForJob">
        Apply for This Position
      </button>
    </article>
  </main>
</template>

<style scoped>
.career-details {
  max-width: 900px;
  margin: 40px auto;
  padding: 24px;
  color: #1f2937;
}

.back-button {
  border: none;
  background: transparent;
  color: #15803d;
  cursor: pointer;
  font-size: 15px;
  margin-bottom: 24px;
}

.job-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 32px;
}

.job-type {
  display: inline-block;
  background: #dcfce7;
  color: #166534;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
}

h1 {
  margin: 16px 0 8px;
}

h2 {
  margin-top: 28px;
  font-size: 19px;
}

p {
  line-height: 1.7;
  white-space: pre-line;
}

.job-meta {
  color: #64748b;
}

.apply-button {
  margin-top: 24px;
  padding: 12px 22px;
  border: none;
  border-radius: 8px;
  background: #15803d;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.apply-button:hover {
  background: #166534;
}

.error-message {
  color: #b91c1c;
}
</style>
```
