
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const [selectedFile, setSelectedFile] = useState(null);
  const [apiMessage, setApiMessage] = useState("");
  const [uploadMessage, setUploadMessage] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [uploading, setUploading] = useState(false);

  // Job matching states
  const [jobs, setJobs] = useState([]);
  const [jobsLoading, setJobsLoading] = useState(false);
  const [jobsError, setJobsError] = useState("");

  const [searchKeyword, setSearchKeyword] =
    useState("software developer");

  const [searchLocation, setSearchLocation] =
    useState("India");

  const [minimumMatch, setMinimumMatch] =
    useState(0);

  const loginData = JSON.parse(
    localStorage.getItem("user") || "null"
  );

  const user = loginData?.user || null;

  // ============================================================
  // CHECK LOGIN + BACKEND
  // ============================================================

  useEffect(() => {
    if (!user || !user.id) {
      navigate("/login");
      return;
    }

    fetch("http://127.0.0.1:8000/api/test")
      .then((response) => response.json())
      .then((data) => {
        setApiMessage(data.message);
      })
      .catch((error) => {
        console.error(
          "Backend connection failed:",
          error
        );

        setApiMessage(
          "Backend connection failed"
        );
      });
  }, [navigate]);

  // ============================================================
  // LOAD RECOMMENDED JOBS
  // ============================================================

  const fetchRecommendedJobs = async () => {
    if (!user || !user.id) {
      return;
    }

    setJobsLoading(true);
    setJobsError("");

    try {
      const url =
        "http://127.0.0.1:8000/api/jobs/recommended" +
        `?user_id=${user.id}` +
        `&what=${encodeURIComponent(searchKeyword)}` +
        `&where=${encodeURIComponent(searchLocation)}` +
        "&page=1";

      const response = await fetch(url);

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Failed to load recommended jobs"
        );
      }

      // Store jobs only.
      // Do NOT update analysis here because that
      // can cause an infinite useEffect loop.
      setJobs(data.jobs || []);

    } catch (error) {
      console.error(
        "Job matching failed:",
        error
      );

      setJobsError(
        error.message ||
          "Unable to load recommended jobs."
      );

      setJobs([]);

    } finally {
      setJobsLoading(false);
    }
  };

  // ============================================================
  // CHOOSE RESUME
  // ============================================================

  const handleChooseResume = () => {
    fileInputRef.current.click();
  };

  // ============================================================
  // UPLOAD RESUME
  // ============================================================

  const handleFileChange = async (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    if (file.type !== "application/pdf") {
      setUploadMessage(
        "Please select a PDF file."
      );
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setUploadMessage(
        "File size must be less than 5MB."
      );
      return;
    }

    setSelectedFile(file);

    setUploadMessage(
      "Uploading and analyzing your resume..."
    );

    setAnalysis(null);
    setJobs([]);
    setJobsError("");

    setUploading(true);

    const formData = new FormData();

    formData.append("file", file);

    formData.append(
      "user_id",
      String(user.id)
    );

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/resume/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            `Upload failed (${response.status})`
        );
      }

      setUploadMessage(
        data.message ||
          "Resume uploaded and analyzed successfully!"
      );

      if (data.analysis) {
        setAnalysis(data.analysis);

        // Fetch recommended jobs once,
        // after the resume has been analyzed.
        await fetchRecommendedJobs();
      }

    } catch (error) {
      console.error(
        "Resume upload failed:",
        error
      );

      setUploadMessage(
        error.message ||
          "Resume upload failed."
      );

    } finally {
      setUploading(false);
    }
  };

  // ============================================================
  // LOGOUT
  // ============================================================

  const handleLogout = () => {
    localStorage.removeItem("user");

    navigate("/login");
  };

  // ============================================================
  // FILTER JOBS
  // ============================================================

  const filteredJobs = jobs.filter(
    (job) =>
      Number(job.match_percentage || 0) >=
      Number(minimumMatch)
  );

  // ============================================================
  // MATCH COLOR
  // ============================================================

  const getMatchClass = (percentage) => {
    if (percentage >= 80) {
      return "match-excellent";
    }

    if (percentage >= 60) {
      return "match-good";
    }

    if (percentage >= 40) {
      return "match-average";
    }

    return "match-low";
  };

  // ============================================================
  // DASHBOARD
  // ============================================================

  return (
    <div className="dashboard-page">

      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside className="sidebar">

        <div className="sidebar-logo">
          AI<span>JOB</span>MATCHER
        </div>

        <nav className="sidebar-nav">

          <a
            href="#"
            className="nav-item active"
            onClick={(e) =>
              e.preventDefault()
            }
          >
            Dashboard
          </a>

          <a
            href="#"
            className="nav-item"
            onClick={(e) =>
              e.preventDefault()
            }
          >
            Resume
          </a>

          <a
            href="#"
            className="nav-item"
            onClick={(e) =>
              e.preventDefault()
            }
          >
            Job Matcher
          </a>

          <a
            href="#"
            className="nav-item"
            onClick={(e) =>
              e.preventDefault()
            }
          >
            History
          </a>

          <a
            href="#"
            className="nav-item"
            onClick={(e) =>
              e.preventDefault()
            }
          >
            Profile
          </a>

        </nav>

        <div className="sidebar-bottom">

          <button
            className="nav-item"
            onClick={handleLogout}
            style={{
              width: "100%",
              background: "transparent",
              border: "none",
              textAlign: "left",
              cursor: "pointer",
              color: "#94a3b8",
              fontWeight: "normal",
            }}
          >
            Logout
          </button>

        </div>

      </aside>


      {/* ======================================================
          MAIN CONTENT
      ====================================================== */}

      <main className="dashboard-content">

        {/* HEADER */}

        <header className="dashboard-header">

          <div>

            <h1>
              Dashboard
            </h1>

            <p>
              Welcome back! Let's find your
              next opportunity.
            </p>

            {apiMessage && (
              <p className="api-status">
                🟢 {apiMessage}
              </p>
            )}

          </div>


          <div className="user-avatar">

            {user?.full_name
              ? user.full_name
                  .split(" ")
                  .map((name) =>
                    name[0]
                  )
                  .join("")
                  .slice(0, 2)
                  .toUpperCase()
              : "AS"}

          </div>

        </header>


        {/* ====================================================
            STATS
        ==================================================== */}

        <section className="stats-grid">

          <div className="stat-card">

            <span className="stat-title">
              Resume Status
            </span>

            <h2>
              {analysis
                ? "Analyzed"
                : selectedFile
                ? "Uploaded"
                : "Not Uploaded"}
            </h2>

            <span className="stat-subtitle">

              {analysis
                ? "Resume analyzed successfully"
                : selectedFile
                ? "Resume selected successfully"
                : "Upload your resume to begin"}

            </span>

          </div>


          <div className="stat-card">

            <span className="stat-title">
              Jobs Matched
            </span>

            <h2>
              {filteredJobs.length}
            </h2>

            <span className="stat-subtitle">

              {jobsLoading
                ? "Finding jobs..."
                : "Jobs matching your resume"}

            </span>

          </div>


          <div className="stat-card">

            <span className="stat-title">
              Applications
            </span>

            <h2>
              0
            </h2>

            <span className="stat-subtitle">
              Track your applications
            </span>

          </div>

        </section>


        {/* ====================================================
            RESUME UPLOAD
        ==================================================== */}

        <section className="dashboard-card">

          <div className="section-header">

            <div>

              <h2>
                Upload Your Resume
              </h2>

              <p>
                Upload your PDF resume to
                analyze your skills.
              </p>

            </div>

          </div>


          <div className="upload-box">

            <div className="upload-icon">
              📄
            </div>

            <h3>
              Upload your resume
            </h3>

            <p>
              PDF files only · Maximum 5MB
            </p>


            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              style={{
                display: "none",
              }}
              onChange={handleFileChange}
            />


            <button
              type="button"
              className="upload-button"
              onClick={handleChooseResume}
              disabled={uploading}
            >
              {uploading
                ? "Analyzing..."
                : "Choose Resume"}
            </button>


            {selectedFile && (
              <div className="selected-file">

                📄 {selectedFile.name}

              </div>
            )}


            {uploadMessage && (
              <p className="api-status">

                {uploadMessage}

              </p>
            )}

          </div>

        </section>


        {/* ====================================================
            RESUME ANALYSIS
        ==================================================== */}

        {analysis && (
          <section className="dashboard-card">

            <div className="section-header">

              <h2>
                Resume Analysis
              </h2>

              <p>
                Information extracted from
                your resume.
              </p>

            </div>


            {analysis.name && (
              <div className="selected-file">

                <strong>
                  Name:
                </strong>{" "}

                {analysis.name}

              </div>
            )}


            {analysis.email && (
              <div className="selected-file">

                <strong>
                  Email:
                </strong>{" "}

                {analysis.email}

              </div>
            )}


            {analysis.phone && (
              <div className="selected-file">

                <strong>
                  Phone:
                </strong>{" "}

                {analysis.phone}

              </div>
            )}


            {analysis.skills && (
              <div className="selected-file">

                <strong>
                  Skills:
                </strong>{" "}

                {Array.isArray(
                  analysis.skills
                )
                  ? analysis.skills.join(", ")
                  : analysis.skills}

              </div>
            )}


            {analysis.education && (
              <div className="selected-file">

                <strong>
                  Education:
                </strong>{" "}

                {Array.isArray(
                  analysis.education
                )
                  ? analysis.education.join(", ")
                  : analysis.education}

              </div>
            )}


            {analysis.experience && (
              <div className="selected-file">

                <strong>
                  Experience:
                </strong>{" "}

                {Array.isArray(
                  analysis.experience
                )
                  ? analysis.experience.join(", ")
                  : analysis.experience}

              </div>
            )}

          </section>
        )}


        {/* ====================================================
            JOB SEARCH
        ==================================================== */}

        <section className="dashboard-card">

          <div className="section-header">

            <div>

              <h2>
                Find Matching Jobs
              </h2>

              <p>
                Search real-time jobs and
                compare them with your resume.
              </p>

            </div>

          </div>


          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "1fr 1fr 180px 140px",
              gap: "12px",
              marginTop: "20px",
            }}
          >

            <input
              type="text"
              value={searchKeyword}
              onChange={(e) =>
                setSearchKeyword(
                  e.target.value
                )
              }
              placeholder="Job title or keyword"
              style={{
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid #334155",
                background: "#0f172a",
                color: "#fff",
              }}
            />


            <input
              type="text"
              value={searchLocation}
              onChange={(e) =>
                setSearchLocation(
                  e.target.value
                )
              }
              placeholder="Location"
              style={{
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid #334155",
                background: "#0f172a",
                color: "#fff",
              }}
            />


            <select
              value={minimumMatch}
              onChange={(e) =>
                setMinimumMatch(
                  Number(e.target.value)
                )
              }
              style={{
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid #334155",
                background: "#0f172a",
                color: "#fff",
              }}
            >

              <option value={0}>
                All Matches
              </option>

              <option value={40}>
                40%+
              </option>

              <option value={60}>
                60%+
              </option>

              <option value={70}>
                70%+
              </option>

              <option value={80}>
                80%+
              </option>

              <option value={90}>
                90%+
              </option>

            </select>


            <button
              type="button"
              className="upload-button"
              onClick={fetchRecommendedJobs}
              disabled={
                jobsLoading || !analysis
              }
            >

              {jobsLoading
                ? "Searching..."
                : "Search Jobs"}

            </button>

          </div>


          {!analysis && (
            <p
              style={{
                marginTop: "15px",
                color: "#94a3b8",
              }}
            >
              Upload your resume first to
              start matching jobs.
            </p>
          )}

        </section>


        {/* ====================================================
            RECENT JOB MATCHES
        ==================================================== */}

        <section className="dashboard-card">

          <div className="section-header">

            <div>

              <h2>
                Recent Job Matches
              </h2>

              <p>
                Your latest AI-powered job
                recommendations.
              </p>

            </div>

            {jobs.length > 0 && (
              <span
                style={{
                  color: "#94a3b8",
                  fontSize: "13px",
                }}
              >
                Powered by Adzuna
              </span>
            )}

          </div>


          {/* JOB ERROR */}

          {jobsError && (
            <div
              style={{
                background: "#450a0a",
                border: "1px solid #991b1b",
                padding: "15px",
                borderRadius: "10px",
                marginTop: "20px",
                color: "#fecaca",
              }}
            >

              {jobsError}

            </div>
          )}


          {/* JOB LOADING */}

          {jobsLoading && (
            <div className="empty-state">

              <div className="empty-icon">
                🔄
              </div>

              <h3>
                Finding matching jobs...
              </h3>

              <p>
                We're comparing your resume
                with real-time job listings.
              </p>

            </div>
          )}


          {/* NO JOBS */}

          {!jobsLoading &&
            !jobsError &&
            filteredJobs.length === 0 && (

              <div className="empty-state">

                <div className="empty-icon">
                  🔍
                </div>

                <h3>
                  {analysis
                    ? "No job matches found"
                    : "No job matches yet"}
                </h3>

                <p>
                  {analysis
                    ? "Try another job title or location."
                    : "Upload your resume to start discovering matching jobs."}
                </p>

              </div>

            )}


          {/* JOB CARDS */}

          {!jobsLoading &&
            !jobsError &&
            filteredJobs.length > 0 && (

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns:
                    "repeat(auto-fit, minmax(320px, 1fr))",
                  gap: "20px",
                  marginTop: "20px",
                }}
              >

                {filteredJobs.map(
                  (job, index) => (

                    <div
                      key={
                        job.id || index
                      }
                      style={{
                        background: "#0f172a",
                        border: "1px solid #334155",
                        borderRadius: "14px",
                        padding: "20px",
                      }}
                    >

                      {/* JOB HEADER */}

                      <div
                        style={{
                          display: "flex",
                          justifyContent:
                            "space-between",
                          gap: "15px",
                        }}
                      >

                        <div>

                          <h3
                            style={{
                              margin:
                                "0 0 7px 0",
                            }}
                          >
                            {job.title}
                          </h3>

                          <p
                            style={{
                              margin: 0,
                              color: "#94a3b8",
                            }}
                          >
                            {job.company ||
                              "Company not specified"}
                          </p>

                        </div>


                        {/* MATCH */}

                        <div
                          className={getMatchClass(
                            Number(
                              job.match_percentage
                            )
                          )}
                          style={{
                            minWidth: "65px",
                            height: "65px",
                            borderRadius: "50%",
                            display: "flex",
                            flexDirection:
                              "column",
                            justifyContent:
                              "center",
                            alignItems:
                              "center",
                            border:
                              "3px solid currentColor",
                          }}
                        >

                          <strong>
                            {job.match_percentage}%
                          </strong>

                          <small>
                            Match
                          </small>

                        </div>

                      </div>


                      {/* LOCATION */}

                      <p
                        style={{
                          color: "#cbd5e1",
                          fontSize: "13px",
                          marginTop: "15px",
                        }}
                      >
                        📍{" "}
                        {job.location ||
                          "Location not specified"}
                      </p>


                      {/* DESCRIPTION */}

                      <p
                        style={{
                          color: "#94a3b8",
                          fontSize: "13px",
                          lineHeight: "1.6",
                        }}
                      >
                        {job.description
                          ? job.description
                              .replace(
                                /<[^>]*>/g,
                                ""
                              )
                              .substring(
                                0,
                                220
                              ) + "..."
                          : "No description available."}
                      </p>


                      {/* MATCHED SKILLS */}

                      {job.matched_skills &&
                        job.matched_skills
                          .length > 0 && (

                          <div
                            style={{
                              marginTop:
                                "15px",
                            }}
                          >

                            <h4
                              style={{
                                fontSize:
                                  "13px",
                                marginBottom:
                                  "8px",
                                color:
                                  "#4ade80",
                              }}
                            >
                              ✓ Skills You Have
                            </h4>


                            <div
                              style={{
                                display:
                                  "flex",
                                flexWrap:
                                  "wrap",
                                gap: "6px",
                              }}
                            >

                              {job.matched_skills.map(
                                (
                                  skill,
                                  skillIndex
                                ) => (

                                  <span
                                    key={
                                      skillIndex
                                    }
                                    style={{
                                      background:
                                        "#14532d",
                                      color:
                                        "#bbf7d0",
                                      padding:
                                        "5px 9px",
                                      borderRadius:
                                        "15px",
                                      fontSize:
                                        "11px",
                                    }}
                                  >
                                    {skill}
                                  </span>

                                )
                              )}

                            </div>

                          </div>

                        )}


                      {/* MISSING SKILLS */}

                      {job.missing_skills &&
                        job.missing_skills
                          .length > 0 && (

                          <div
                            style={{
                              marginTop:
                                "15px",
                            }}
                          >

                            <h4
                              style={{
                                fontSize:
                                  "13px",
                                marginBottom:
                                  "8px",
                                color:
                                  "#fbbf24",
                              }}
                            >
                              ⚠ Skills To Learn
                            </h4>


                            <div
                              style={{
                                display:
                                  "flex",
                                flexWrap:
                                  "wrap",
                                gap: "6px",
                              }}
                            >

                              {job.missing_skills
                                .slice(
                                  0,
                                  6
                                )
                                .map(
                                  (
                                    skill,
                                    skillIndex
                                  ) => (

                                    <span
                                      key={
                                        skillIndex
                                      }
                                      style={{
                                        background:
                                          "#451a03",
                                        color:
                                          "#fed7aa",
                                        padding:
                                          "5px 9px",
                                        borderRadius:
                                          "15px",
                                        fontSize:
                                          "11px",
                                      }}
                                    >
                                      {skill}
                                    </span>

                                  )
                                )}

                            </div>

                          </div>

                        )}


                      {/* FOOTER */}

                      <div
                        style={{
                          display:
                            "flex",
                          justifyContent:
                            "space-between",
                          alignItems:
                            "center",
                          marginTop:
                            "20px",
                          paddingTop:
                            "15px",
                          borderTop:
                            "1px solid #334155",
                        }}
                      >

                        <span
                          style={{
                            color:
                              "#64748b",
                            fontSize:
                              "11px",
                          }}
                        >
                          Real-time job
                        </span>


                        {job.job_url && (

                          <a
                            href={
                              job.job_url
                            }
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                              background:
                                "#22c55e",
                              color:
                                "#052e16",
                              textDecoration:
                                "none",
                              padding:
                                "9px 14px",
                              borderRadius:
                                "7px",
                              fontWeight:
                                "bold",
                              fontSize:
                                "12px",
                            }}
                          >
                            Apply Now →
                          </a>

                        )}

                      </div>

                    </div>

                  )
                )}

              </div>

            )}

        </section>

      </main>

    </div>
  );
}

export default Dashboard;
