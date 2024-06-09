# Polyglot: FastAPI Backend for NLP Data Collection and Annotation Tool

This repository contains a FastAPI-based backend app for data collection and annotation for Natural Language Processing (NLP) projects.

## Features

- **User Management**: Handles user creation, deletion, authentication and authorization.
- **Data Management**: Supports CRUD operations for creating and annotating datasets.
- **Annotation Tools**: Provides endpoints for creating and annotating NLP data for text-to-text or text-to-speech projects.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/polyglot.git
    cd polyglot
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the FastAPI server**:
    ```bash
    uvicorn app.main:app --reload
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## Contact

For questions or feedback, please open an issue or contact [ibrahimnaafi@gmail.com](ibrahimnaafi@gmail.com).
