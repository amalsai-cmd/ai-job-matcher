import { Link } from "react-router-dom";

function Login() {
  return (
    <div className="login-page">
      <div className="login-card">

        <div className="logo">
          AI<span>JOB</span>MATCHER
        </div>

        <h1>Welcome Back</h1>

        <p className="subtitle">
          Find jobs that match your skills.
        </p>

        <form>
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
              placeholder="Enter your password"
            />
          </div>

          <div className="forgot">
            <a href="#">Forgot password?</a>
          </div>

          <button type="submit">
            Login
          </button>
        </form>

        <p className="register-text">
          Don't have an account?{" "}
          <Link to="/register">
            Register
          </Link>
        </p>

      </div>
    </div>
  );
}

export default Login;