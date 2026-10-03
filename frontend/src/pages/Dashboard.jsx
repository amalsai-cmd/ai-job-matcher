import { useEffect, useRef, useState } from "react";

function Dashboard() {
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [apiMessage, setApiMessage] = useState("");

  // Connect to FastAPI when Dashboard loads
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/test")
      .then((response) => response.json())
      .then((data) => {
        setApiMessage(data.message);
      })
      .catch((error) => {
        console.error("Backend connection failed:", error);
      });
  }, []);

  // Open file picker
  const handleChooseResume = () => {
    fileInputRef.current.click();
  };

  // Handle selected PDF
  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      setSelectedFile(file);
    }
  };

  return (
    <div className="dashboard-page">

      {/* Sidebar */}
      <aside className="sidebar">

        <div className="sidebar-logo">
          AI<span>JOB</span>MATCHER
        </div>

        <nav className="sidebar-nav">

          <a href="#" className="nav-item active">
            Dashboard
          </a>

          <a href="#" className="nav-item">
            Resume
          </a>

          <a href="#" className="nav-item">
            Job Matcher
          </a>

          <a href="#" className="nav-item">
            History
          </a>

          <a href="#" className="nav-item">
            Profile
          </a>

        </nav>

        <div className="sidebar-bottom">
          <a href="/login" className="nav-item">
            Logout
          </a>
        </div>

      </aside>


      {/* Main Content */}
      <main className="dashboard-content">

        {/* Header */}
        <header className="dashboard-header">

          <div>

            <h1>
              Dashboard
            </h1>

            <p>
              Welcome back! Let's find your next opportunity.
            </p>

            {/* Backend Connection Status */}
            {apiMessage && (
              <p className="api-status">
                🟢 {apiMessage}
              </p>
            )}

          </div>

          <div className="user-avatar">
            AS
          </div>

        </header>


        {/* Statistics */}
        <section className="stats-grid">

          {/* Resume Status */}
          <div className="stat-card">

            <span className="stat-title">
              Resume Status
            </span>

            <h2>
              {selectedFile ? "Uploaded" : "Not Uploaded"}
            </h2>

            <span className="stat-subtitle">
              {selectedFile
                ? "Resume selected successfully"
                : "Upload your resume to begin"}
            </span>

          </div>


          {/* Jobs Matched */}
          <div className="stat-card">

            <span className="stat-title">
              Jobs Matched
            </span>

            <h2>
              0
            </h2>

            <span className="stat-subtitle">
              Start matching jobs
            </span>

          </div>


          {/* Applications */}
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


        {/* Resume Upload */}
        <section className="dashboard-card">

          <div className="section-header">

            <div>

              <h2>
                Upload Your Resume
              </h2>

              <p>
                Upload your PDF resume to analyze your skills.
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


            {/* Hidden File Input */}
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              style={{ display: "none" }}
              onChange={handleFileChange}
            />


            {/* Choose Resume */}
            <button
              className="upload-button"
              onClick={handleChooseResume}
            >
              Choose Resume
            </button>


            {/* Selected File */}
            {selectedFile && (
              <div className="selected-file">
                📄 {selectedFile.name}
              </div>
            )}

          </div>

        </section>


        {/* Recent Job Matches */}
        <section className="dashboard-card">

          <div className="section-header">

            <div>

              <h2>
                Recent Job Matches
              </h2>

              <p>
                Your latest AI-powered job recommendations.
              </p>

            </div>

          </div>


          <div className="empty-state">

            <div className="empty-icon">
              🔍
            </div>

            <h3>
              No job matches yet
            </h3>

            <p>
              Upload your resume to start discovering
              matching jobs.
            </p>

          </div>

        </section>

      </main>

    </div>
  );
}

export default Dashboard;