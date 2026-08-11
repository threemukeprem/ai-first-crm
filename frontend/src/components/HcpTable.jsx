function HcpTable({ hcps, onDelete }) {
    return (
      <table width="100%">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Specialty</th>
            <th>Organization</th>
            <th>City</th>
            <th>Actions</th>
          </tr>
        </thead>
  
        <tbody>
          {hcps.map((hcp) => (
            <tr key={hcp.id}>
              <td>{hcp.id}</td>
              <td>{hcp.full_name}</td>
              <td>{hcp.specialty}</td>
              <td>{hcp.organization}</td>
              <td>{hcp.city}</td>
              <td>
                <button
                  onClick={() => onDelete(hcp.id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }
  
  export default HcpTable;