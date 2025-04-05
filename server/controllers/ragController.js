const { spawn } = require('child_process');
const path = require('path');

exports.runRagQuery = (req, res) => {
  const userQuery = req.body.query;
  if (!userQuery) {
    return res.status(400).json({ error: 'Query not provided' });
  }

  // Build the path to the Python script
  const scriptPath = path.join(__dirname, '../../python/rag.py');

  // Spawn the Python process without CLI arguments
  const pythonProcess = spawn('python', [scriptPath]);

  // Write the user query to the Python process's stdin
  pythonProcess.stdin.write(userQuery);
  pythonProcess.stdin.end();

  let output = '';
  pythonProcess.stdout.on('data', (data) => {
    output += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python error: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: 'Python process exited with code ' + code });
    }
    res.json({ result: output });
  });
};
