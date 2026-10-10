
<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
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

const router = useRouter()
const jobs = ref<Job[]>([])
const loading = ref(true)
const error = ref('')
const search = ref('')
const employmentType = ref('All')

const employmentTypes = computed(() => [
  'All',
  ...new Set(jobs.value.map(job => job.employment_type)),
])

const filteredJobs = computed(() => {
  const query = search.value.trim().toLowerCase()

  return jobs.value.filter(job => {
    const matchesSearch =
      !query ||
      job.title.toLowerCase().includes(query) ||
      job.location.toLowerCase().includes(query) ||
      job.description.toLowerCase().includes(query)

    const matchesType =
      employmentType.value === 'All' ||
      job.employment_type === employmentType.value

    return matchesSearch && matchesType
  })
})

async function fetchJobs() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get<Job[]>('/public/jobs/')
    jobs.value = response.data
  } catch (err) {
    console.error('Failed to load jobs:', err)
    error.value = 'We could not load jobs right now. Please try again.'
  } finally {
    loading.value = false
  }
}

function viewJob(jobId: number) {
  router.push({ name: 'career-details', params: { id: jobId } })
}

function formatDate(value: string | null) {
  if (!value) return 'Not specified'

  return new Date(value).toLocaleDateString('en-KE', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

onMounted(fetchJobs)
</script>

<template>
  <div class="careers-page">
    <header class="topbar">
      <a class="brand" href="/careers">
        <span class="brand-icon">C</span>
        <span>ChesrHire <strong>AI</strong></span>
      </a>

      <span class="topbar-label">Careers Portal</span>
    </header>

    <section class="hero">
      <div class="hero-content">
        <span class="eyebrow">YOUR NEXT OPPORTUNITY</span>
        <h1>Find work that moves<br />your career forward.</h1>
        <p>
          Discover opportunities, showcase your talent, and take the next
          step in your professional journey.
        </p>
      </div>
      <div class="hero-decoration" aria-hidden="true">
        <span class="decoration-circle circle-one"></span>
        <span class="decoration-circle circle-two"></span>
        <span class="decoration-square"></span>
      </div>
    </section>

    <main class="content">
      <div class="section-heading">
        <div>
          <h2>Open positions</h2>
          <p>Explore opportunities that match your skills.</p>
        </div>
        <span class="job-count">{{ filteredJobs.length }} positions</span>
      </div>

      <div class="filters">
        <label class="search-box">
          <span aria-hidden="true">⌕</span>
          <input
            v-model="search"
            type="search"
            placeholder="Search job title, location..."
            aria-label="Search jobs"
          />
        </label>

        <select v-model="employmentType" aria-label="Filter by employment type">
          <option v-for="type in employmentTypes" :key="type" :value="type">
            {{ type === 'All' ? 'All employment types' : type }}
          </option>
        </select>
      </div>

      <div v-if="loading" class="message">
        <span class="loader"></span>
        <p>Finding opportunities for you...</p>
      </div>

      <div v-else-if="error" class="message error-message">
        <p>{{ error }}</p>
        <button class="retry-button" @click="fetchJobs">Try again</button>
      </div>

      <div v-else-if="filteredJobs.length === 0" class="message empty-message">
        <div class="empty-icon">⌕</div>
        <h3>{{ jobs.length ? 'No matching jobs' : 'No open positions yet' }}</h3>
        <p>
          {{
            jobs.length
              ? 'Try changing your search or employment type.'
              : 'Please check back later for new opportunities.'
          }}
        </p>
        <button
          v-if="search || employmentType !== 'All'"
          class="retry-button"
          @click="search = ''; employmentType = 'All'"
        >
          Clear filters
        </button>
      </div>

      <div v-else class="jobs-grid">
        <article
          v-for="job in filteredJobs"
          :key="job.id"
          class="job-card"
        >
          <div class="card-top">
            <div class="company-mark">C</div>
            <span class="status"><span></span> Open</span>
          </div>

          <h3>{{ job.title }}</h3>

          <div class="job-meta">
            <span>⌖ {{ job.location }}</span>
            <span>◷ {{ job.employment_type }}</span>
          </div>

          <p class="description">{{ job.description }}</p>

          <div class="card-footer">
            <span class="closing-date">
              Closes: {{ formatDate(job.closing_date) }}
            </span>
            <button class="details-button" @click="viewJob(job.id)">
              View &amp; apply <span>→</span>
            </button>
          </div>
        </article>
      </div>

      <footer class="page-footer">
        <span>© {{ new Date().getFullYear() }} ChesrHire AI</span>
        <span>Connecting talent with opportunity.</span>
      </footer>
    </main>
  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.careers-page {
  min-height: 100vh;
  background: #f7f8fc;
  color: #192338;
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.topbar {
  height: 76px;
  padding: 0 8%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid #e9edf4;
}

.brand {
  display: flex;
  align-items: center;
  gap: 11px;
  color: #17223b;
  font-size: 19px;
  font-weight: 750;
  text-decoration: none;
}

.brand strong {
  color: #5366d9;
}

.brand-icon,
.company-mark {
  display: grid;
  place-items: center;
  width: 38px;
  height: 38px;
  border-radius: 11px;
  background: #5366d9;
  color: white;
  font-size: 20px;
  font-weight: 800;
}

.topbar-label {
  color: #68748a;
  font-size: 13px;
  font-weight: 600;
}

.hero {
  position: relative;
  overflow: hidden;
  min-height: 310px;
  display: flex;
  align-items: center;
  padding: 52px 10%;
  background: linear-gradient(115deg, #18284b, #344a85 70%, #5366d9);
  color: #fff;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 620px;
}

.eyebrow {
  color: #c5d0ff;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 2px;
}

.hero h1 {
  margin: 16px 0;
  font-size: clamp(30px, 4vw, 45px);
  line-height: 1.18;
  letter-spacing: -1.3px;
}

.hero p {
  max-width: 510px;
  color: #e0e6ff;
  font-size: 15px;
  line-height: 1.8;
}

.hero-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.decoration-circle {
  position: absolute;
  right: 12%;
  top: 8%;
  width: 220px;
  height: 220px;
  border: 1px solid #ffffff25;
  border-radius: 50%;
}

.circle-two {
  right: 5%;
  top: 28%;
  width: 280px;
  height: 280px;
}

.decoration-square {
  position: absolute;
  right: 18%;
  top: 28%;
  width: 90px;
  height: 90px;
  border: 1px solid #ffffff30;
  border-radius: 20px;
  transform: rotate(35deg);
}

.content {
  width: min(1120px, 90%);
  margin: 0 auto;
  padding: 44px 0 24px;
}

.section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.section-heading h2 {
  margin: 0 0 7px;
  font-size: 25px;
  letter-spacing: -0.6px;
}

.section-heading p {
  margin: 0;
  color: #788399;
  font-size: 14px;
}

.job-count {
  padding: 8px 13px;
  border: 1px solid #e1e5ef;
  border-radius: 20px;
  color: #5366d9;
  background: #fff;
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
}

.filters {
  display: flex;
  gap: 14px;
  margin: 27px 0;
}

.search-box {
  display: flex;
  flex: 1;
  align-items: center;
  gap: 10px;
  padding: 0 15px;
  border: 1px solid #e1e5ef;
  border-radius: 9px;
  background: #fff;
  color: #788399;
}

.search-box > span {
  font-size: 24px;
}

.search-box input {
  width: 100%;
  min-width: 0;
  padding: 13px 0;
  border: 0;
  outline: none;
  background: transparent;
  color: #192338;
  font: inherit;
  font-size: 13px;
}

.filters select {
  min-width: 205px;
  padding: 0 13px;
  border: 1px solid #e1e5ef;
  border-radius: 9px;
  background: white;
  color: #44516a;
  font: inherit;
  font-size: 13px;
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.job-card {
  display: flex;
  flex-direction: column;
  min-width: 0;
  padding: 24px;
  border: 1px solid #e8ebf3;
  border-radius: 13px;
  background: #fff;
  box-shadow: 0 5px 18px #18284b06;
  transition: transform 0.2s, box-shadow 0.2s;
}

.job-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 26px #18284b0d;
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.company-mark {
  width: 43px;
  height: 43px;
  border-radius: 12px;
  background: #eef0ff;
  color: #5366d9;
}

.status {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 20px;
  background: #eaf8ef;
  color: #21854a;
  font-size: 11px;
  font-weight: 700;
}

.status span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #2eb565;
}

.job-card h3 {
  margin: 20px 0 12px;
  font-size: 19px;
  line-height: 1.4;
}

.job-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  color: #6d7890;
  font-size: 12px;
}

.description {
  display: -webkit-box;
  overflow: hidden;
  margin: 17px 0 22px;
  color: #67738a;
  font-size: 13px;
  line-height: 1.8;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: auto;
  padding-top: 17px;
  border-top: 1px solid #edf0f6;
}

.closing-date {
  color: #8992a5;
  font-size: 11px;
}

.details-button,
.retry-button {
  padding: 10px 14px;
  border: 0;
  border-radius: 7px;
  background: #5366d9;
  color: #fff;
  font: inherit;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

.details-button span {
  margin-left: 7px;
}

.details-button:hover,
.retry-button:hover {
  background: #4053c1;
}

.message {
  display: flex;
  min-height: 220px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #778198;
  text-align: center;
}

.message p {
  margin: 0;
  font-size: 14px;
}

.error-message {
  color: #b42318;
}

.empty-icon {
  display: grid;
  place-items: center;
  width: 55px;
  height: 55px;
  border-radius: 50%;
  background: #edf0ff;
  color: #5366d9;
  font-size: 32px;
}

.empty-message h3 {
  margin: 4px 0 0;
  color: #192338;
}

.loader {
  width: 28px;
  height: 28px;
  border: 3px solid #dce1fa;
  border-top-color: #5366d9;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.page-footer {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-top: 48px;
  padding-top: 20px;
  border-top: 1px solid #e6eaf2;
  color: #939caf;
  font-size: 11px;
}

@media (max-width: 700px) {
  .topbar {
    height: 65px;
    padding: 0 5%;
  }

  .hero {
    min-height: 270px;
    padding: 40px 6%;
  }

  .hero-decoration {
    opacity: 0.45;
  }

  .content {
    width: 90%;
    padding-top: 30px;
  }

  .section-heading h2 {
    font-size: 21px;
  }

  .filters {
    flex-direction: column;
  }

  .filters select {
    min-height: 44px;
  }

  .jobs-grid {
    grid-template-columns: 1fr;
  }

  .job-card {
    padding: 20px;
  }

  .page-footer {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
