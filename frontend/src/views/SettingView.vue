<template>
  <div class="page">
    <header class="page-header">
      <h1>Settings</h1>
      <p>Manage your recruiter account and platform settings.</p>
    </header>

    <section class="settings-card">
      <h2>Profile</h2>

      <div class="form-grid">
        <div class="form-group">
          <label>Full Name</label>
          <input
            type="text"
            value="Recruiter"
          />
        </div>

        <div class="form-group">
          <label>Email Address</label>
          <input
            type="email"
            value="admin@chesrhire.ai"
          />
        </div>

        <div class="form-group">
          <label>Role</label>
          <input
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
      <h2>AI Settings</h2>

      <div class="setting-row">
        <div>
          <strong>Candidate AI Analysis</strong>
          <p>
            Enable AI-powered CV analysis for candidate applications.
          </p>
        </div>

        <input
          type="checkbox"
          checked
        />
      </div>
    </section>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  padding: 30px;
  background: #f4f7fb;
}

.page-header {
  margin-bottom: 25px;
}

.page-header h1 {
  margin: 0;
  color: #111827;
}

.page-header p {
  margin-top: 6px;
  color: #6b7280;
}

.settings-card {
  margin-bottom: 20px;
  padding: 25px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.settings-card h2 {
  margin-top: 0;
  color: #111827;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 7px;
  color: #374151;
  font-size: 14px;
  font-weight: 600;
}

.form-group input {
  width: 100%;
  box-sizing: border-box;
  padding: 11px;
  border: 1px solid #d1d5db;
  border-radius: 7px;
}

.save-button {
  margin-top: 20px;
  padding: 11px 18px;
  border: none;
  border-radius: 7px;
  background: #2563eb;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.setting-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.setting-row p {
  margin-top: 5px;
  color: #6b7280;
  font-size: 13px;
}

@media (max-width: 700px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
