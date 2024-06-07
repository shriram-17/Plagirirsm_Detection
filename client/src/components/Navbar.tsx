import { Link } from "react-router-dom";
import "../styles/Navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <h1 className="title">IR Package</h1>
      <ul className="nav-links">
        <li className="nav-link font-mono">
          <Link to="/form">Form</Link>
        </li>
        <li className="nav-link">
          <Link to="/find">Find</Link>
        </li>
      </ul>
    </nav>
  );
}
