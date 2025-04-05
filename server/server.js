// /server/server.js
const express = require('express');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 5004;

// Middleware
app.use(cors());
app.use(express.json());

// Import routes

const uploadRoutes = require('./routes/uploadRoutes');
const emailRoutes = require('./routes/emailRoutes');
const ragRoutes = require('./routes/ragRoutes');

// Mount routes (you can adjust the prefix as needed)
app.use('/api', uploadRoutes);
app.use('/api', emailRoutes);
app.use('/api/rag', ragRoutes);

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
