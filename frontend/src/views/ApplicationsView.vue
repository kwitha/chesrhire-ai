<template>
  <div class="page">
    <header class="page-header">
      <div>
        <h1>Applications</h1>
        <p>Review and manage candidate applications.</p>
      </div>

```
  <select v-model="selectedStatus">
    <option value="all">All Applications</option>
    <option value="pending">Pending</option>
    <option value="reviewing">Reviewing</option>
    <option value="shortlisted">Shortlisted</option>
    <option value="interview">Interview</option>
    <option value="rejected">Rejected</option>
    <option value="hired">Hired</option>
  </select>
</header>

<section class="applications-card">
  <div class="table-wrapper">
    <table>
      <thead>
        <tr>
          <th>Candidate</th>
          <th>Position</th>
          <th>Email</th>
          <th>Status</th>
          <th>Applied</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-if="loading">
          <td colspan="6" class="message-cell">
            Loading applications...
          </td>
        </tr>

        <tr v-else-if="error">
          <td colspan="6" class="message-cell error-message">
            {{ error }}
          </td>
        </tr>

        <tr v-else-if="filteredApplications.length === 0">
          <td colspan="6" class="message-cell">
            No applications found.
          </td>
        </tr>

        <tr
          v-for="application in filteredApplications"
          :key="application.id"
        >
          <td>
            <div class="candidate">
              <div class="avatar">
                {{ getInitials(application.full_name) }}
              </div>

              <div>
                <strong>
                  {{ application.full_name }}
                </strong>

                <span>
                  Application #{{ application.id }}
                </span>
              </div>
            </div>
          </td>

          <td>
            {{ getJobTitle(application.job_id) }}
          </td>

          <td>
            {{ application.email }}
          </td>

          <td>
            <span
              class="status"
              :class="application.status"
            >
              {{ application.status }}
            </span>
          </td>

          <td>
            {{ formatDate(application.created_at) }}
          </td>

          <td>
            <button
              class="view-button"
              @click="viewApplication(application.id)"
            >
              View
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
```

  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
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

const router = useRouter()

const applications = ref<Application[]>([])
const jobs = ref<Job[]>([])

const selectedStatus = ref('all')
const loading = ref(true)
const error = ref('')

const filteredApplications = computed(() => {
  if (selectedStatus.value === 'all') {
    return applications.value
  }

  return applications.value.filter(
    (application) =>
      application.status === selectedStatus.value
  )
})

function getJobTitle(jobId: number) {
  const job = jobs.value.find(
    (job) => job.id === jobId
  )

  return job
    ? job.title
    : `Job #${jobId}`
}

async function fetchApplications() {
  const response = await api.get<Application[]>(
    '/applications/'
  )

  applications.value = response.data
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
      fetchApplications(),
      fetchJobs()
    ])
  } catch (err) {
    console.error(
      'Failed to load applications or jobs:',
      err
    )

    error.value =
      'Unable to load applications from the server.'
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

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

function viewApplication(applicationId: number) {
  router.push(`/applications/${applicationId}`)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page {
  padding: 30px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
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

select {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 13px;
  cursor: pointer;
}

select:focus {
  outline: none;
  border-color: #2563eb;
}

.applications-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 16px 20px;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
  font-size: 13px;
}

th {
  background: #f8fafc;
  color: #6b7280;
  font-weight: 600;
}

td {
  color: #374151;
}

.candidate {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border-radius: 50%;
  background: #eff6ff;
  color: #2563eb;
  font-size: 13px;
  font-weight: 700;
}

.candidate strong {
  display: block;
  color: #111827;
  font-size: 13px;
}

.candidate span {
  display: block;
  margin-top: 4px;
  color: #9ca3af;
  font-size: 12px;
}

.status {
  display: inline-block;
  padding: 5px 9px;
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

.view-button {
  padding: 6px 11px;
  border: 1px solid #dbeafe;
  border-radius: 6px;
  background: white;
  color: #2563eb;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.view-button:hover {
  background: #eff6ff;
}

.message-cell {
  padding: 40px;
  text-align: center;
  color: #6b7280;
}

.error-message {
  color: #b91c1c;
}

@media (max-width: 800px) {
  .page {
    padding: 20px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
    gap: 15px;
  }

  select {
    width: 100%;
  }
}
</style>
