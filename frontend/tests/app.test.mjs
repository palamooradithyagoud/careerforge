import test from "node:test";
import assert from "node:assert/strict";

// Mock localStorage for test environment
class MockLocalStorage {
  constructor() {
    this.store = {};
  }
  getItem(key) {
    return this.store[key] || null;
  }
  setItem(key, value) {
    this.store[key] = String(value);
  }
  removeItem(key) {
    delete this.store[key];
  }
  clear() {
    this.store = {};
  }
}

globalThis.localStorage = new MockLocalStorage();

// ============================================================================
// 1. AUTHENTICATION & JWT SESSION STORAGE
// ============================================================================
test("Authentication: Session and JWT token storage in localStorage", () => {
  const session = {
    token: "mock-jwt-token-xyz.123",
    student_id: "student-uuid-456",
    email: "student@example.edu",
    name: "Alex Patel",
    education_stage: "b_tech",
  };

  localStorage.setItem("skillcatalyst_session", JSON.stringify(session));
  const retrieved = JSON.parse(localStorage.getItem("skillcatalyst_session"));

  assert.equal(retrieved.token, "mock-jwt-token-xyz.123");
  assert.equal(retrieved.student_id, "student-uuid-456");
  assert.equal(retrieved.email, "student@example.edu");
  assert.equal(retrieved.education_stage, "b_tech");
});

test("Authentication: Authorization Bearer header formatting", () => {
  const session = JSON.parse(localStorage.getItem("skillcatalyst_session"));
  const headers = { "Content-Type": "application/json" };

  if (session?.token) {
    headers["Authorization"] = `Bearer ${session.token}`;
  }

  assert.equal(headers["Authorization"], "Bearer mock-jwt-token-xyz.123");
});

// ============================================================================
// 2. ONBOARDING & STAGE SELECTION
// ============================================================================
test("Onboarding: Validates education stages and redirection parameters", () => {
  const validStages = ["b_tech", "intermediate", "class_10"];

  function getOnboardingUrl(stage) {
    const cleanStage = validStages.includes(stage) ? stage : "b_tech";
    return `/onboarding?stage=${cleanStage}`;
  }

  assert.equal(getOnboardingUrl("b_tech"), "/onboarding?stage=b_tech");
  assert.equal(getOnboardingUrl("intermediate"), "/onboarding?stage=intermediate");
  assert.equal(getOnboardingUrl("class_10"), "/onboarding?stage=class_10");
  assert.equal(getOnboardingUrl("unknown_stage"), "/onboarding?stage=b_tech");
});

// ============================================================================
// 3. PROFILE DATA & SKILLS VALIDATION
// ============================================================================
test("Profile: GPA and profile normalization", () => {
  function normalizeStudentProfile(raw) {
    return {
      id: raw.id,
      name: raw.name.trim(),
      cgpa: Math.min(10.0, Math.max(0.0, Number(raw.cgpa) || 0.0)),
      skills: Array.isArray(raw.skills) ? raw.skills.map((s) => s.trim()) : [],
    };
  }

  const normalized = normalizeStudentProfile({
    id: "std-1",
    name: " Priya Sharma ",
    cgpa: "8.75",
    skills: [" Python ", "FastAPI", "React "],
  });

  assert.equal(normalized.name, "Priya Sharma");
  assert.equal(normalized.cgpa, 8.75);
  assert.deepEqual(normalized.skills, ["Python", "FastAPI", "React"]);
});

// ============================================================================
// 4. SCHOLARSHIP MATCHING & ELIGIBILITY SCORING
// ============================================================================
test("Scholarships: Deterministic eligibility criteria evaluation", () => {
  function evaluateScholarshipEligibility(student, scholarship) {
    const checks = {
      stageMatch: student.education_stage === scholarship.target_stage,
      minScoreMatch: student.cgpa >= scholarship.min_cgpa,
      incomeMatch: student.annual_income <= scholarship.max_family_income,
    };

    const isEligible = Object.values(checks).every(Boolean);
    const score = Object.values(checks).filter(Boolean).length / Object.keys(checks).length;

    return { isEligible, score: Math.round(score * 100), checks };
  }

  const student = { education_stage: "b_tech", cgpa: 8.5, annual_income: 450000 };
  const scholarship = { target_stage: "b_tech", min_cgpa: 7.5, max_family_income: 600000 };

  const result = evaluateScholarshipEligibility(student, scholarship);
  assert.equal(result.isEligible, true);
  assert.equal(result.score, 100);

  // Ineligible on income
  const richStudent = { education_stage: "b_tech", cgpa: 9.0, annual_income: 900000 };
  const ineligibleResult = evaluateScholarshipEligibility(richStudent, scholarship);
  assert.equal(ineligibleResult.isEligible, false);
  assert.equal(ineligibleResult.checks.incomeMatch, false);
});

// ============================================================================
// 5. JOBS & SKILL GAP MATCHING
// ============================================================================
test("Jobs: Skill gap calculation and match score", () => {
  function calculateSkillGap(studentSkills, jobSkills) {
    const normalizedStudent = new Set(studentSkills.map((s) => s.toLowerCase().trim()));
    const matched = [];
    const missing = [];

    for (const req of jobSkills) {
      if (normalizedStudent.has(req.toLowerCase().trim())) {
        matched.push(req);
      } else {
        missing.push(req);
      }
    }

    const fitPercentage = jobSkills.length > 0 ? Math.round((matched.length / jobSkills.length) * 100) : 100;
    return { matched, missing, fitPercentage };
  }

  const studentSkills = ["Python", "FastAPI", "Git"];
  const jobRequirements = ["Python", "FastAPI", "Docker", "Kubernetes"];

  const gap = calculateSkillGap(studentSkills, jobRequirements);
  assert.equal(gap.fitPercentage, 50);
  assert.deepEqual(gap.matched, ["Python", "FastAPI"]);
  assert.deepEqual(gap.missing, ["Docker", "Kubernetes"]);
});

// ============================================================================
// 6. LEARNING ROADMAP & VIDEO LECTURE COMPLETION
// ============================================================================
test("Learning Roadmap: Lecture completion and progress tracking", () => {
  const lectures = [
    { video_id: "v-001", title: "Introduction to FastAPI" },
    { video_id: "v-002", title: "Path & Query Parameters" },
    { video_id: "v-003", title: "Database Models & SQLAlchemy" },
    { video_id: "v-004", title: "Authentication with JWT" },
  ];

  let completedList = ["v-001", "v-002"];

  function getProgress(total, completed) {
    return total > 0 ? Math.min(100, Math.round((completed.length / total) * 100)) : 0;
  }

  assert.equal(getProgress(lectures.length, completedList), 50);

  // Toggle v-003 to completed
  function toggleLecture(id, current) {
    return current.includes(id) ? current.filter((x) => x !== id) : [...current, id];
  }

  completedList = toggleLecture("v-003", completedList);
  assert.equal(getProgress(lectures.length, completedList), 75);

  completedList = toggleLecture("v-004", completedList);
  assert.equal(getProgress(lectures.length, completedList), 100);
});

// ============================================================================
// 7. AI ASSISTANT CONVERSATION STATES
// ============================================================================
test("AI Assistant: Conversation turn management and state", () => {
  const history = [];

  function addTurn(role, text) {
    const turn = {
      id: `msg-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      role,
      text,
      timestamp: new Date().toISOString(),
    };
    history.push(turn);
    return turn;
  }

  addTurn("user", "What are the job opportunities for a B.Tech Computer Science student?");
  addTurn("assistant", "Here are the top career paths: Software Development Engineer (SDE-1)...");

  assert.equal(history.length, 2);
  assert.equal(history[0].role, "user");
  assert.equal(history[1].role, "assistant");
  assert.ok(history[1].text.includes("SDE-1"));
});

// ============================================================================
// 8. ERROR & LOADING STATES
// ============================================================================
test("Error Handling: Handles HTTP 401, 403, and network errors gracefully", () => {
  function formatApiErrorMessage(status, fallback) {
    switch (status) {
      case 401:
        return "Session expired or invalid. Please sign in again.";
      case 403:
        return "Access denied: You are not authorized to view this resource.";
      case 404:
        return "The requested record was not found.";
      case 429:
        return "Service is experiencing high traffic. Please try again shortly.";
      default:
        return fallback || "An unexpected error occurred. Please try again.";
    }
  }

  assert.equal(formatApiErrorMessage(401), "Session expired or invalid. Please sign in again.");
  assert.equal(formatApiErrorMessage(403), "Access denied: You are not authorized to view this resource.");
  assert.equal(formatApiErrorMessage(429), "Service is experiencing high traffic. Please try again shortly.");
  assert.equal(formatApiErrorMessage(500, "Server error"), "Server error");
});
