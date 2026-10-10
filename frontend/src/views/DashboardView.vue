<template>
  <div class="dashboard-page">
    <div class="page-header">
      <div>
        <h1>Dashboard</h1>
        <p>Overview of your recruitment activities.</p>
      </div>

      <button class="primary-button">
        + Create Job
      </button>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">💼</div>

        <div>
          <span>Total Jobs</span>
          <strong>1</strong>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📄</div>

        <div>
          <span>Total Applications</span>
          <strong>1</strong>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">⏳</div>

        <div>
          <span>Pending Applications</span>
          <strong>1</strong>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">🤖</div>

        <div>
          <span>AI Analyses</span>
          <strong>1</strong>
        </div>
      </div>
    </div>

    <section class="content-card">
      <div class="section-header">
        <div>
          <h2>Recent Applications</h2>
          <p>Latest applications submitted by candidates.</p>
        </div>

        <RouterLink to="/applications" class="view-all">
          View All
        </RouterLink>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Candidate</th>
              <th>Position</th>
              <th>Status</th>
              <th>Date</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>
                <strong>Eve Ndanu</strong>
                <span class="email">
                  evendanu@gmail.com
                </span>
              </td>

              <td>Junior Python Developer</td>

              <td>
                <span class="status pending">
                  Pending
                </span>
              </td>

              <td>02 Oct 2026</td>

              <td>
                <RouterLink
                  to="/applications"
                  class="action-button"
                >
                  View
                </RouterLink>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.dashboard-page {
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

.primary-button {
  padding: 11px 18px;
  border: none;
  border-radius: 8px;
  background: #2563eb;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.primary-button:hover {
  background: #1d4ed8;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-bottom: 28px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.stat-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eff6ff;
  border-radius: 10px;
  font-size: 20px;
}

.stat-card span {
  display: block;
  color: #6b7280;
  font-size: 13px;
}

.stat-card strong {
  display: block;
  margin-top: 4px;
  color: #111827;
  font-size: 24px;
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

.view-all {
  color: #2563eb;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
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
}

.email {
  display: block;
  margin-top: 4px;
  color: #6b7280;
  font-size: 12px;
}

.status {
  display: inline-block;
  padding: 5px 9px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.status.pending {
  background: #fef3c7;
  color: #92400e;
}

.action-button {
  display: inline-block;
  padding: 6px 11px;
  border: 1px solid #dbeafe;
  border-radius: 6px;
  color: #2563eb;
  text-decoration: none;
  font-size: 12px;
  font-weight: 600;
}

.action-button:hover {
  background: #eff6ff;
}

@media (max-width: 1000px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 650px) {
  .dashboard-page {
    padding: 20px;
  }

  .page-header {
    align-items: flex-start;
    gap: 15px;
    flex-direction: column;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
