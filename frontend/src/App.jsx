// src/App.js
import React from "react";
import { ThemeProvider } from "@mui/material/styles";
import theme from "./theme";
import AdminDashboard from "./pages/AdminDashboard";

function App() {
  return (
    <ThemeProvider theme={theme}>
      <AdminDashboard />
    </ThemeProvider>
  );
}

export default App;
