# IDOR Detector

IDOR Detector is an open-source Python tool designed to detect Insecure Direct Object Reference (IDOR) vulnerabilities in web applications. The tool scans API endpoints and uses multiple detection techniques to identify potential IDOR issues.

## Features

- Scans a list of API endpoints to detect potential IDOR vulnerabilities.
- Supports a plugin system to easily extend the tool with custom detection techniques.
- Comes with pre-built detection techniques, including pattern-based and sequence-based methods.

## Installation

To install the IDOR Detector, simply clone this repository:

```
git clone https://github.com/yourusername/idor_detector.git
cd idor_detector
```

Create a virtual environment to isolate the project dependencies:

```
python3 -m venv venv
source venv/bin/activate # For Linux/macOS
.\venv\Scripts\activate # For Windows
```

Install the required packages:

```
pip install -r requirements.txt
```

## Usage

To use the IDOR Detector, create a Python script and import the `IDORDetector` class:

```python
from idor_detector.detector import IDORDetector
from idor_detector.api_scanner import APIScanner

# Initialize the API scanner
scanner = APIScanner("https://example.com")

# Initialize the IDOR Detector
detector = IDORDetector(scanner)

# Detect IDOR vulnerabilities
results = detector.detect()

# Process the results
# ...
```

Plugins
The IDOR Detector supports a plugin architecture that allows users to add their own detection methods without modifying the core code. To create a plugin:

Create a Python file in the plugins directory.
Implement a class that extends the IDORTechnique interface from the idor_techniques module.
Ensure the class has a detect method and a name attribute.
The IDOR Detector will automatically load and use any plugins placed in the plugins directory.

License
This project is licensed under the MIT License. See the LICENSE file for details.