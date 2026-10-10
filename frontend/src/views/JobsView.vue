
<template>
  <div class="jobs-page">
    <div class="page-header">
      <div>
        <h1>Jobs</h1>
        <p>Manage your job vacancies and recruitment positions.</p>
      </div>

      <button class="primary-button" @click="openCreateForm">
        + Create Job
      </button>
    </div>

    <!-- Feedback messages -->
    <div v-if="successMessage" class="alert success-alert">
      {{ successMessage }}
    </div>

    <div v-if="error" class="alert error-alert">
      {{ error }}
    </div>

    <!-- Jobs table -->
    <section class="content-card">
      <div class="section-header">
        <div>
          <h2>Job Vacancies</h2>
          <p>Currently available positions.</p>
        </div>

        <span class="job-count">
          {{ jobs.length }} {{ jobs.length === 1 ? 'Job' : 'Jobs' }}
        </span>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Location</th>
              <th>Employment Type</th>
              <th>Applications</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="loading">
              <td colspan="6" class="message-cell">
                Loading jobs...
              </td>
            </tr>

            <tr v-else-if="jobs.length === 0">
              <td colspan="6" class="message-cell">
                No jobs found. Click "Create Job" to add your first vacancy.
              </td>
            </tr>

            <tr v-for="job in jobs" :key="job.id">
              <td>
                <strong>{{ job.title }}</strong>
                <span class="job-id">Job #{{ job.id }}</span>
              </td>

              <td>{{ job.location }}</td>

              <td>{{ job.employment_type }}</td>

              <td>—</td>

              <td>
                <span class="status" :class="job.status">
                  {{ job.status }}
                </span>
              </td>

              <td>
                <div class="actions">
                  <button
                    class="action-button"
                    @click="viewJob(job.id)"
                  >
                    View
                  </button>

                  <button
                    class="action-button edit"
                    @click="openEditForm(job.id)"
                  >
                    Edit
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Create/Edit modal -->
    <div
      v-if="showForm"
      class="modal-overlay"
      @click.self="closeForm"
    >
      <section class="modal-card">
        <div class="modal-header">
          <div>
            <h2>{{ editingJobId ? 'Edit Job' : 'Create Job' }}</h2>
            <p>
              {{
                editingJobId
                  ? 'Update the vacancy details below.'
                  : 'Enter the details for the new vacancy.'
              }}
            </p>
          </div>

          <button
            class="close-button"
            type="button"
            aria-label="Close form"
            :disabled="saving"
            @click="closeForm"
          >
            &times;
          </button>
        </div>

        <form class="job-form" @submit.prevent="saveJob">
          <div class="form-group">
            <label for="title">Job Title *</label>
            <input
              id="title"
              v-model.trim="form.title"
              type="text"
              maxlength="255"
              placeholder="e.g. Junior Python Developer"
              required
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="location">Location *</label>
              <input
                id="location"
                v-model.trim="form.location"
                type="text"
                maxlength="255"
                placeholder="e.g. Nairobi, Kenya"
                required
              />
            </div>

            <div class="form-group">
              <label for="employmentType">Employment Type *</label>
              <select
                id="employmentType"
                v-model="form.employment_type"
                required
              >
                <option value="" disabled>Select type</option>
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Contract">Contract</option>
                <option value="Internship">Internship</option>
                <option value="Temporary">Temporary</option>
                <option value="Remote">Remote</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label for="description">Job Description *</label>
            <textarea
              id="description"
              v-model.trim="form.description"
              rows="5"
              placeholder="Describe the role and responsibilities..."
              required
            ></textarea>
          </div>

          <div class="form-group">
            <label for="requirements">Requirements *</label>
            <textarea
              id="requirements"
              v-model.trim="form.requirements"
              rows="4"
              placeholder="List the qualifications, skills and experience..."
              required
            ></textarea>
          </div>

          <div class="form-group">
            <label for="closingDate">Application Closing Date</label>
            <input
              id="closingDate"
              v-model="form.closing_date"
              type="date"
            />
          </div>

          <p v-if="formError" class="form-error">
            {{ formError }}
          </p>

          <div class="form-actions">
            <button
              type="button"
              class="secondary-button"
              :disabled="saving"
              @click="closeForm"
            >
              Cancel
            </button>

            <button
              type="submit"
              class="primary-button"
              :disabled="saving"
            >
              {{
                saving
                  ? 'Saving...'
                  : editingJobId
                    ? 'Save Changes'
                    : 'Create Job'
              }}
            </button>
          </div>
        </form>
      </section>
    </div>

    <!-- Job details modal -->
    <div
      v-if="selectedJob"
      class="modal-overlay"
      @click.self="selectedJob = null"
    >
      <section class="modal-card details-card">
        <div class="modal-header">
          <div>
            <h2>Job Details</h2>
            <p>Job #{{ selectedJob.id }}</p>
          </div>

          <button
            class="close-button"
            type="button"
            aria-label="Close job details"
            @click="selectedJob = null"
          >
            &times;
          </button>
        </div>

        <div class="job-details">
          <div class="detail-heading">
            <h3>{{ selectedJob.title }}</h3>
            <span class="status" :class="selectedJob.status">
              {{ selectedJob.status }}
            </span>
          </div>

          <div class="detail-grid">
            <div>
              <span class="detail-label">Location</span>
              <strong>{{ selectedJob.location }}</strong>
            </div>

            <div>
              <span class="detail-label">Employment Type</span>
              <strong>{{ selectedJob.employment_type }}</strong>
            </div>

            <div>
              <span class="detail-label">Closing Date</span>
              <strong>{{ formatDate(selectedJob.closing_date) }}</strong>
            </div>

            <div>
              <span class="detail-label">Date Created</span>
              <strong>{{ formatDate(selectedJob.created_at) }}</strong>
            </div>
          </div>

          <div class="detail-section">
            <h4>Job Description</h4>
            <p class="preserve-lines">{{ selectedJob.description }}</p>
          </div>

          <div class="detail-section">
            <h4>Requirements</h4>
            <p class="preserve-lines">{{ selectedJob.requirements }}</p>
          </div>
        </div>

        <div class="form-actions">
          <button
            class="secondary-button"
            @click="selectedJob = null"
          >
            Close
          </button>

          <button
            class="primary-button"
            @click="openEditForm(selectedJob.id)"
          >
            Edit Job
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import axios from 'axios'
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

interface JobForm {
  title: string
  description: string
  requirements: string
  location: string
  employment_type: string
  closing_date: string
}

function emptyForm(): JobForm {
  return {
    title: '',
    description: '',
    requirements: '',
    location: '',
    employment_type: '',
    closing_date: '',
  }
}

const jobs = ref<Job[]>([])
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const formError = ref('')
const successMessage = ref('')

const showForm = ref(false)
const editingJobId = ref<number | null>(null)
const selectedJob = ref<Job | null>(null)

const form = reactive<JobForm>(emptyForm())

function clearMessages() {
  error.value = ''
  formError.value = ''
  successMessage.value = ''
}

function resetForm() {
  Object.assign(form, emptyForm())
  editingJobId.value = null
  formError.value = ''
}

function openCreateForm() {
  clearMessages()
  selectedJob.value = null
  resetForm()
  showForm.value = true
}

function closeForm() {
  if (saving.value) return

  showForm.value = false
  resetForm()
}

async function fetchJobs() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get<Job[]>('/jobs/')
    jobs.value = response.data
  } catch (err: unknown) {
    console.error('Failed to fetch jobs:', err)

    if (axios.isAxiosError(err) && err.response?.status === 401) {
      error.value = 'Your session has expired. Please log in again.'
    } else {
      error.value = 'Unable to load jobs from the server. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

async function viewJob(jobId: number) {
  clearMessages()
  selectedJob.value = null

  try {
    const response = await api.get<Job>(`/jobs/${jobId}`)
    selectedJob.value = response.data
  } catch (err: unknown) {
    console.error('Failed to fetch job details:', err)

    error.value =
      axios.isAxiosError(err) && err.response?.status === 404
        ? 'This job could not be found.'
        : 'Unable to load job details. Please try again.'
  }
}

function toDateInput(value: string | null): string {
  if (!value) return ''

  return value.slice(0, 10)
}

async function openEditForm(jobId: number) {
  clearMessages()

  try {
    let job = jobs.value.find((item) => item.id === jobId)

    if (!job) {
      const response = await api.get<Job>(`/jobs/${jobId}`)
      job = response.data
    }

    Object.assign(form, {
      title: job.title,
      description: job.description,
      requirements: job.requirements,
      location: job.location,
      employment_type: job.employment_type,
      closing_date: toDateInput(job.closing_date),
    })

    editingJobId.value = job.id
    selectedJob.value = null
    showForm.value = true
  } catch (err: unknown) {
    console.error('Failed to load job for editing:', err)
    error.value = 'Unable to load this job for editing.'
  }
}

async function saveJob() {
  if (saving.value) return

  formError.value = ''

  if (
    !form.title.trim() ||
    !form.description.trim() ||
    !form.requirements.trim() ||
    !form.location.trim() ||
    !form.employment_type
  ) {
    formError.value = 'Please complete all required fields.'
    return
  }

  saving.value = true

  try {
    const payload = {
      title: form.title.trim(),
      description: form.description.trim(),
      requirements: form.requirements.trim(),
      location: form.location.trim(),
      employment_type: form.employment_type,
      closing_date: form.closing_date
        ? `${form.closing_date}T23:59:00`
        : null,
    }

    if (editingJobId.value !== null) {
      await api.put<Job>(`/jobs/${editingJobId.value}`, payload)
      successMessage.value = 'Job updated successfully.'
    } else {
      await api.post<Job>('/jobs/', payload)
      successMessage.value = 'Job created successfully.'
    }

    showForm.value = false
    resetForm()

    await fetchJobs()
  } catch (err: unknown) {
    console.error('Failed to save job:', err)

    if (axios.isAxiosError(err)) {
      if (err.response?.status === 401) {
        formError.value = 'Your session has expired. Please log in again.'
      } else if (err.response?.status === 422) {
        formError.value =
          'Some job details are invalid. Please review the form.'
      } else {
        formError.value = 'Unable to save the job. Please try again.'
      }
    } else {
      formError.value = 'An unexpected error occurred.'
    }
  } finally {
    saving.value = false
  }
}

function formatDate(value: string | null): string {
  if (!value) return 'Not specified'

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) return 'Not specified'

  return new Intl.DateTimeFormat('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(date)
}

onMounted(fetchJobs)
</script>

<style scoped>
.jobs-page {
  padding: 30px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
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

.primary-button {
  padding: 11px 18px;
  border: none;
  border-radius: 8px;
  background: #2563eb;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.primary-button:hover {
  background: #1d4ed8;
}

.primary-button:disabled,
.secondary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.content-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.section-header {
  padding: 22px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.job-count {
  padding: 6px 10px;
  border-radius: 6px;
  background: #eff6ff;
  color: #2563eb;
  font-size: 12px;
  font-weight: 600;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 16px 24px;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
  font-size: 13px;
  white-space: nowrap;
}

th {
  background: #f8fafc;
  color: #6b7280;
  font-weight: 600;
}

td {
  color: #374151;
}

td strong {
  display: block;
  color: #111827;
  font-size: 13px;
}

.job-id {
  display: block;
  margin-top: 4px;
  color: #9ca3af;
  font-size: 12px;
}

.status {
  display: inline-block;
  padding: 5px 9px;
  border-radius: 999px;
  background: #f3f4f6;
  color: #374151;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.status.open {
  background: #dcfce7;
  color: #166534;
}

.status.closed {
  background: #fee2e2;
  color: #991b1b;
}

.actions {
  display: flex;
  gap: 8px;
}

.action-button {
  padding: 6px 11px;
  border: 1px solid #dbeafe;
  border-radius: 6px;
  background: white;
  color: #2563eb;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.action-button:hover {
  background: #eff6ff;
}

.action-button.edit {
  border-color: #e5e7eb;
  color: #4b5563;
}

.action-button.edit:hover {
  background: #f9fafb;
}

.message-cell {
  padding: 40px;
  text-align: center;
  color: #6b7280;
}

.alert {
  margin-bottom: 18px;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
}

.success-alert {
  border: 1px solid #bbf7d0;
  background: #f0fdf4;
  color: #166534;
}

.error-alert {
  border: 1px solid #fecaca;
  background: #fef2f2;
  color: #b91c1c;
}

/* Modals */

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgb(15 23 42 / 55%);
  overflow-y: auto;
}

.modal-card {
  width: 100%;
  max-width: 720px;
  max-height: calc(100vh - 40px);
  overflow-y: auto;
  background: white;
  border-radius: 14px;
  box-shadow: 0 20px 50px rgb(0 0 0 / 20%);
}

.details-card {
  max-width: 760px;
}

.modal-header {
  padding: 22px 24px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.modal-header h2 {
  margin: 0;
  color: #111827;
  font-size: 20px;
}

.modal-header p {
  margin: 6px 0 0;
  color: #6b7280;
  font-size: 13px;
}

.close-button {
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  border: none;
  border-radius: 7px;
  background: #f3f4f6;
  color: #374151;
  font-size: 24px;
  cursor: pointer;
}

.close-button:hover {
  background: #e5e7eb;
}

.job-form {
  padding: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
  margin-bottom: 18px;
}

.form-group label {
  color: #374151;
  font-size: 13px;
  font-weight: 600;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 11px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  color: #111827;
  font: inherit;
  font-size: 14px;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #2563eb;
  outline: 2px solid rgb(37 99 235 / 12%);
}

.form-group textarea {
  resize: vertical;
  min-height: 90px;
}

.form-error {
  margin: 0 0 16px;
  color: #b91c1c;
  font-size: 13px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 0 24px 24px;
}

.job-form .form-actions {
  padding: 6px 0 0;
}

.secondary-button {
  padding: 10px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.secondary-button:hover {
  background: #f9fafb;
}

/* Job details */

.job-details {
  padding: 24px;
}

.detail-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.detail-heading h3 {
  margin: 0;
  color: #111827;
  font-size: 22px;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin: 24px 0;
  padding: 20px;
  background: #f8fafc;
  border-radius: 10px;
}

.detail-grid > div {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.detail-label {
  color: #6b7280;
  font-size: 12px;
}

.detail-grid strong {
  color: #111827;
  font-size: 13px;
  overflow-wrap: anywhere;
}

.detail-section {
  margin-top: 24px;
}

.detail-section h4 {
  margin: 0 0 10px;
  color: #111827;
  font-size: 15px;
}

.detail-section p {
  margin: 0;
  color: #4b5563;
  font-size: 14px;
  line-height: 1.7;
}

.preserve-lines {
  white-space: pre-line;
}

@media (max-width: 700px) {
  .jobs-page {
    padding: 20px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .page-header > .primary-button {
    width: 100%;
  }

  .section-header {
    align-items: flex-start;
    gap: 12px;
    flex-direction: column;
  }

  th,
  td {
    padding: 13px 16px;
  }

  .form-row,
  .detail-grid {
    grid-template-columns: 1fr;
  }

  .modal-overlay {
    padding: 10px;
  }

  .modal-card {
    max-height: calc(100vh - 20px);
  }

  .modal-header,
  .job-form,
  .job-details {
    padding: 18px;
  }

  .form-actions {
    padding: 0 18px 18px;
  }

  .job-form .form-actions {
    padding: 6px 0 0;
  }
}
</style>
