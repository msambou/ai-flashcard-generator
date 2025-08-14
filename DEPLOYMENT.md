# Deployment Guide

## Deploying to Vercel

### Prerequisites
- GitHub account
- Vercel account (free tier available)
- OpenAI API key

### Step 1: Prepare Your Repository
1. Push your code to a GitHub repository
2. Ensure all files are committed and pushed

### Step 2: Configure Environment Variables
1. Go to your Vercel dashboard
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. In the project settings, add environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key

### Step 3: Deploy
1. Vercel will automatically detect the configuration from `vercel.json`
2. The build process will:
   - Build the React frontend from the `/frontend` folder
   - Deploy the FastAPI backend as serverless functions in `/api`
3. Click "Deploy" to start the deployment

### Step 4: Access Your App
- Frontend: `https://your-project-name.vercel.app`
- API: `https://your-project-name.vercel.app/api/`

### Alternative Deployment Options

#### Option 1: Separate Deployments
**Frontend (Vercel):**
\`\`\`bash
cd frontend
npm run build
# Deploy the dist folder to Vercel
\`\`\`

**Backend (Railway/Render/Heroku):**
\`\`\`bash
cd backend
# Deploy to a Python hosting service
# Update VITE_API_URL in frontend to point to your backend URL
\`\`\`

#### Option 2: Docker Deployment
\`\`\`bash
# Build and deploy using Docker containers
docker-compose up --build
\`\`\`

### Environment Variables Needed
- `OPENAI_API_KEY`: Your OpenAI API key
- `CORS_ORIGINS`: Allowed origins for CORS (set to your frontend URL)

### Troubleshooting
- Ensure your OpenAI API key has sufficient credits
- Check Vercel function logs for backend errors
- Verify CORS settings if getting cross-origin errors
