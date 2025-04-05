// /server/routes/emailRoutes.js

const express = require('express');
const router = express.Router();
const path = require('path');
const { spawn } = require('child_process');

router.post('/send-emails', (req, res) => {
  console.log("Received a request to trigger email sending.");
  
  // Construct the absolute path to the Python script.
  const path = require('path');
  const pythonScriptPath = path.join(__dirname, '..', '..', 'python', 'send_emails.py');
  console.log("Using Python script path:", pythonScriptPath);


  const pythonProcess = spawn('python', [pythonScriptPath]);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('error', (error) => {
    console.error('Failed to start Python process:', error);
    res.status(500).json({ message: 'Failed to send.' });
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
    if (code === 0) {
      res.json({ message: 'Email sent!' });
    } else {
      res.status(500).json({ message: 'Failed to trigger email sending.' });
    }
  });
});

module.exports = router;
