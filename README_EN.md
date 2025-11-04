# Minic - Taipei Medical University Neurology Research Database Platform

## Project Overview

Minic is a platform designed to collect and integrate clinical and research data related to neuroscience and neurosurgery. Operated by Taipei Medical University, the platform covers neurology and neurosurgery fields, aggregating clinical cases, research data, imaging files, and multifaceted medical information from three affiliated hospitals within the Taipei Medical University system (TMU Hospital, Wan Fang Hospital, and Shuang Ho Hospital).

## Key Features

- **Database Management**: Integration of multiple neurology research databases
- **Data De-identification**: All data undergoes strict de-identification and thematic classification
- **Research Collaboration**: Promotes resource sharing in neurology research, education, and clinical practice
- **Cross-institutional Cooperation**: Supports interdisciplinary and inter-institutional collaboration for researchers both within and outside the institution

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Processing**: Pandas, NumPy, Matplotlib
- **Database**: CSV file format
- **Deployment**: Docker support

## Project Structure

```
dementiaDB/
├── app/                    # Main application
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS, images)
├── data/                  # Data files
├── scripts/               # Script files
├── tests/                 # Test files
├── docker/                # Docker-related files
├── web_server.py          # Main web server
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Installation and Execution

### Requirements

- Python 3.9+
- pip

### Installation Steps

1. Clone the project
```bash
git clone https://github.com/arbiterski/minic.git
cd minic
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python web_server.py
```

4. Open your browser and visit
```
http://localhost:5001
```

### Docker Deployment

```bash
# Build image
docker build -t minic .

# Run container
docker run -p 5001:5001 minic
```

## Database Contents

### Taiwan Dementia Clinical Database

- **Data Source**: Dementia Center and Neurology Department, Taipei Medical University-Shuang Ho Hospital
- **Assessment Standards**: National Institute on Aging-Alzheimer's Association (NIA-AA)
- **Data Content**: Medical records, neuropsychological assessments (MMSE, CASI, CDR), brain MRI imaging
- **Features**: Machine learning methods for heterogeneity classification, promoting subtype clustering analysis

### Brain Consciousness Database

- **Research Areas**: Brain consciousness states, cognitive functions, and neuroplasticity
- **Data Types**: Multi-modal data including EEG, functional MRI
- **Status**: In planning

## Research Fields

### Neurology
- Alzheimer's Disease and Dementia
- Parkinson's Disease
- Stroke
- Epilepsy
- Multiple Sclerosis

### Neurosurgery
- Brain Tumors
- Cerebrovascular Diseases
- Spinal Diseases
- Traumatic Brain Injury
- Functional Neurosurgery

## Contact Information

- **Platform Management**: arbiter@tmu.edu.tw
- **Phone**: +886-2-2736-1661
- **Address**: No. 250, Wuxing St., Xinyi Dist., Taipei City, Taiwan

## License

This project is licensed under the Creative Commons Attribution 4.0 International License.

## Contribution

We welcome researchers to submit new databases to jointly advance neuroscience research development.

## Reference

The platform design is inspired by [PhysioNet](https://physionet.org/)'s model of open collaboration and data reusability.

---

© 2025 Taipei Medical University Neurology Research Database Platform | Brand: Minic
