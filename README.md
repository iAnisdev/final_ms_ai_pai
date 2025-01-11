# Final MS AI Project: Programming for AI

This repository contains the code and documentation for the **Final MS AI Project** (Programming for AI). The project showcases collaborative work among group members, each contributing their individual components to achieve the project's objectives.

## Repository Clone

Clone this repository to your local system using the following command:

```bash
git clone https://github.com/iAnisdev/final_ms_ai_pai.git
```

## Repository Structure

The repository is organized into the following structure:

```
final_ms_ai_pai/
├── <RollNumber1>/    # Work directory for member 1
├── <RollNumber2>/    # Work directory for member 2
├── <RollNumber3>/    # Work directory for member 3
├── shared/           # Shared components 
└── README.md         # Project README
```

Each group member must work within their assigned directory named after their **roll number**.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- [Git](https://git-scm.com/)
- Python 3.8 or later

### Tech Stack
- Python
- PostgreSQL
- pip

### Libraries and 3rd Party Tools
- [Pandas](https://pandas.pydata.org/)
- [Numpy](https://numpy.org/)
- [Scikit-learn](https://scikit-learn.org/)
- [Shiny](https://shiny.rstudio.com/)
- [Binance API](https:binance.com)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/iAnisdev/final_ms_ai_pai.git
   ```
2. Navigate to your directory:
   ```bash
   cd final_ms_ai_pai
   ```
3. Install required dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```
4. Update Environment Variables and add binance API key in `.env` file:
   ```bash
   cp .env.example .env
   ```
5. Make sure postgresql is installed and running on your system.
6. [Setup](DATABASE.md) a database named `crypto_analysis` in postgresql and update the database credentials in `.env` file.
7. Run the following command to run shiny app locally:
   ```bash
   shiny run --reload --launch-browser
   ```
   or 
   ```bash
   make run
   ```
   Project will be running on ` http://127.0.0.1:8000/`

## Contribution Guidelines

1. Document your code thoroughly to help other group members understand your contributions.
3. Maintain consistency in coding style and adhere to best practices.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Happy coding! 🚀
