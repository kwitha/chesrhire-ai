<template>
  <div class="analysis-page">
    <div class="page-header">
      <button class="back-button" @click="goBack">
        ← Back to Application
      </button>

  <h1>AI Candidate Analysis</h1>
  <p>Review AI-generated insights about the candidate.</p>
</div>

<div v-if="loading" class="message-card">
  <div class="loading-spinner"></div>
  <p>Loading AI analysis...</p>
</div>

<div v-else-if="error" class="message-card error-message">
  <h2>Unable to Load Analysis</h2>
  <p>{{ error }}</p>

  <button class="retry-button" @click="loadAnalysis">
    Try Again
  </button>
</div>

<div v-else-if="analysis">
  <section class="candidate-card">
    <div class="candidate-info">
      <div class="candidate-avatar">
        {{ getInitials(candidateName) }}
      </div>

      <div>
        <h2>{{ candidateName }}</h2>
        <p>{{ jobTitle }}</p>
        <span>
          Application #{{ analysis.application_id }}
        </span>
      </div>
    </div>

    <div class="analysis-status">
      AI Analysis Complete
    </div>
  </section>

  <div class="analysis-grid">
    <section class="content-card">
      <div class="section-header">
        <h2>Candidate Summary</h2>
      </div>

      <div class="section-content">
        <p>{{ analysis.summary }}</p>
      </div>
    </section>

    <section class="content-card">
      <div class="section-header">
        <h2>Skills</h2>
      </div>

      <div class="section-content">
        <p>{{ analysis.skills }}</p>
      </div>
    </section>
  </div>

  <div class="analysis-grid">
    <section class="content-card">
      <div class="section-header">
        <h2>Experience</h2>
      </div>

      <div class="section-content">
        <p>{{ analysis.experience }}</p>
      </div>
    </section>

    <section class="content-card">
      <div class="section-header">
        <h2>Education</h2>
      </div>

      <div class="section-content">
        <p>{{ analysis.education }}</p>
      </div>
    </section>
  </div>

  <section class="content-card">
    <div class="section-header">
      <h2>Relevant Experience</h2>
    </div>

    <div class="section-content">
      <p>{{ analysis.relevant_experience }}</p>
    </div>
  </section>

  <section class="content-card">
    <div class="section-header">
      <h2>Requirement Analysis</h2>
      <p>
        Comparison between the job requirements and the candidate's CV.
      </p>
    </div>

    <div class="requirements-table">
      <table>
        <thead>
          <tr>
            <th>Requirement</th>
            <th>Status</th>
            <th>Evidence</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="requirement in analysis.requirement_analysis"
            :key="requirement.requirement"
          >
            <td>
              <strong>
                {{ requirement.requirement }}
              </strong>
            </td>

            <td>
              <span
                class="status"
                :class="getStatusClass(requirement.status)"
              >
                {{ requirement.status }}
              </span>
            </td>

            <td>
              {{ requirement.evidence }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="content-card">
    <div class="section-header">
      <h2>Missing Requirements</h2>
    </div>

    <div
      v-if="missingRequirements.length > 0"
      class="missing-list"
    >
      <span
        v-for="requirement in missingRequirements"
        :key="requirement"
      >
        {{ requirement }}
      </span>
    </div>

    <div v-else class="no-missing">
      No missing requirements were identified.
    </div>
  </section>

  <section class="content-card">
    <div class="section-header">
      <h2>Match Analysis</h2>
    </div>

    <div class="section-content">
      <p>{{ analysis.match_analysis }}</p>
    </div>
  </section>

  <div class="analysis-meta">
    Analysis generated:
    {{ formatDate(analysis.created_at) }}
  </div>
</div>

  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

interface RequirementAnalysis {
  requirement: string
  status: string
  evidence: string
}

interface CandidateAnalysis {
  id: number
  application_id: number
  summary: string
  skills: string
  experience: string
  education: string
  relevant_experience: string
  missing_requirements: string | string[]
  match_analysis: string
  requirement_analysis: RequirementAnalysis[]
  created_at: string
}

interface Application {
  id: number
  job_id: number
  full_name: string
  email: string
  phone: string
  cv_filename: string
  cv_text: string | null
  cover_letter: string
  status: string
  created_at: string
}

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

const analysis = ref<CandidateAnalysis | null>(null)
const application = ref<Application | null>(null)
const jobs = ref<Job[]>([])

const loading = ref(true)
const error = ref('')

const applicationId = computed(() => {
  return Number(route.query.application_id)
})

const candidateName = computed(() => {
  return application.value?.full_name ?? 'Candidate'
})

const jobTitle = computed(() => {
  if (!application.value) {
    return 'Job Position'
  }

  const job = jobs.value.find(
    (job) => job.id === application.value?.job_id
  )

  return job
    ? job.title
    : `Job #${application.value.job_id}`
})

const missingRequirements = computed(() => {
  if (!analysis.value) {
    return []
  }

  const value = analysis.value.missing_requirements

  if (Array.isArray(value)) {
    return value
  }

  if (!value) {
    return []
  }

  try {
    const parsed = JSON.parse(value)

    if (Array.isArray(parsed)) {
      return parsed
    }
  } catch {
    return value
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean)
  }

  return []
})

async function fetchAnalysis() {
  const response = await api.get<CandidateAnalysis>(
    `/candidate-analysis/${applicationId.value}`
  )

  analysis.value = response.data
}

async function fetchApplication() {
  const response = await api.get<Application>(
    `/applications/${applicationId.value}`
  )

  application.value = response.data
}

async function fetchJobs() {
  const response = await api.get<Job[]>('/jobs/')

  jobs.value = response.data
}

async function loadAnalysis() {
  try {
    loading.value = true
    error.value = ''

    if (
      !applicationId.value ||
      Number.isNaN(applicationId.value)
    ) {
      error.value = 'No valid application ID was provided.'
      return
    }

    await Promise.all([
      fetchAnalysis(),
      fetchApplication(),
      fetchJobs()
    ])
  } catch (err) {
    console.error(
      'Failed to load candidate analysis:',
      err
    )

    error.value =
      'Unable to load candidate analysis from the server.'
  } finally {
    loading.value = false
  }
}

function getInitials(name: string) {
  const parts = name.trim().split(/\s+/)

  const firstName = parts[0] ?? ''
  const lastName = parts[parts.length - 1] ?? ''

  if (parts.length === 1) {
    return firstName.charAt(0).toUpperCase()
  }

  return (
    firstName.charAt(0) +
    lastName.charAt(0)
  ).toUpperCase()
}

function getStatusClass(status: string) {
  if (status.toLowerCase() === 'found') {
    return 'found'
  }

  return 'not-found'
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

function goBack() {
  if (application.value) {
    router.push(
      `/applications/${application.value.id}`
    )
    return
  }

  router.push('/applications')
}

onMounted(() => {
  loadAnalysis()
})
</script>

<style scoped>
.analysis-page {
  padding: 30px;
}

.page-header {
  margin-bottom: 28px;
}

.back-button {
  padding: 0;
  margin-bottom: 16px;
  border: none;
  background: transparent;
  color: #2563eb;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.back-button:hover {
  text-decoration: underline;
}

.page-header h1 {
  margin: 0;
  color: #111827;
  font-size: 28px;
}

.page-header p {
  margin: 7px 0 0;
  color: #6b7280;
  font-size: 14px;
}

.candidate-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 22px 24px;
  margin-bottom: 24px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.candidate-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.candidate-avatar {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #2563eb;
  color: white;
  font-size: 20px;
  font-weight: 700;
}

.candidate-info h2 {
  margin: 0;
  color: #111827;
  font-size: 18px;
}

.candidate-info p {
  margin: 4px 0;
  color: #374151;
  font-size: 14px;
}

.candidate-info span {
  color: #9ca3af;
  font-size: 12px;
}

.analysis-status {
  padding: 8px 12px;
  border-radius: 8px;
  background: #dcfce7;
  color: #166534;
  font-size: 12px;
  font-weight: 600;
}

.analysis-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.content-card {
  margin-bottom: 20px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.section-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.section-header h2 {
  margin: 0;
  color: #111827;
  font-size: 18px;
}

.section-header p {
  margin: 5px 0 0;
  color: #6b7280;
  font-size: 13px;
}

.section-content {
  padding: 20px 24px;
}

.section-content p {
  margin: 0;
  color: #4b5563;
  line-height: 1.7;
  font-size: 14px;
  white-space: pre-wrap;
}

.requirements-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 15px 20px;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
  font-size: 13px;
  vertical-align: top;
}

th {
  background: #f8fafc;
  color: #6b7280;
  font-weight: 600;
}

td {
  color: #4b5563;
  line-height: 1.5;
}

td strong {
  color: #111827;
}

.status {
  display: inline-block;
  padding: 5px 9px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.status.found {
  background: #dcfce7;
  color: #166534;
}

.status.not-found {
  background: #fee2e2;
  color: #991b1b;
}

.missing-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 20px 24px;
}

.missing-list span {
  padding: 7px 11px;
  border-radius: 7px;
  background: #fee2e2;
  color: #991b1b;
  font-size: 13px;
  font-weight: 600;
}

.no-missing {
  padding: 20px 24px;
  color: #166534;
  font-size: 14px;
  background: #f0fdf4;
}

.analysis-meta {
  padding: 5px 0 20px;
  color: #9ca3af;
  font-size: 12px;
}

.message-card {
  padding: 50px;
  text-align: center;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  color: #6b7280;
}

.message-card h2 {
  margin: 0 0 8px;
  color: #111827;
  font-size: 18px;
}

.message-card p {
  margin: 8px 0;
}

.error-message {
  color: #b91c1c;
}

.error-message h2 {
  color: #991b1b;
}

.retry-button {
  margin-top: 15px;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  background: #2563eb;
  color: white;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.retry-button:hover {
  background: #1d4ed8;
}

.loading-spinner {
  width: 30px;
  height: 30px;
  margin: 0 auto 15px;
  border: 3px solid #e5e7eb;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 850px) {
  .analysis-grid {
    grid-template-columns: 1fr;
  }

  .candidate-card {
    align-items: flex-start;
    flex-direction: column;
  }
}

@media (max-width: 650px) {
  .analysis-page {
    padding: 20px;
  }
}
</style>

