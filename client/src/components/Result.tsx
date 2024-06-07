import { useLocation } from "react-router-dom";
import "../styles/Table.css";

export default function Table() {
    const location = useLocation();
    const state = location.state;

    return (
        <div>
            <h1 className="result-header">Result</h1>
            <div className="table-container">
                <table className="shadowed-table">
                    <thead>
                        <tr>
                            <th>Attribute</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Object.entries(state).map(([key, value], index) => (
                            <tr key={index}>
                                <td>{key.replace(/_/g, " ")}</td>
                                <td>{Array.isArray(value) ? value.join(", ") : value}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
