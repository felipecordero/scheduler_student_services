# Scheduler Student Services

**Scheduler Student Services** is a web-based application developed using [Streamlit](https://streamlit.io/), [Google Cloud Firestore](https://firebase.google.com/docs/firestore), and [Pandas](https://pandas.pydata.org/). It is designed to streamline the process for volunteer students to register their availability for the Welcome Team during the start of each academic semester.&#8203;:contentReference[oaicite:0]{index=0}

## Features

- **Volunteer Availability Registration**: :contentReference[oaicite:1]{index=1}
- **Real-Time Data Storage**: :contentReference[oaicite:2]{index=2}
- **Data Analysis**: :contentReference[oaicite:3]{index=3}
- **User-Friendly Interface**: :contentReference[oaicite:4]{index=4}&#8203;:contentReference[oaicite:5]{index=5}

## Architecture Overview

- **Frontend**: :contentReference[oaicite:6]{index=6}
- **Backend**: :contentReference[oaicite:7]{index=7}
- **Data Processing**: :contentReference[oaicite:8]{index=8}&#8203;:contentReference[oaicite:9]{index=9}

## Installation

To run the application locally:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/felipecordero/scheduler_student_services.git
   cd scheduler_student_services
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Firestore Credentials**:

   - :contentReference[oaicite:10]{index=10}
   - :contentReference[oaicite:11]{index=11}
   - :contentReference[oaicite:12]{index=12}&#8203;:contentReference[oaicite:13]{index=13}

     ```toml
     [firebase]
     type = "service_account"
     project_id = "your-project-id"
     private_key_id = "your-private-key-id"
     private_key = "your-private-key"
     client_email = "your-client-email"
     client_id = "your-client-id"
     auth_uri = "https://accounts.google.com/o/oauth2/auth"
     token_uri = "https://oauth2.googleapis.com/token"
     auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
     client_x509_cert_url = "your-client-x509-cert-url"
     ```

   - :contentReference[oaicite:14]{index=14}&#8203;:contentReference[oaicite:15]{index=15}

5. **Run the Application**:

   ```bash
   streamlit run app.py
   ```

   Access the application at `http://localhost:8501` in your web browser.

## Usage

- **Volunteers**:
  - :contentReference[oaicite:16]{index=16}
  - :contentReference[oaicite:17]{index=17}
  - :contentReference[oaicite:18]{index=18}
  - :contentReference[oaicite:19]{index=19}&#8203;:contentReference[oaicite:20]{index=20}

- **Administrators**:
  - :contentReference[oaicite:21]{index=21}
  - :contentReference[oaicite:22]{index=22}
  - :contentReference[oaicite:23]{index=23}&#8203;:contentReference[oaicite:24]{index=24}

## Deployment

:contentReference[oaicite:25]{index=25}&#8203;:contentReference[oaicite:26]{index=26}

1. **Push the Repository to GitHub**:

   Ensure your latest code is committed and pushed to a GitHub repository.

2. **Set Up Streamlit Cloud**:

   - :contentReference[oaicite:27]{index=27}
   - :contentReference[oaicite:28]{index=28}
   - :contentReference[oaicite:29]{index=29}&#8203;:contentReference[oaicite:30]{index=30}

3. **Configure Secrets**:

   - :contentReference[oaicite:31]{index=31}
   - :contentReference[oaicite:32]{index=32}&#8203;:contentReference[oaicite:33]{index=33}

4. **Deploy**:

   Click "Deploy" to launch your application.

## Contributing

:contentReference[oaicite:34]{index=34}&#8203;:contentReference[oaicite:35]{index=35}

1. **Fork the Repository**:

   Click on "Fork" at the top right of the repository page.

2. **Create a New Branch**:

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Make Your Changes**:

   Implement your feature or fix.

4. **Commit and Push**:

   ```bash
   git commit -m "Add your message here"
   git push origin feature/YourFeatureName
   ```

5. **Submit a Pull Request**:

   Open a pull request to the main repository's `main` branch.

## License

:contentReference[oaicite:36]{index=36}&#8203;:contentReference[oaicite:37]{index=37}

## Acknowledgments

:contentReference[oaicite:38]{index=38}&#8203;:contentReference[oaicite:39]{index=39}
