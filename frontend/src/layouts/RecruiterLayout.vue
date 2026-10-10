
<template>
  <div class="recruiter-layout">
    <aside class="sidebar">
      <div class="brand">
        <h1>ChesrHire AI</h1>
        <p>Recruitment Platform</p>
      </div>

      <nav class="navigation">
        <RouterLink to="/dashboard" class="nav-item">
          <span>📊</span>
          <span>Dashboard</span>
        </RouterLink>

        <RouterLink to="/jobs" class="nav-item">
          <span>💼</span>
          <span>Jobs</span>
        </RouterLink>

        <RouterLink to="/applications" class="nav-item">
          <span>📄</span>
          <span>Applications</span>
        </RouterLink>

        <RouterLink to="/analysis" class="nav-item">
          <span>🤖</span>
          <span>AI Analysis</span>
        </RouterLink>

        <RouterLink to="/settings" class="nav-item">
          <span>⚙️</span>
          <span>Settings</span>
        </RouterLink>
      </nav>

      <div class="sidebar-bottom">
        <button
          class="logout-button"
          type="button"
          @click="logout"
        >
          <span>🚪</span>
          <span>Sign Out</span>
        </button>
      </div>
    </aside>

    <div class="main-area">
      <header class="topbar">
        <div>
          <h2>Recruiter Portal</h2>
          <p>Manage your recruitment activities</p>
        </div>

        <div class="profile">
          <div class="profile-avatar">
            {{ recruiterInitial }}
          </div>

          <div class="profile-info">
            <strong>{{ recruiterName }}</strong>
            <span>Administrator</span>
          </div>
        </div>
      </header>

      <main class="content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'

const router = useRouter()

interface Recruiter {
  full_name?: string
  name?: string
  email?: string
}

const recruiter = computed<Recruiter | null>(() => {
  try {
    const savedRecruiter = localStorage.getItem('recruiter')

    if (!savedRecruiter) {
      return null
    }

    return JSON.parse(savedRecruiter) as Recruiter
  } catch {
    return null
  }
})

const recruiterName = computed(() => {
  return (
    recruiter.value?.full_name ||
    recruiter.value?.name ||
    'Recruiter'
  )
})

const recruiterInitial = computed(() => {
  return recruiterName.value.charAt(0).toUpperCase() || 'R'
})

async function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('recruiter')

  await router.replace({ name: 'login' })
}
</script>

<style scoped>
.recruiter-layout {
  min-height: 100vh;
  display: flex;
  background: #f8fafc;
}

/* Sidebar */

.sidebar {
  width: 250px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #111827;
  color: white;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  overflow-y: auto;
}

.brand {
  padding: 28px 22px;
  border-bottom: 1px solid #1f2937;
}

.brand h1 {
  margin: 0;
  font-size: 22px;
}

.brand p {
  margin: 6px 0 0;
  color: #9ca3af;
  font-size: 12px;
}

.navigation {
  padding: 20px 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 8px;
  color: #d1d5db;
  text-decoration: none;
  font-size: 14px;
  transition: background 0.2s, color 0.2s;
}

.nav-item:hover {
  background: #1f2937;
  color: white;
}

.nav-item.router-link-active {
  background: #2563eb;
  color: white;
}

.sidebar-bottom {
  margin-top: auto;
  padding: 16px 12px;
  border-top: 1px solid #1f2937;
}

.logout-button {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #d1d5db;
  cursor: pointer;
  font-size: 14px;
  text-align: left;
  transition: background 0.2s, color 0.2s;
}

.logout-button:hover {
  background: #1f2937;
  color: white;
}

.logout-button:focus-visible {
  outline: 2px solid #60a5fa;
  outline-offset: 2px;
}

/* Main area */

.main-area {
  flex: 1;
  margin-left: 250px;
  min-width: 0;
}

/* Topbar */

.topbar {
  min-height: 76px;
  padding: 12px 30px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.topbar h2 {
  margin: 0;
  color: #111827;
  font-size: 18px;
}

.topbar p {
  margin: 4px 0 0;
  color: #6b7280;
  font-size: 13px;
}

.profile {
  display: flex;
  align-items: center;
  gap: 10px;
}

.profile-avatar {
  width: 38px;
  height: 38px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #2563eb;
  color: white;
  font-weight: 700;
}

.profile-info {
  display: flex;
  flex-direction: column;
}

.profile-info strong {
  color: #374151;
  font-size: 14px;
}

.profile-info span {
  margin-top: 2px;
  color: #6b7280;
  font-size: 12px;
}

/* Content */

.content {
  min-height: calc(100vh - 76px);
}

/* Responsive */

@media (max-width: 768px) {
  .sidebar {
    width: 210px;
  }

  .main-area {
    margin-left: 210px;
  }

  .topbar {
    padding: 12px 20px;
  }

  .profile-info {
    display: none;
  }
}

@media (max-width: 600px) {
  .sidebar {
    width: 70px;
  }

  .brand {
    padding: 20px 10px;
    text-align: center;
  }

  .brand h1 {
    font-size: 14px;
    overflow-wrap: anywhere;
  }

  .brand p {
    display: none;
  }

  .navigation {
    padding: 15px 8px;
  }

  .nav-item {
    justify-content: center;
    padding: 12px 8px;
  }

  .nav-item span:last-child {
    display: none;
  }

  .logout-button {
    justify-content: center;
    padding: 12px 8px;
  }

  .logout-button span:last-child {
    display: none;
  }

  .main-area {
    margin-left: 70px;
  }

  .topbar {
    padding: 12px;
  }

  .topbar h2 {
    font-size: 16px;
  }

  .topbar p {
    font-size: 11px;
  }
}
</style>
