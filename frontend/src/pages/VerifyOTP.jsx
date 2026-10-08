import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function VerifyOTP() {
  const navigate = useNavigate();

  const [otp, setOtp] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const email = localStorage.getItem("otp_email");

  const handleVerify = async (e) => {
    e.preventDefault();

    if (!email) {
      setMessage(
        "Registration session expired. Please register again."
      );
      return;
    }

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/verify-otp",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email,
            otp: otp,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "OTP verification failed"
        );
      }

      setMessage(
        "Email verified successfully! Redirecting to login..."
      );

      localStorage.removeItem("otp_email");

      setTimeout(() => {
        navigate("/login");
      }, 1500);
    } catch (error) {
      setMessage(
        error.message || "OTP verification failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">

        <div className="logo">
          AI<span>JOB</span>MATCHER
        </div>

        <h1>Verify Your Email</h1>

        <p className="subtitle">
          Enter the 6-digit OTP sent to
        </p>

        <p
          style={{
            textAlign: "center",
            marginBottom: "25px",
            color: "#22d3ee",
            wordBreak: "break-word",
          }}
        >
          {email || "your email"}
        </p>

        <form onSubmit={handleVerify}>

          <div className="input-group">

            <label>Verification Code</label>

            <input
              type="text"
              inputMode="numeric"
              maxLength={6}
              placeholder="Enter 6-digit OTP"
              value={otp}
              onChange={(e) =>
                setOtp(
                  e.target.value.replace(/\D/g, "")
                )
              }
              required
            />

          </div>

          <button
            type="submit"
            disabled={loading || otp.length !== 6}
          >
            {loading ? "Verifying..." : "Verify OTP"}
          </button>

          {message && (
            <p
              style={{
                textAlign: "center",
                marginTop: "15px",
                color: message.includes("successfully")
                  ? "#22d3ee"
                  : "#f87171",
              }}
            >
              {message}
            </p>
          )}

        </form>

        <p className="register-text">
          Already verified?{" "}
          <Link to="/login">
            Login
          </Link>
        </p>

      </div>
    </div>
  );
}

export default VerifyOTP;