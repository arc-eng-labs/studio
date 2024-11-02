# Arcane Studio

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-3.2%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Arcane Studio is a collection of productivity-boosting tools built on top of the [Arcane Engine](https://arcane.engineer/engine). The engine takes natural language instructions (Tasks) and executes them on the users' behalf using its capabilities, which include reading, writing, and editing code and interacting with issues, tickets, wikis, etc., via integrations.

## 🛠️ Tech Stack
- **Backend**: Python and Django
- **Frontend**: Django templates, BulmaCSS, and jQuery

## 🐳 Quickstart with Docker
You can use Docker to run the project locally. Make sure you have Docker installed on your machine.

```shell
git clone https://github.com/arc-eng/studio.git
cd studio
docker-compose up --build
```

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8+

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/arc-eng/studio.git
   ```
2. Navigate to the project directory:
   ```sh
   cd studio
   ```
3. Install the dependencies:
   ```sh
   poetry install
   ```
4. Apply migrations:
   ```sh
   python manage.py migrate
   ```
5. Run the development server:
   ```sh
   python manage.py runserver
   ```

## 🤝 Contributing
Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📧 Contact
For any inquiries, please contact us at [support@arcane.engineer](mailto:support@arcane.engineer).
