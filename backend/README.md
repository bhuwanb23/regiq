# REGIQ Backend

Node.js backend for the REGIQ AI Compliance Copilot - Fintech Regulatory Intelligence, Bias Analysis, and Risk Simulation.

## 🚀 Getting Started

### Prerequisites
- Node.js 16+
- npm or yarn
- MongoDB (for development)

### Installation

1. Clone the repository
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
5. Start the development server:
   ```bash
   npm run dev
   ```

### Docker Setup

To run the application with Docker:
```bash
docker-compose up
```

### Available Scripts

- `npm start` - Start production server
- `npm run dev` - Start development server with nodemon
- `npm test` - Run tests
- `npm run lint` - Check for linting errors
- `npm run lint:fix` - Fix linting errors
- `npm run format` - Format code with Prettier

## 📁 Project Structure

```
backend/
├── src/
│   ├── controllers/     # Request handlers
│   ├── routes/         # API routes
│   ├── middleware/     # Custom middleware
│   ├── models/         # Database models
│   ├── services/       # Business logic
│   ├── utils/          # Utility functions
│   ├── config/         # Configuration files
│   └── server.js       # Entry point
├── tests/              # Test files
├── docs/               # Documentation
├── .env.example        # Environment variables example
├── .gitignore          # Git ignore file
├── package.json        # Project dependencies and scripts
├── Dockerfile          # Docker configuration
└── docker-compose.yml  # Docker Compose configuration
```

## 🌐 API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check

## 🛠️ Development

### Environment Variables

Create a `.env` file with the following variables:
- `PORT` - Server port (default: 3000)
- `NODE_ENV` - Environment (development/production/test)
- `DB_HOST` - Database host
- `DB_PORT` - Database port
- `DB_NAME` - Database name
- `JWT_SECRET` - JWT secret key
- `JWT_EXPIRES_IN` - JWT expiration time

## 🧪 Testing

Run tests with:
```bash
npm test
```

## 📚 Documentation

API documentation is available at `/docs` when the server is running.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## 📄 License

This project is licensed under the MIT License.