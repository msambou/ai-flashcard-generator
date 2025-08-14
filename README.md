# AI-Powered Flashcard Generator

A web application that allows teachers and students to upload text content (lecture notes, articles, etc.) and automatically generates flashcards with questions and answers using AI.

## Features

- **Text Upload**: Upload text files or paste content directly
- **AI-Powered Generation**: Automatically creates flashcards using OpenAI API
- **Interactive Flashcards**: Flip through generated flashcards with questions and answers
- **Clean Interface**: Modern, responsive design for easy use
- **Smart Card Generation**: Adapts number of flashcards based on content length
- **Error Handling**: Comprehensive error handling and user feedback
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices

## Tech Stack

### Frontend
- **ReactJS** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Axios** for API communication
- **Lucide React** for icons

### Backend
- **FastAPI** with Python
- **OpenAI API** (GPT-3.5-turbo) for AI-powered flashcard generation
- **Pydantic** for data validation
- **Async/Await** for non-blocking operations
- **CORS** middleware for cross-origin requests

## Project Structure

\`\`\`
ai-flashcard-generator/
├── frontend/                 # React TypeScript application
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Header.tsx
│   │   │   ├── TextInput.tsx
│   │   │   ├── FlashcardDisplay.tsx
│   │   │   ├── LoadingState.tsx
│   │   │   └── ErrorMessage.tsx
│   │   ├── services/        # API services
│   │   │   └── api.ts
│   │   ├── types/           # TypeScript type definitions
│   │   │   └── index.ts
│   │   ├── App.tsx          # Main application component
│   │   ├── main.tsx         # React entry point
│   │   └── index.css        # Global styles
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── .env.example
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI main application
│   │   ├── config.py        # Configuration settings
│   │   ├── models.py        # Pydantic models
│   │   └── services/        # Business logic
│   │       ├── __init__.py
│   │       ├── flashcard_service.py
│   │       └── openai_service.py
│   ├── requirements.txt
│   ├── run.py              # Development server runner
│   └── .env.example
├── scripts/                 # Development scripts
│   ├── start-dev.sh        # Start both servers
│   └── setup.sh            # Initial setup script
└── README.md
\`\`\`

## Quick Start

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Option 1: Automated Setup (Recommended)

1. Clone the repository:
   \`\`\`bash
   git clone <repository-url>
   cd ai-flashcard-generator
   \`\`\`

2. Run the setup script:
   \`\`\`bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   \`\`\`

3. Add your OpenAI API key to `backend/.env`:
   \`\`\`bash
   echo "OPENAI_API_KEY=your_api_key_here" > backend/.env
   \`\`\`

4. Start both servers:
   \`\`\`bash
   chmod +x scripts/start-dev.sh
   ./scripts/start-dev.sh
   \`\`\`

### Option 2: Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
   \`\`\`bash
   cd backend
   \`\`\`

2. Create a virtual environment:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Create environment file:
   \`\`\`bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   \`\`\`

5. Run the FastAPI server:
   \`\`\`bash
   python run.py
   # Or alternatively: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   \`\`\`

#### Frontend Setup

1. Navigate to the frontend directory:
   \`\`\`bash
   cd frontend
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

3. (Optional) Create environment file:
   \`\`\`bash
   cp .env.example .env
   # Edit if you need to change the API URL
   \`\`\`

4. Start the development server:
   \`\`\`bash
   npm run dev
   \`\`\`

## Usage

1. **Access the Application**: Open your browser to `http://localhost:5173`

2. **Upload Content**: 
   - Drag and drop a `.txt` file, or
   - Click "Choose File" to browse for a file, or
   - Paste text directly into the text area

3. **Generate Flashcards**: Click "Generate Flashcards" button

4. **Study**: 
   - Click on flashcards to flip between questions and answers
   - Use navigation buttons or dots to move between cards
   - Click "New Cards" to generate flashcards from different content

## API Documentation

### Endpoints

#### `GET /`
- **Description**: API information
- **Response**: Basic API details and version

#### `GET /health`
- **Description**: Health check endpoint
- **Response**: 
  \`\`\`json
  {
    "status": "healthy",
    "version": "1.0.0",
    "openai_configured": true
  }
  \`\`\`

#### `POST /generate-flashcards`
- **Description**: Generate flashcards from text content
- **Request Body**:
  \`\`\`json
  {
    "text": "Your educational content here..."
  }
  \`\`\`
- **Response**:
  \`\`\`json
  {
    "flashcards": [
      {
        "question": "What is...?",
        "answer": "The answer is..."
      }
    ],
    "total_count": 5
  }
  \`\`\`
- **Error Responses**:
  - `400`: Invalid input (empty text, too long, etc.)
  - `500`: Server error or OpenAI API issues

### Interactive API Documentation

When the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Environment Variables

### Backend (.env)
\`\`\`bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (with defaults)
API_TITLE="AI Flashcard Generator API"
API_VERSION="1.0.0"
HOST="0.0.0.0"
PORT=8000
RELOAD=true
\`\`\`

### Frontend (.env)
\`\`\`bash
# Optional (defaults to localhost:8000)
VITE_API_URL=http://localhost:8000
\`\`\`

## Development

### Code Structure

- **Frontend**: React components with TypeScript, using functional components and hooks
- **Backend**: FastAPI with async/await, dependency injection, and service layer architecture
- **AI Integration**: OpenAI GPT-3.5-turbo with structured prompts and JSON response formatting

### Key Features

- **Adaptive Card Generation**: Number of flashcards adapts to content length (3-12 cards)
- **Smart Text Processing**: Removes excessive whitespace and filters meaningful content
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Loading States**: Engaging loading animations during AI generation
- **Responsive Design**: Mobile-first design with Tailwind CSS

### Running Tests

\`\`\`bash
# Backend tests (if implemented)
cd backend
python -m pytest

# Frontend tests (if implemented)
cd frontend
npm test
\`\`\`

## Deployment

### Backend Deployment

The FastAPI backend can be deployed to platforms like:
- **Heroku**: Use `Procfile` with `web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}`
- **Railway**: Direct deployment with automatic Python detection
- **DigitalOcean App Platform**: Use `app.yaml` configuration
- **AWS Lambda**: With Mangum adapter for serverless deployment

### Frontend Deployment

The React frontend can be deployed to:
- **Vercel**: `npm run build` and deploy `dist/` folder
- **Netlify**: Direct GitHub integration with build command `npm run build`
- **GitHub Pages**: Static deployment after build
- **AWS S3 + CloudFront**: For scalable static hosting

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**:
   - Ensure your API key is correctly set in `backend/.env`
   - Check that your OpenAI account has sufficient credits
   - Verify the API key has the correct permissions

2. **CORS Errors**:
   - Ensure the frontend URL is included in `allowed_origins` in the backend
   - Check that both servers are running on the expected ports

3. **Module Not Found Errors**:
   - Ensure all dependencies are installed (`pip install -r requirements.txt` and `npm install`)
   - Activate the Python virtual environment before running the backend

4. **Port Already in Use**:
   - Change the port in the configuration files
   - Kill existing processes: `lsof -ti:8000 | xargs kill -9` (backend) or `lsof -ti:5173 | xargs kill -9` (frontend)

### Getting Help

- Check the browser console for frontend errors
- Check the terminal output for backend errors
- Ensure both servers are running and accessible
- Verify environment variables are correctly set

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

### Development Guidelines

- Follow TypeScript best practices for frontend code
- Use Python type hints and follow PEP 8 for backend code
- Add error handling for new features
- Update documentation for any API changes
- Test on both desktop and mobile devices

## License

MIT License - see LICENSE file for details

## Acknowledgments

- OpenAI for providing the GPT-3.5-turbo API
- FastAPI for the excellent Python web framework
- React and Vite for the frontend development experience
- Tailwind CSS for the utility-first CSS framework
