# Website Builder

An AI-powered website builder using CrewAI that creates complete websites with multiple specialized agents working together. This tool leverages the power of AI to generate professional websites based on your requirements, powered by Google's Gemini API for advanced AI capabilities.

## 🌟 Features

- 🤖 Automated website creation using AI agents
- 👥 Specialized agents for research, HTML, CSS, and JavaScript
- ⚙️ Configuration-based agent and task management
- 🛡️ Robust error handling and validation
- 📁 File management utilities
- 📝 Type-safe codebase
- 🔄 Training and replay capabilities
- 🧪 Comprehensive testing suite
- 🤖 Powered by Google Gemini API for advanced AI capabilities

## 📋 Prerequisites

- Python 3.8 or higher
- Serper API key (for web search capabilities)
- Google Gemini API key

## 🚀 Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/website_builder.git
cd website_builder
```

2. **Set up your environment:**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate
```

3. **Install the package:**
```bash
# For basic usage
pip install -e .

# For development
pip install -e ".[dev]"
```

4. **Configure your environment:**
Create a `.env` file in the project root with your API keys:
```env
MODEL=gemini/gemini-1.5-pro-latest
GOOGLE_GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
```

## 🔑 Setting up Google Gemini API

1. **Create a Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gemini API for your project

2. **Get Your API Key:**
   - In the Google Cloud Console, go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy your API key and add it to your `.env` file

3. **Set Up Billing:**
   - Go to "Billing" in the Google Cloud Console
   - Link your project to a billing account
   - Note: Gemini API has a free tier with generous limits

4. **Security Best Practices:**
   - Restrict your API key to specific IP addresses
   - Set up API key quotas
   - Never commit your API key to version control

## 💻 Usage

### Basic Website Creation
```bash
# Create a new website
python -m website_builder.main run "Your Website Topic"
```

### Advanced Features

1. **Train the Crew:**
```bash
python -m website_builder.main train 10 training_session.json "Your Website Topic"
```

2. **Replay a Task:**
```bash
python -m website_builder.main replay "task_id"
```

3. **Test the Crew:**
```bash
python -m website_builder.main test 5 "gpt-4" "Your Website Topic"
```

## 🏗️ Project Structure

```
website_builder/
├── src/
│   └── website_builder/
│       ├── config/          # Configuration files
│       ├── utils/           # Utility functions
│       ├── tools/           # Custom tools
│       ├── main.py          # Main entry point
│       └── crew.py          # CrewAI implementation
├── tests/                   # Test suite
├── knowledge/              # Knowledge base
├── output/                 # Generated websites
└── db/                     # Database files
```

## 🛠️ Development

### Code Quality Tools

```bash
# Format code
black .
isort .

# Type checking
mypy .

# Linting
flake8

# Run tests
pytest
```

## ❓ Frequently Asked Questions

### Q: What is CrewAI and how does it work in this project?
A: CrewAI is a framework that allows multiple AI agents to work together. In this project, we use specialized agents for different aspects of website creation (research, design, coding) that collaborate to build complete websites.

### Q: What kind of websites can this builder create?
A: The builder can create various types of websites including:
- Business websites
- Portfolio sites
- Landing pages
- Blog websites
- E-commerce sites (basic structure)

### Q: Do I need to know coding to use this tool?
A: No, you don't need coding knowledge. The tool is designed to generate complete websites based on your topic description. However, having basic understanding of HTML/CSS can help you customize the output.

### Q: How long does it take to generate a website?
A: The generation time varies based on:
- Website complexity
- Number of pages
- Features requested
- API response times
Typically, a basic website can be generated in 5-10 minutes.

### Q: Can I customize the generated websites?
A: Yes, you can customize the generated websites by:
- Modifying the configuration files
- Adjusting agent behaviors
- Editing the output files directly
- Using the replay feature to modify specific tasks

### Q: What are the system requirements?
A: The minimum requirements are:
- Python 3.8+
- 4GB RAM
- 1GB free disk space
- Internet connection for API access

### Q: What is Google Gemini API and how is it used in this project?
A: Google Gemini API is a powerful AI model that provides advanced language understanding and generation capabilities. In this project, we use Gemini API for:
- Enhanced content generation
- Improved code understanding
- Better context management
- Advanced reasoning capabilities

### Q: How do I get started with Google Gemini API?
A: Follow these steps:
1. Visit the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gemini API
4. Create API credentials
5. Add your API key to the `.env` file

### Q: What are the costs associated with Google Gemini API?
A: Google Gemini API offers:
- A generous free tier
- Pay-as-you-go pricing
- Different model tiers (Pro, Ultra) with varying costs
- Visit [Google Cloud Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) for detailed information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, please:
1. Check the FAQ section
2. Review existing issues
3. Create a new issue if needed
4. Contact the maintainers

## 🙏 Acknowledgments

- CrewAI team for the amazing framework
- OpenAI for GPT models
- Google Cloud and Gemini API team for advanced AI capabilities
- Saptaparni Pal for her contributions in this project(crew.py)
