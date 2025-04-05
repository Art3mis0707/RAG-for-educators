// /server/routes/uploadRoutes.js
const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

// Ensure the uploads folder exists
const uploadDir = path.join(__dirname, '..', 'uploads');
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
  console.log("Created uploads folder at:", uploadDir);
}

// Configure Multer storage to save files to the uploads folder
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    console.log("Saving file to:", uploadDir);
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    // Use the original filename (you can modify to ensure uniqueness)
    cb(null, file.originalname);
  }
});
const upload = multer({ storage });

// POST endpoint to handle document upload
router.post('/upload-document', upload.single('docfile'), (req, res) => {
  if (!req.file) {
    console.error("No file received in the request.");
    return res.status(400).json({ message: "No file uploaded" });
  }
  
  console.log("File received:", req.file);
  const filePath = req.file.path;
  console.log("Uploaded file saved at:", filePath);
  
  // Build the absolute path to the Python script.
  // Our structure: server and python are siblings, so we use ../../python/ocr.py
  const pythonScriptPath = path.join(__dirname, '..', '..', 'python', 'ocr.py');
  console.log("Using Python script:", pythonScriptPath);
  
  // Spawn the Python process and pass the uploaded file path as an argument
  const pythonProcess = spawn('python', [pythonScriptPath, filePath]);
  
  let resultData = "";
  
  pythonProcess.stdout.on('data', (data) => {
    resultData += data.toString();
  });
  
  pythonProcess.stderr.on('data', (data) => {
    console.error("Python stderr:", data.toString());
  });
  
  pythonProcess.on('error', (error) => {
    console.error("Python process error:", error);
    res.status(500).json({ message: "Failed to run Python script" });
  });
  
  pythonProcess.on('close', (code) => {
    console.log("Python process exited with code:", code);
    if (code === 0) {
      // Return the result from the Python script to the client.
      res.json({ result: resultData });
    } else {
      res.status(500).json({ message: "Python script failed" });
    }
  });
});

module.exports = router;
