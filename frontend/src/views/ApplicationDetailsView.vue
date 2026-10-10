<template>
  <div class="details-page">
    <div class="page-header">
      <button class="back-button" @click="goBack">
        ← Back to Applications
      </button>

      <h1>Application Details</h1>
      <p>Review candidate information and application details.</p>
    </div>

    <div v-if="loading" class="message-card">
      Loading application...
    </div>

    <div v-else-if="error" class="message-card error-message">
      {{ error }}
    </div>

    <div v-else-if="application" class="details-grid">

      <!-- Candidate Header -->
      <section class="details-card candidate-card">
        <div class="candidate-header">
          <div class="avatar">
            {{ getInitials(application.full_name) }}
          </div>

          <div>
            <h2>{{ application.full_name }}</h2>
            <p>Application #{{ application.id }}</p>
          </div>
        </div>

        <div class="status-row">
          <span class="label">Status</span>

          <span
            class="status"
            :class="application.status"
          >
            {{ application.status }}
          </span>
        </div>
      </section>

      <!-- Candidate Information -->
      <section class="details-card">
        <h2>Candidate Information</h2>

        <div class="information-grid">
          <div class="information-item">
            <span class="label">Full Name</span>
            <strong>{{ application.full_name }}</strong>
          </div>

          <div class="information-item">
            <span class="label">Email</span>
            <strong>{{ application.email }}</strong>
          </div>

          <div class="information-item">
            <span class="label">Phone</span>
            <strong>{{ application.phone }}</strong>
          </div>

          <div class="information-item">
            <span class="label">Position</span>
            <strong>{{ jobTitle }}</strong>
          </div>

          <div class="information-item">
            <span class="label">Application Date</span>
            <strong>
              {{ formatDate(application.created_at) }}
            </strong>
          </div>

          <div class="information-item">
            <span class="label">CV Filename</span>
            <strong>{{ application.cv_filename }}</strong>
          </div>
        </div>
      </section>

      <!-- Cover Letter -->
      <section class="details-card">
        <h2>Cover Letter</h2>

        <div class="text-content">
          {{ application.cover_letter }}
        </div>
      </section>

      <!-- CV -->
      <section class="details-card">
        <h2>CV Information</h2>

        <div
          v-if="application.cv_text"
          class="cv-preview"
        >
          {{ application.cv_text }}
        </div>

        <div
          v-else
          class="empty-message"
        >
          No extracted CV text is available for this application.
        </div>
      </section>

      <!-- Candidate Actions -->
      <section class="details-card">
        <h2>Candidate Actions</h2>

        <div class="action-buttons">

          <!-- AI Analysis -->
          <button
            class="primary-button"
            :disabled="generatingAnalysis"
            @click="generateAnalysis"
          >
            <span v-if="generatingAnalysis">
              ⏳ Generating AI Analysis...
            </span>

            <span v-else>
              🤖 AI Analysis
            </span>
          </button>

          <!-- Change Status -->
          <button
            class="secondary-button"
            :disabled="updatingStatus"
            @click="showStatusSelector = !showStatusSelector"
          >
            {{ updatingStatus ? 'Updating...' : 'Change Status' }}
          </button>

        </div>

        <!-- Status Selector -->
        <div
          v-if="showStatusSelector"
          class="status-selector"
        >
          <label for="status">
            Select new status
          </label>

          <select
            id="status"
            v-model="selectedStatus"
            :disabled="updatingStatus"
          >
            <option value="" disabled>
              Choose a status
            </option>

            <option
              v-for="status in statuses"
              :key="status"
              :value="status"
            >
              {{ status }}
            </option>
          </select>

          <button
            class="update-status-button"
            :disabled="!selectedStatus || updatingStatus"
            @click="updateStatus"
          >
            {{ updatingStatus ? 'Updating...' : 'Update Status' }}
          </button>
        </div>

        <!-- AI Analysis Message -->
        <p
          v-if="generatingAnalysis"
          class="analysis-message"
        >
          The AI is reading the candidate's CV and comparing
          it with the job requirements. This may take a few minutes.
        </p>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import {
  computed,
  onMounted,
  ref
} from 'vue'

import {
  useRoute,
  useRouter
} from 'vue-router'

import api from '../services/api'

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

const application = ref<Application | null>(null)
const jobs = ref<Job[]>([])

const loading = ref(true)
const generatingAnalysis = ref(false)
const updatingStatus = ref(false)
const showStatusSelector = ref(false)
const selectedStatus = ref('')
const error = ref('')

const statuses = [
  'pending',
  'reviewing',
  'shortlisted',
  'interview',
  'rejected',
  'hired'
]

const jobTitle = computed(() => {
  if (!application.value) {
    return ''
  }

  const job = jobs.value.find(
    (job) => job.id === application.value?.job_id
  )

  return job
    ? job.title
    : `Job #${application.value.job_id}`
})

async function fetchApplication() {
  const applicationId = Number(route.params.id)

  const response = await api.get<Application>(
    `/applications/${applicationId}`
  )

  application.value = response.data
}

async function fetchJobs() {
  const response = await api.get<Job[]>(
    '/jobs/'
  )

  jobs.value = response.data
}

async function loadData() {
  try {
    loading.value = true
    error.value = ''

    await Promise.all([
      fetchApplication(),
      fetchJobs()
    ])
  } catch (err) {
    console.error(
      'Failed to load application details:',
      err
    )

    error.value =
      'Unable to load application details.'
  } finally {
    loading.value = false
  }
}

async function generateAnalysis() {
  if (!application.value) {
    return
  }

  try {
    generatingAnalysis.value = true
    error.value = ''

    const applicationId = application.value.id

    await api.post(
      `/candidate-analysis/generate/${applicationId}`
    )

    router.push(
      `/analysis?application_id=${applicationId}`
    )
  } catch (err) {
    console.error(
      'Failed to generate candidate analysis:',
      err
    )

    error.value =
      'Unable to generate AI analysis. Please try again.'
  } finally {
    generatingAnalysis.value = false
  }
}

async function updateStatus() {
  if (!application.value || !selectedStatus.value) {
    return
  }

  try {
    updatingStatus.value = true
    error.value = ''

    const applicationId = application.value.id

    const response = await api.patch<Application>(
      `/applications/${applicationId}/status`,
      {
        status: selectedStatus.value
      }
    )

    application.value = response.data

    showStatusSelector.value = false
    selectedStatus.value = ''
  } catch (err) {
    console.error(
      'Failed to update application status:',
      err
    )

    error.value =
      'Unable to update application status. Please try again.'
  } finally {
    updatingStatus.value = false
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

function formatDate(date: string) {
  return new Date(date).toLocaleDateString(
    'en-GB',
    {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    }
  )
}

function goBack() {
  router.push('/applications')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.details-page {
  padding: 30px;
}

.page-header {
  margin-bottom: 25px;
}

.back-button {
  padding: 0;
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
  margin: 14px 0 0;
  color: #111827;
  font-size: 28px;
}

.page-header p {
  margin: 7px 0 0;
  color: #6b7280;
  font-size: 14px;
}

.details-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.details-card {
  padding: 24px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.details-card h2 {
  margin: 0 0 20px;
  color: #111827;
  font-size: 18px;
}

.candidate-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.candidate-header {
  display: flex;
  align-items: center;
  gap: 15px;
}

.avatar {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #eff6ff;
  color: #2563eb;
  font-size: 17px;
  font-weight: 700;
}

.candidate-header h2 {
  margin: 0;
  font-size: 20px;
}

.candidate-header p {
  margin: 5px 0 0;
  color: #6b7280;
  font-size: 13px;
}

.status-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.label {
  color: #6b7280;
  font-size: 12px;
}

.status {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.status.pending {
  background: #fef3c7;
  color: #92400e;
}

.status.reviewing {
  background: #dbeafe;
  color: #1e40af;
}

.status.shortlisted {
  background: #dcfce7;
  color: #166534;
}

.status.interview {
  background: #ede9fe;
  color: #6d28d9;
}

.status.rejected {
  background: #fee2e2;
  color: #991b1b;
}

.status.hired {
  background: #dcfce7;
  color: #166534;
}

.information-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.information-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.information-item strong {
  color: #111827;
  font-size: 14px;
  word-break: break-word;
}

.text-content {
  padding: 18px;
  border-radius: 8px;
  background: #f8fafc;
  color: #374151;
  line-height: 1.7;
  white-space: pre-wrap;
  font-size: 14px;
}

.cv-preview {
  max-height: 500px;
  overflow-y: auto;
  padding: 18px;
  border-radius: 8px;
  background: #f8fafc;
  color: #374151;
  line-height: 1.6;
  white-space: pre-wrap;
  font-size: 13px;
}

.empty-message {
  padding: 20px;
  text-align: center;
  color: #6b7280;
  background: #f8fafc;
  border-radius: 8px;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.primary-button,
.secondary-button {
  padding: 11px 18px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.primary-button {
  border: none;
  background: #2563eb;
  color: white;
}

.primary-button:hover {
  background: #1d4ed8;
}

.primary-button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.secondary-button {
  border: 1px solid #d1d5db;
  background: white;
  color: #374151;
}

.secondary-button:hover {
  background: #f9fafb;
}

.secondary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.status-selector {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
  padding: 15px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.status-selector label {
  color: #374151;
  font-size: 13px;
  font-weight: 600;
}

.status-selector select {
  padding: 9px 12px;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  background: white;
  color: #374151;
  font-size: 13px;
  cursor: pointer;
}

.status-selector select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.update-status-button {
  padding: 9px 14px;
  border: none;
  border-radius: 7px;
  background: #2563eb;
  color: white;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.update-status-button:hover {
  background: #1d4ed8;
}

.update-status-button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.analysis-message {
  margin: 15px 0 0;
  color: #6b7280;
  font-size: 13px;
  line-height: 1.6;
}

.message-card {
  padding: 50px;
  text-align: center;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  color: #6b7280;
}

.error-message {
  color: #b91c1c;
}

@media (max-width: 700px) {
  .details-page {
    padding: 20px;
  }

  .candidate-card {
    align-items: flex-start;
    flex-direction: column;
    gap: 15px;
  }

  .information-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .primary-button,
  .secondary-button {
    width: 100%;
  }

  .status-selector {
    align-items: stretch;
    flex-direction: column;
  }

  .status-selector select,
  .update-status-button {
    width: 100%;
  }
}
</style>
