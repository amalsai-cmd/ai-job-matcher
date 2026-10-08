import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Register() {
  const navigate = useNavigate();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            full_name: fullName,
            email: email,
            password: password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Registration failed"
        );
      }

      // Save email temporarily for OTP verification
      localStorage.setItem(
        "otp_email",
        email
      );

      setMessage(
        "OTP sent successfully! Check your email."
      );

      // Go to OTP page
      setTimeout(() => {
        navigate("/verify-otp");
      }, 800);

    } catch (error) {

      setMessage(
        error.message || "Registration failed"
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

        <h1>
          Create Account
        </h1>

        <p className="subtitle">
          Start finding jobs that match your skills.
        </p>

        <form onSubmit={handleRegister}>

          <div className="input-group">

            <label>
              Full Name
            </label>

            <input
              type="text"
              placeholder="Enter your full name"
              value={fullName}
              onChange={(e) =>
                setFullName(e.target.value)
              }
              required
            />

          </div>

          <div className="input-group">

            <label>
              Email
            </label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) =>
                setEmail(e.target.value)
              }
              required
            />

          </div>

          <div className="input-group">

            <label>
              Password
            </label>

            <input
              type="password"
              placeholder="Create a password"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
              required
              minLength={6}
            />

          </div>

          <button
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Sending OTP..."
              : "Create Account"}
          </button>

          {message && (
            <p
              style={{
                textAlign: "center",
                marginTop: "15px",
                color: message.includes("OTP")
                  ? "#22d3ee"
                  : "#f87171",
              }}
            >
              {message}
            </p>
          )}

        </form>

        <p className="register-text">

          Already have an account?{" "}

          <Link to="/login">
            Login
          </Link>

        </p>

      </div>

    </div>
  );
}

export default Register;