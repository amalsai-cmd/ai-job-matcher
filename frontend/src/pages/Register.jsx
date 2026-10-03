import { Link } from "react-router-dom";

function Register() {
  return (
    <div className="login-page">
      <div className="login-card">

        <div className="logo">
          AI<span>JOB</span>MATCHER
        </div>

        <h1>Create Account</h1>

        <p className="subtitle">
          Start finding jobs that match your skills.
        </p>

        <form>
          <div className="input-group">
            <label>Full Name</label>

            <input
              type="text"
              placeholder="Enter your full name"
            />
          </div>

          <div className="input-group">
            <label>Email</label>

            <input
              type="email"
              placeholder="Enter your email"
            />
          </div>

          <div className="input-group">
            <label>Password</label>

            <input
              type="password"
              placeholder="Create a password"
            />
          </div>

          <div className="input-group">
            <label>Confirm Password</label>

            <input
              type="password"
              placeholder="Confirm your password"
            />
          </div>

          <button type="submit">
            Create Account
          </button>
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