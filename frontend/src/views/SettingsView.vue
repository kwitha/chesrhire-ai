<template>
  <div class="settings-page">
    <div class="page-header">
      <div>
        <h1>Settings</h1>
        <p>Manage your recruiter account and AI preferences.</p>
      </div>
    </div>

    <section class="settings-card">
      <div class="section-header">
        <h2>Profile</h2>
        <p>Update your account information.</p>
      </div>

      <div class="form-grid">
        <div class="form-group">
          <label for="name">Full Name</label>
          <input
            id="name"
            type="text"
            value="Recruiter"
          />
        </div>

        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            id="email"
            type="email"
            value="admin@chesrhire.ai"
          />
        </div>

        <div class="form-group">
          <label for="role">Role</label>
          <input
            id="role"
            type="text"
            value="Administrator"
            disabled
          />
        </div>
      </div>

      <button class="save-button">
        Save Changes
      </button>
    </section>

    <section class="settings-card">
      <div class="section-header">
        <h2>AI Settings</h2>
        <p>Configure AI-powered recruitment features.</p>
      </div>

      <label class="checkbox-row">
        <input
          type="checkbox"
          checked
        />

        <span>
          <strong>Candidate AI Analysis</strong>
          <small>
            Automatically analyze candidate CVs against job requirements.
          </small>
        </span>
      </label>
    </section>
  </div>
</template>

<style scoped>
.settings-page {
  padding: 32px;
  background: #f8fafc;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 28px;
}

.page-header h1 {
  margin: 0;
  color: #111827;
  font-size: 28px;
}

.page-header p {
  margin-top: 8px;
  color: #6b7280;
}

.settings-card {
  background: white;
  border-radius: 12px;
  padding: 28px;
  margin-bottom: 24px;
  border: 1px solid #e5e7eb;
}

.section-header {
  margin-bottom: 24px;
}

.section-header h2 {
  margin: 0;
  color: #111827;
  font-size: 20px;
}

.section-header p {
  margin-top: 6px;
  color: #6b7280;
  font-size: 14px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
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
  padding: 11px 13px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
}

.form-group input:disabled {
  background: #f3f4f6;
  color: #6b7280;
}

.save-button {
  margin-top: 24px;
  padding: 11px 18px;
  border: none;
  border-radius: 8px;
  background: #2563eb;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.save-button:hover {
  background: #1d4ed8;
}

.checkbox-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
}

.checkbox-row input {
  margin-top: 3px;
  width: 16px;
  height: 16px;
}

.checkbox-row span {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.checkbox-row strong {
  color: #374151;
  font-size: 14px;
}

.checkbox-row small {
  color: #6b7280;
  font-size: 13px;
}

@media (max-width: 700px) {
  .settings-page {
    padding: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
