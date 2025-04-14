// src/pages/AdminDashboard.js
import React, { useState } from "react";
import {
  Container,
  TextField,
  Button,
  Typography,
  Paper,
  Box,
} from "@mui/material";

function AdminDashboard() {
  const [clientId, setClientId] = useState("");
  const [intentPrompt, setIntentPrompt] = useState("");
  const [inferPrompt, setInferPrompt] = useState("");

  const handleSubmit = async () => {
    const response = await fetch("/api/savetemplate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        client_id: clientId,
        intent_prompt: intentPrompt,
        infer_prompt: inferPrompt,
      }),
    });
    const result = await response.json();
    alert(result.message || "Saved");
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Admin Dashboard
        </Typography>
        <TextField
          label="Client ID"
          fullWidth
          margin="normal"
          value={clientId}
          onChange={(e) => setClientId(e.target.value)}
        />
        <TextField
          label="Intent Prompt Template"
          fullWidth
          multiline
          rows={6}
          margin="normal"
          value={intentPrompt}
          onChange={(e) => setIntentPrompt(e.target.value)}
        />
        <TextField
          label="Infer Prompt Template"
          fullWidth
          multiline
          rows={6}
          margin="normal"
          value={inferPrompt}
          onChange={(e) => setInferPrompt(e.target.value)}
        />
        <Box textAlign="center" mt={2}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleSubmit}
            sx={{ px: 4 }}
          >
            Save Templates
          </Button>
        </Box>
      </Paper>
    </Container>
  );
}

export default AdminDashboard;
